# -*- coding: utf-8 -*-
from Model import Model
import sys;

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

# ogranicava vrijednost x izmedju minx i maxx
def clamp(x, minx, maxx):
    return max(min(maxx, x), minx)

# ispisuje izlaz modela u datoteku file (rezultati se ogranicavaju na [0, 5])
def write_output(file, output):
    f = open(file, 'w')
    for x in output:
        r = clamp(x, 0, 5)
        f.write(str(r) + '\n')

# ispisuje n najgore ocjenjenih primjera u datoteku file (rezultati se ogranicavaju na [0, 5])
def write_low_scored(file, X, y, output, n):
    if (n >= len(output)):
        n = len(output) - 1
    diffs = [abs(clamp(output[i], 0, 5) - y[i]) for i in xrange(0, len(output))]
    diff_threshold = sorted(diffs, reverse=True)[n]

    f = open(file, 'w')
    for i in xrange(0, len(output)):
        r = clamp(output[i], 0, 5)
        diff = abs(r - y[i])
        if diff >= diff_threshold:
            f.write(X[i][0].encode('utf-8') + '\n')
            f.write(X[i][1].encode('utf-8') + '\n')
            f.write('Tocno: ' + str(y[i]) + '\n')
            f.write('Dobiveno: ' + str(r) + '\n')
            f.write('Razlika: ' + str(diff) + '\n')

# testiranje za 1 primjer
# moze se zadati model ako je vec naucen
def test(X_train_files, y_train_files, X_test_files, y_test_files, train_out_file, test_out_file,
         train_bad_out_file=None, test_bad_out_file=None,
         model=None, C_set=None, gamma_set=None, epsilon_set=None, k=None):
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    for file in X_train_files:
        X_train.extend(load_data_X(file))
    for file in y_train_files:
        y_train.extend(load_data_y(file))
    for file in X_test_files:
        X_test.extend(load_data_X(file))
    for file in y_test_files:
        y_test.extend(load_data_y(file))

    if model is None:
        if C_set is None:
            C_set = [2 ** x for x in range(-5, 15 + 1)]
        if gamma_set is None:
            gamma_set = [2 ** x for x in range(-15, 3 + 1)]
        if epsilon_set is None:
            epsilon_set = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6,
                           0.7, 0.8, 0.9, 1, 2]
        if k is None:
            k = 10
        model = Model()
        model.train_k_fold(X_train, y_train, C_set, gamma_set, epsilon_set, k)

    print 'C:', model.get_param_C()
    print 'epsilon:', model.get_param_epsilon()
    print 'gamma:', model.get_param_gamma()

    if train_out_file != '':
        # print "Tocni (train): ", y_train
        predicted_train = model.predict(X_train)
        # print "Dobiveni (train): ", predicted_train
        write_output(train_out_file, predicted_train)
        if (train_bad_out_file is not None):
            write_low_scored(train_bad_out_file, X_train, y_train, predicted_train, 50)

    if test_out_file != '':
        # print "Tocni (test): ", y_test
        predicted_test = model.predict(X_test)
        # print "Dobiveni (test): ", predicted_test
        write_output(test_out_file, predicted_test)
        if (test_bad_out_file is not None):
            write_low_scored(test_bad_out_file, X_test, y_test, predicted_test, 50)

    return model

# pokreni ucenje i evaluaciju
k = 1
if len(sys.argv) >= 2:
    k = int(sys.argv[1])
print "Trazena akcija k =", k
if k == 1:
    # MSRpar
    print 'MSRpar'
    test(['../data/train/STS.input.MSRpar.txt'], ['../data/train/STS.gs.MSRpar.txt'],
         ['../data/test-gold/STS.input.MSRpar.txt'], ['../data/test-gold/STS.gs.MSRpar.txt'],
         'MSRpar_train.out', 'MSRpar_test.out', 'MSRpar_train_bad.txt', 'MSRpar_test_bad.txt')
elif k == 2:
    # MSRvid
    print 'MSRvid'
    test(['../data/train/STS.input.MSRvid.txt'], ['../data/train/STS.gs.MSRvid.txt'],
         ['../data/test-gold/STS.input.MSRvid.txt'], ['../data/test-gold/STS.gs.MSRvid.txt'],
         'MSRvid_train.out', 'MSRvid_test.out', 'MSRvid_train_bad.txt', 'MSRvid_test_bad.txt')
elif k == 3:
    # SMTeuroparl i SMTnews
    print 'SMTeuroparl'
    model = test(['../data/train/STS.input.SMTeuroparl.txt'], ['../data/train/STS.gs.SMTeuroparl.txt'],
                 ['../data/test-gold/STS.input.SMTeuroparl.txt'], ['../data/test-gold/STS.gs.SMTeuroparl.txt'],
         'SMTeuroparl_train.out', 'SMTeuroparl_test.out', 'SMTeuroparl_train_bad.txt', 'SMTeuroparl_test_bad.txt')
    print 'SMTnews'
    test([], [],
        ['../data/test-gold/STS.input.surprise.SMTnews.txt'], ['../data/test-gold/STS.gs.surprise.SMTnews.txt'],
        '', 'SMTnews_test.out', '', 'SMTnews_test_bad.txt', model)
elif k == 4:
    # OnWn i All
    print 'OnWn'
    model = test(['../data/train/STS.input.MSRpar.txt', '../data/train/STS.input.MSRvid.txt',
                  '../data/train/STS.input.SMTeuroparl.txt'],
                 ['../data/train/STS.gs.MSRpar.txt', '../data/train/STS.gs.MSRvid.txt',
                  '../data/train/STS.gs.SMTeuroparl.txt'],
                 ['../data/test-gold/STS.input.surprise.OnWN.txt'],
                 ['../data/test-gold/STS.gs.surprise.OnWN.txt'],
                 'OnWn_train.out', 'OnWn_test.out', 'OnWn_train_bad.txt', 'OnWn_test_bad.txt',
                 None, [2 ** x for x in range(-3, 11 + 1)], [2 ** x for x in range(-15, 3 + 1)],
                 [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5, 0.75, 1, 2], 3)
    print 'All'
    test([], [],
        ['../data/test-gold/STS.input.MSRpar.txt', '../data/test-gold/STS.input.MSRvid.txt',
         '../data/test-gold/STS.input.SMTeuroparl.txt', '../data/test-gold/STS.input.surprise.SMTnews.txt',
         '../data/test-gold/STS.input.surprise.OnWN.txt'],
        ['../data/test-gold/STS.gs.MSRpar.txt', '../data/test-gold/STS.gs.MSRvid.txt',
         '../data/test-gold/STS.gs.SMTeuroparl.txt', '../data/test-gold/STS.gs.surprise.SMTnews.txt',
         '../data/test-gold/STS.gs.surprise.OnWN.txt'],
        '', 'All_test.out', '', 'All_test_bad.txt', model)