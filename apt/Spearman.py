__author__ = 'karlo'

from scipy.stats import spearmanr


def sp_file(xName, yName):
    x = open(xName)
    X = []
    for line in x.readlines():
        X.append(float(line))

    y = open(yName)
    Y = []
    for line in y.readlines():
        Y.append(float(line))

    print spearmanr(X, Y)


xs_train = ["MSRpar_train.out", "MSRvid_train.out", "SMTeuroparl_train.out", "OnWn_train.out", "SMTeuroparl_train.out"]
xs_test = ["MSRpar_test.out", "MSRvid_test.out", "SMTeuroparl_test.out", "OnWn_test.out", "SMTnews_test.out"]
ys_train = ["STS.gs.MSRpar.txt", "STS.gs.MSRvid.txt", "STS.gs.SMTeuroparl.txt", "STS.gs.union.txt",
            "STS.gs.SMTeuroparl.txt"]
ys_test = ["STS.gs.MSRpar.txt", "STS.gs.MSRvid.txt", "STS.gs.SMTeuroparl.txt", "STS.gs.surprise.OnWN.txt",
           "STS.gs.surprise.SMTnews.txt"]

for i in range(len(xs_train)):
    sp_file("/home/karlo/PycharmProjects/apt_project/Rezultati9/" + xs_train[i],
            "/home/karlo/PycharmProjects/apt_project/data/train/" + ys_train[i])
    sp_file("/home/karlo/PycharmProjects/apt_project/Rezultati9/" + xs_test[i],
            "/home/karlo/PycharmProjects/apt_project/data/test-gold/" + ys_test[i])

sp_file("/home/karlo/PycharmProjects/apt_project/Rezultati9/All_test.out",
        "/home/karlo/PycharmProjects/apt_project/data/test-gold/STS.gs.ALL.txt")
sp_file("/home/karlo/PycharmProjects/apt_project/Rezultati9/All_test_norm.out",
        "/home/karlo/PycharmProjects/apt_project/data/test-gold/STS.gs.ALL.txt")