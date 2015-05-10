# -*- coding: utf-8 -*-
from Model import Model

# TODO: TESTIRANJE DA SE VIDI STRUKTURA - START - MAKNI OVO KASNIJE
model = Model()
# print model.preprocess(["cater pillar", "caterpillar"])  # treba ispast [caterpillar] i [caterpillar]
# print model.preprocess(["a b c de ef", "ab bc d e f"])  # treba ispast [ab c de ef] i [ab bc de f]
# print model.preprocess(["$US1234 $US1,234.00 $US345.12 $US -123.13 a sada normalni broj = 213.12", ""])
# print model.get_features(["r1", "r2"])
# print model.get_features([["r1", "r2"], ["a", "b"]])
print model.preprocess([
    u"The broader Standard & Poor's 500 Index <.SPX> shed 2.38 points, or 0.24 percent, at 995.10",
    u"Albuquerque Mayor Martin Chavez said investigators felt confident that with the arrests they had \"at least one of the fires resolved.\""
], True, True, False)
print model.preprocess([
    u"The broader Standard & Poor's 500 Index <.SPX> shed 2.38 points, or 0.24 percent, at 995.10",
    u"Albuquerque Mayor Martin Chavez said investigators felt confident that with the arrests they had \"at least one of the fires resolved.\""
], True, True, True)
print model.get_features([
    u"The broader Standard & Poor's 500 Index <.SPX> shed 2.38 points, or 0.24 percent, at 995.10",
    u"Albuquerque Mayor Martin Chavez said investigators felt confident that with the arrests they had \"at least one of the fires resolved.\""
])
# TODO: TESTIRANJE DA SE VIDI STRUKTURA - END - MAKNI OVO KASNIJE

# ucitava primjere iz zadane datoteke
def load_data_X(file):
    X = []
    for line in open(file):
        line = line.decode('utf-8')
        sentences = line.strip().split('\t')
        X.append(sentences)
    return X

# ucitava izlaze primjera iz zadane datoteke
def load_data_y(file):
    y = []
    for line in open(file):
        y.append(float(line))
    return y

X_train = load_data_X('../data/train/STS.input.MSRpar.txt')
y_train = load_data_y('../data/train/STS.gs.MSRpar.txt')
X_test = load_data_X('../data/test-gold/STS.input.MSRpar.txt')
y_test = load_data_y('../data/test-gold/STS.gs.MSRpar.txt')
# model = Model()
# model.train(X_train, y_train)
# model.train_k_fold(X_train, y_train, [1, 2, 3], [1, 2, 3], [0.1, 0.2, 0.3], 3)
# print "Tocni: ", y_train
# ove dodatne debug poruke ispisuje sam library, a MSE nije tocan (jer se nije predao pravi y u predict, ali se moze)
# print "Dobiveni: ", model.predict(X_train)
