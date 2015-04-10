import nltk

class Model:
    _NLTK_DATA_PATH = '../data/nltk'

    def __init__(self):
        if self._NLTK_DATA_PATH not in nltk.data.path:
            nltk.data.path.append(self._NLTK_DATA_PATH)

    def _preprocess_strip(self, sentence):
        # TODO - da li treba maknuti i . , ? ! [ ] ' "
        return sentence.strip().translate({'\\': '', '/': '', '-': '', '(': '', ')': '', '<': '', '>': ''})

    def _preprocess_currency(self, sentence):
        # TODO
        return sentence

    def _preprocess_tokenize(self, sentence):
        return nltk.word_tokenize(sentence)

    def _preprocess_compounds(self, tokens):
        # TODO
        return tokens

    def _preprocess_pos_tagging(self, tokens):
        return nltk.pos_tag(tokens)

    def _preprocess_stopwords(self, tokens):
        stopwords = nltk.corpus.stopwords.words('english')
        return [x for x in tokens if x[0] not in stopwords]

    # vraca preprocesirani niz tokena za 1 recenicu
    def preprocess(self, sentence):
        sentence = self._preprocess_strip(sentence)
        sentence = self._preprocess_currency(sentence)
        tokens = self._preprocess_tokenize(sentence)
        tokens = self._preprocess_compounds(tokens)
        tokens = self._preprocess_pos_tagging(tokens)
        tokens = self._preprocess_stopwords(tokens)
        return tokens
    
    def get_features(self, X):
        # TODO - pozvati za obje recenice preprocess i zatim potrebne funkcije za izvaditi sve numericke znacajke
        # jedan primjer je lista od 2 recenice (stringa)
        # ako je X jedan primjer vratiti listu znacajki za njega
        # ako je X lista primjera vratiti listu znacajki za svaki primjer
        return
    
    def train(self, X, y, k = 5):
        # TODO - X, y training setovi, radi se k-unakrsna provjera za optimalne hiperparametre
        # parametre i pravi objekt modela ce se pamtiti u varijablama klase
        return
    
    def predict(self, X):
        # vraca rezultat za 1 primjer ili listu primjera
        return
    
