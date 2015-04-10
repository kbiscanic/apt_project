class Model:
    def _preprocess_strip(self):
        return

    def _preprocess_currency(self):
        return

    def _preprocess_tokenize(self):
        return

    def _preprocess_compounds(self):
        return

    def _preprocess_pos_tagging(self):
        return

    def _preprocess_stopwords(self):
        return

    def preprocess(self, x):
        # TODO - vraca preprocesirani niz tokena (tuplea) za 1 primjer
        return
    
    def get_features(self, X):
        # TODO - pozvati preprocess i zatim potrebne funkcije za izvaditi sve numericke znacajke
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
    
