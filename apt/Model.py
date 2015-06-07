# -*- coding: utf-8 -*-
import re

import numpy as np
import nltk
import sklearn
import sklearn.cross_validation

from apt.libsvm.python.svmutil import *
from features.karlo.WWO import calc_wwo
from features.karlo.ND import calc_nda, calc_ndc
from features.karlo.NO import calc_no
from features.kbiscanic.wordnet_aug_overlap import wordnet_aug_overlap_words
from features.kbiscanic.vector_space_similarity import vector_space_similarity_words
from features.kbiscanic.shallow_nerc import named_overlap_words
from features.kbiscanic.shallow_nerc import stocks_overlap_words
from features.jagar.ngram_overlap import calc_ngram_overlap
from features.karlo.word2vec import calc_w2v_similarity, w2v_model_load, w2v_model_unload

class Model:
    _NLTK_DATA_PATH = '../data/nltk'

    # model i parametri koji su koristeni pri ucenju
    _model = None
    _param_C = None
    _param_gamma = None
    _param_epsilon = None

    def __init__(self):
        if self._NLTK_DATA_PATH not in nltk.data.path:
            nltk.data.path.append(self._NLTK_DATA_PATH)

    # obavlja pocetno preprocesiranje recenice - prebacivanje u lowercase, micanje i zamjena nekih znakova
    def _preprocess_sentence(self, sentence, toLower=True):
        replace = {u'’': u'\'', u'``': u'"', u'\'\'': u'"', u'—': u'-', u'´': u'\''}
        for key in replace:
            sentence = sentence.replace(key, replace[key])
        str = re.sub(r"[\\\/\-()<>:#\[\]\{\}]", "", sentence.strip())
        if toLower:
            str = str.lower();
        return str

    # obavlja preprocesiranje novcanih vrijednosti u recenici
    def _preprocess_currency(self, sentence):
        return re.sub(ur"(\$|\€|\₤|\¥)[a-zA-Z]+([ 0-9.,]+)", ur"\1\2", sentence)

    # pretvara recenicu u tokene
    def _preprocess_tokenize(self, sentence):
        return nltk.word_tokenize(sentence)

    # obavlje preprocesiranje tokena - zamjenjuje odredjene tokene
    def _preprocess_token_replacement(self, tokens):
        replace = {u'\'m': u'am', u'n\'t': u'not', u'\'re': u'are'}
        return [replace.get(x.lower(), x) for x in tokens]

    # obavlja preprocesiranje compound tokena - ako se 2 susjedna tokena iz liste tokens1 pojavljuju zajedno u tokens2
    # onda se zamjenjuju sa spojenim tokenom
    def _preprocess_compounds(self, tokens1, tokens2):
        tokens2_lower = [x.lower() for x in tokens2]
        new_tokens1 = []
        i = 0
        while i < len(tokens1):
            if i == len(tokens1) - 1:
                new_tokens1.append(tokens1[i])
                break
            else:
                compound = tokens1[i] + tokens1[i + 1]
                if compound.lower() in tokens2_lower:
                    new_tokens1.append(compound)
                    i += 2
                else:
                    new_tokens1.append(tokens1[i])
                    i += 1
        return new_tokens1

    # dodaje tokenima POS tagove
    def _preprocess_pos_tagging(self, tokens):
        return nltk.pos_tag(tokens)

    # brise tokene koji predstavljaju stopwords
    def _preprocess_stopwords(self, tokens):
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.extend([u'.', u',', u'!', u'?', u'\'', u'"', u'\'\'', u'""', u'``'])
        return [x for x in tokens if x[0].lower() not in stopwords]

    # obavlja lematizaciju nad listom tokena
    def _preprocess_lemmatization(self, tokens):
        lemma_tokens = []
        for token in tokens:
            if re.match(r"\b[a-zA-z ]+\b", token[0]) is not None:
                if token[1] == 'NN':
                    wtag = nltk.corpus.wordnet.NOUN
                elif token[1] == 'JJ':
                    wtag = nltk.corpus.wordnet.ADJ
                elif token[1] == 'VB':
                    wtag = nltk.corpus.wordnet.VERB
                elif token[1] == 'RB':
                    wtag = nltk.corpus.wordnet.ADV
                else:
                    wtag = None

                if wtag is None:
                    lemma_tokens.append(token)
                else:
                    lemma_tokens.append((nltk.corpus.wordnet.morphy(token[0], wtag) or token[0], token[1]))
        return lemma_tokens

    # vraca listu koja sadrzi 2 liste preprocesiranih tokena za 1 primjer (primjer je lista od 2 recenice)
    def preprocess(self, X, toLower=True, stopwords=False, lemmatization=False):
        str = ["", ""]
        tokens = [[], []]

        for i in xrange(0, 2):
            str[i] = self._preprocess_sentence(X[i], toLower)
            str[i] = self._preprocess_currency(str[i])
            tokens[i] = self._preprocess_tokenize(str[i])
            tokens[i] = self._preprocess_token_replacement(tokens[i])

        for i in xrange(0, 2):
            tokens[i] = self._preprocess_compounds(tokens[i], tokens[1 - i])

        for i in xrange(0, 2):
            tokens[i] = self._preprocess_pos_tagging(tokens[i])
            if stopwords:
                tokens[i] = self._preprocess_stopwords(tokens[i])
            if lemmatization:
                tokens[i] = self._preprocess_lemmatization(tokens[i])

        return tokens

    # vraca znacajke za jedan ili vise primjera (1 primjer je lista sa 2 recenice)
    def get_features(self, X):
        w2v_model_load()

        X = np.array(X)
        if X.ndim == 1:
            X = np.array([X])

        X_features = []
        for x in X:
            features = []

            # originalni case podaci
            all_tokens_org_case = self.preprocess(x, False)
            all_words_org_case = [[t[0] for t in all_tokens_org_case[0]], [t[0] for t in all_tokens_org_case[1]]]

            # lowercase podaci
            all_tokens = self.preprocess(x)
            tokens = [self._preprocess_stopwords(all_tokens[0]), self._preprocess_stopwords(all_tokens[1])]
            lemma_tokens = [self._preprocess_lemmatization(tokens[0]), self._preprocess_lemmatization(tokens[1])]
            all_words = [[t[0] for t in all_tokens[0]], [t[0] for t in all_tokens[1]]]
            words = [[t[0] for t in tokens[0]], [t[0] for t in tokens[1]]]
            lemma_words = [[t[0] for t in lemma_tokens[0]], [t[0] for t in lemma_tokens[1]]]

            no = named_overlap_words(all_tokens_org_case)
            features.append(no[0])
            features.append(no[1])

            so = stocks_overlap_words(all_tokens_org_case)
            features.append(so[0])
            features.append(so[1])

            features.append(calc_ngram_overlap(words, 1))
            features.append(calc_ngram_overlap(words, 2))
            features.append(calc_ngram_overlap(words, 3))
            features.append(calc_ngram_overlap(lemma_words, 1))
            features.append(calc_ngram_overlap(lemma_words, 2))
            features.append(calc_ngram_overlap(lemma_words, 3))
            features.append(wordnet_aug_overlap_words(lemma_words))
            features.extend(calc_wwo(all_words))
            features.extend(calc_wwo(lemma_words))
            # features.append(vector_space_similarity_words(lemma_words, False))
            # features.append(vector_space_similarity_words(lemma_words, True))
            features.extend(calc_nda(words))
            features.extend(calc_ndc(all_words))
            features.extend(calc_no(all_words))
            features.extend(calc_w2v_similarity(lemma_words, False))
            features.extend(calc_w2v_similarity(lemma_words, True))

            X_features.append(features)

        w2v_model_unload()
        return X_features

    # obavlja treniranje modela sa zadanim parametrima
    def train(self, X, y, preprocess_X=True, C=1, gamma=1, epsilon=0.1):
        if preprocess_X:
            X = self.get_features(X)
        self._model = svm_train(y, X, '-s 3 -t 2 -q -c ' + str(C) + ' -g ' + str(gamma) + ' -p ' + str(epsilon))
        self._param_C = C
        self._param_gamma = gamma
        self._param_epsilon = epsilon

    # vraca parametar C naucenog modela
    def get_param_C(self):
        return self._param_C

    # vraca parametar gamma naucenog modela
    def get_param_gamma(self):
        return self._param_gamma

    # vraca parametar epsilon naucenog modela
    def get_param_epsilon(self):
        return self._param_epsilon

    # obavlja treniranje modela sa k-unakrsnom provjerom od k preklopa na zadanim vrijednostima za C, gamma i epsilon
    def train_k_fold(self, X, y, C_set, gamma_set, epsilon_set, k=10):
        print 'Zapocinje preprocessing, odredjivanje znacajki i priprema podataka'

        X = np.array(self.get_features(X))
        y = np.array(y)

        best_score_sum = None
        best_C = None
        best_gamma = None
        best_epsilon = None

        # napravi k preklopa u obliku lista (jer libsvm trazi liste, a ne np.array)
        kf = sklearn.cross_validation.KFold(n=len(X), n_folds=k, shuffle=True)
        X_train_folds = []
        X_validate_folds = []
        y_train_folds = []
        y_validate_folds = []
        for train_index, validate_index in kf:
            X_train, X_validate = X[train_index], X[validate_index]
            y_train, y_validate = y[train_index], y[validate_index]
            X_train_folds.append(X_train.tolist())
            X_validate_folds.append(X_validate.tolist())
            y_train_folds.append(y_train.tolist())
            y_validate_folds.append(y_validate.tolist())

        # brojaci napretka
        cnt = 0
        max_cnt = len(C_set) * len(gamma_set) * len(epsilon_set)
        print 'Ukupno koraka:', max_cnt

        for C in C_set:
            for gamma in gamma_set:
                for epsilon in epsilon_set:
                    # za svaki parametar prodji k preklopa
                    score_sum = 0
                    for i in xrange(0, k):
                        self.train(X_train_folds[i], y_train_folds[i], False, C, gamma, epsilon)
                        predicted_y = self.predict(X_validate_folds[i], False)
                        score_sum += np.corrcoef(y_validate_folds[i], predicted_y)[0, 1]

                    # povecaj brojac i ispisi ako treba
                    cnt += 1
                    if cnt % 500 == 0:
                        print cnt, '/', max_cnt

                    # da li su najbolji parametri? (moze se promatrati suma umjesto avg jer je uvijek k preklopa)
                    if best_score_sum is None or score_sum > best_score_sum:
                        best_score_sum = score_sum
                        best_C = C
                        best_gamma = gamma
                        best_epsilon = epsilon

        # nauci model na najboljim parametrima i cijelom skupu
        self.train(X.tolist(), y.tolist(), False, best_C, best_gamma, best_epsilon)

    # vraca predikciju za 1 primjer ili listu primjera
    def predict(self, X, preprocess_X=True):
        if preprocess_X:
            X = self.get_features(X)
        p_labels, _, _ = svm_predict(None, X, self._model, "-q")
        # y = [max(min(5, x), 0) for x in p_labels]
        return p_labels

