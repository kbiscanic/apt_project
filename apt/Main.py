# -*- coding: utf-8 -*-
from Model import Model

# TODO: TESTIRANJE DA SE VIDI STRUKTURA - START - MAKNI OVO KASNIJE
# model = Model()
# print model.preprocess(["cater pillar", "caterpillar"])  # treba ispast [caterpillar] i [caterpillar]
# print model.preprocess(["a b c de ef", "ab bc d e f"])  # treba ispast [ab c de ef] i [ab bc de f]
# print model.preprocess(["$US1234 $US1,234.00 $US345.12 $US -123.13 a sada normalni broj = 213.12", ""])
# print model.get_features(["r1", "r2"])
# print model.get_features([["r1", "r2"], ["a", "b"]])
# print model.preprocess([
# u"The broader Standard & Poor's 500 Index <.SPX> shed 2.38 points, or 0.24 percent, at 995.10",
#    u"Albuquerque Mayor Martin Chavez said investigators felt confident that with the arrests they had \"at least one of the fires resolved.\""
# ], True, True, False)
# print model.preprocess([
#    u"The broader Standard & Poor's 500 Index <.SPX> shed 2.38 points, or 0.24 percent, at 995.10",
#    u"Albuquerque Mayor Martin Chavez said investigators felt confident that with the arrests they had \"at least one of the fires resolved.\""
# ], True, True, True)
# print model.get_features([
#    u"The broader Standard & Poor's 500 Index <.SPX> shed 2.38 points, or 0.24 percent, at 995.10",
#    u"Albuquerque Mayor Martin Chavez said investigators felt confident that with the arrests they had \"at least one of the fires resolved.\""
# ])
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

# ispisuje izlaz modela u datoteku (rezultati se ogranicavaju na [0, 5])
def write_output(file, output):
    f = open(file, 'w')
    for x in output:
        if x < 0:
            r = 0
        elif x > 5:
            r = 5
        else:
            r = x
        f.write(str(r) + '\n')

# testiranje za 1 primjer
def test(X_train_file, y_train_file, X_test_file, y_test_file, train_out_file, test_out_file):
    X_train = load_data_X(X_train_file)
    y_train = load_data_y(y_train_file)
    X_test = load_data_X(X_test_file)
    y_test = load_data_y(y_test_file)

    model = Model()
    C_set = [2 ** x for x in range(-5, 15 + 1)]
    gamma_set = [2 ** x for x in range(-15, 3 + 1)]
    epsilon_set = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    model.train_k_fold(X_train, y_train, C_set, gamma_set, epsilon_set, 3)

    print "Tocni (train): ", y_train
    predicted_train = model.predict(X_train)
    print "Dobiveni (train): ", predicted_train
    write_output(train_out_file, predicted_train)

    print "Tocni (test): ", y_test
    predicted_test = model.predict(X_test)
    print "Dobiveni (test): ", predicted_test
    write_output(test_out_file, predicted_test)

    print 'C:', model.get_param_C()
    print 'epsilon:', model.get_param_epsilon()
    print 'gamma:', model.get_param_gamma()

# test('../data/train/STS.input.MSRpar.txt', '../data/train/STS.gs.MSRpar.txt',
#     '../data/test-gold/STS.input.MSRpar.txt', '../data/test-gold/STS.gs.MSRpar.txt',
#     'MSRpar_train.out', 'MSRpar_test.out')

# test('../data/train/STS.input.MSRvid.txt', '../data/train/STS.gs.MSRvid.txt',
#     '../data/test-gold/STS.input.MSRvid.txt', '../data/test-gold/STS.gs.MSRvid.txt',
#     'MSRvid_train.out', 'MSRvid_test.out')

test('../data/train/STS.input.SMTeuroparl.txt', '../data/train/STS.gs.SMTeuroparl.txt',
     '../data/test-gold/STS.input.SMTeuroparl.txt', '../data/test-gold/STS.gs.SMTeuroparl.txt',
     'SMTeuroparl_train.out', 'SMTeuroparl_test.out')

