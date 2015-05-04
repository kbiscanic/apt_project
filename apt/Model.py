# -*- coding: utf-8 -*-
import nltk
import re
import numpy as np
import libsvm.python.svm

class Model:
    _NLTK_DATA_PATH = '../data/nltk'

    def __init__(self):
        if self._NLTK_DATA_PATH not in nltk.data.path:
            nltk.data.path.append(self._NLTK_DATA_PATH)

    # obavlja pocetno preprocesiranje recenice - prebacivanje u lowercase, micanje i zamjena nekih znakova
    def _preprocess_sentence(self, sentence):
        replace = {u'’': u'\'', u'``': u'"', u'\'\'': u'"', u'—': u'-', u'´': u'\''}
        for key in replace:
            sentence = sentence.replace(key, replace[key])
        return re.sub(r"[\\\/\-()<>:#\[\]\{\}]", "", sentence.strip().lower())

    # obavlja preprocesiranje novcanih vrijednosti u recenici
    def _preprocess_currency(self, sentence):
        return re.sub(ur"(\$|\€|\₤|\¥)[a-zA-Z]+([ 0-9.,]+)", ur"\1\2", sentence)

    # pretvara recenicu u tokene
    def _preprocess_tokenize(self, sentence):
        return nltk.word_tokenize(sentence)

    # obavlje preprocesiranje tokena - zamjenjuje odredjene tokene
    def _preprocess_token_replacement(self, tokens):
        replace = {u'\'m': u'am', u'n\'t': u'not', u'\'re': u'are'}
        return [replace.get(x, x) for x in tokens]

    # obavlja preprocesiranje compound tokena - ako se 2 susjedna tokena iz liste tokens1 pojavljuju zajedno u tokens2
    # onda se zamjenjuju sa spojenim tokenom
    def _preprocess_compounds(self, tokens1, tokens2):
        new_tokens1 = []
        i = 0
        while i < len(tokens1):
            if i == len(tokens1) - 1:
                new_tokens1.append(tokens1[i])
                break
            else:
                compound = tokens1[i] + tokens1[i + 1]
                if compound in tokens2:
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
        return [x for x in tokens if x[0] not in stopwords]

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
    def preprocess(self, X, stopwords=False, lemmatization=False):
        str = ["", ""]
        tokens = [[], []]

        for i in range(0, 2):
            str[i] = self._preprocess_sentence(X[i])
            str[i] = self._preprocess_currency(str[i])
            tokens[i] = self._preprocess_tokenize(str[i])
            tokens[i] = self._preprocess_token_replacement(tokens[i])

        for i in range(0, 2):
            tokens[i] = self._preprocess_compounds(tokens[i], tokens[1 - i])

        for i in range(0, 2):
            tokens[i] = self._preprocess_pos_tagging(tokens[i])
            if stopwords:
                tokens[i] = self._preprocess_stopwords(tokens[i])
            if lemmatization:
                tokens[i] = self._preprocess_lemmatization(tokens[i])

        return tokens

    # vraca ngram overlap znacajke za 2 liste tokena
    def _get_ngram_overlap(self, tokens):
        # TODO
        return [1, 2, 3]

    # vraca znacajke za jedan ili vise primjera (1 primjer je lista sa 2 recenice)
    def get_features(self, X):
        X = np.array(X)
        if X.ndim == 1:
            X = np.array([X])

        X_features = []
        for x in X:
            features = []
            all_tokens = self.preprocess(x)
            tokens = [self._preprocess_stopwords(all_tokens[0]), self._preprocess_stopwords(all_tokens[1])]
            lemma_tokens = [self._preprocess_lemmatization(tokens[0]), self._preprocess_lemmatization(tokens[1])]

            features.extend(self._get_ngram_overlap(tokens))
            features.extend(self._get_ngram_overlap(lemma_tokens))
            # TODO - pozvati ostale funkcije za feature koji postoje i dodati ih u features listu (kao linija gore)
            # TODO - ovisno o vrsti featurea, negdje ce se koristiti all_tokens, negdje tokens a negdje lemma_tokens
            # TODO - najbolje pogledati u sourcu onom

            X_features.append(features)

        return X_features

    # obavlja treniranje modela sa zadanim parametrima
    def train(self, X, y):
        return

    # obavlja treniranje modela sa k-unakrsnom provjerom od k preklopa
    def train_k_fold(self, X, y, k=5):
        # TODO - X, y training setovi, radi se k-unakrsna provjera za optimalne hiperparametre
        # parametre i pravi objekt modela ce se pamtiti u varijablama klase
        return

    def predict(self, X):
        # vraca rezultat za 1 primjer ili listu primjera
        return
    
