__author__ = 'karlo'


def norm(X, Y):
    if len(X) != len(Y):
        return

    a1 = 0.0
    a2 = 0.0
    a3 = 0.0
    b1 = 0.0
    b2 = 0.0
    b3 = 0.0
    for i in range(len(X)):
        a1 += X[i] * Y[i]
        a2 += -X[i] * X[i]
        a3 += -X[i]
        b1 += Y[i]
        b2 += -X[i]
        b3 += -1

    beta1 = (-b1 + a1 * b3 / a3) / (b2 - a2 * b3 / a3)
    beta2 = (-a1 - a2 * beta1) / a3

    for x in X:
        print x * beta1 + beta2


def tran_file(xName, yName):
    x = open(xName)
    X = []
    for line in x.readlines():
        X.append(float(line))

    y = open(yName)
    Y = []
    for line in y.readlines():
        Y.append(float(line))

    norm(X, Y)


xs = ["MSRpar_test.out", "MSRvid_test.out", "SMTeuroparl_test.out", "OnWn_test.out", "SMTnews_test.out"]
ys = ["STS.gs.MSRpar.txt", "STS.gs.MSRvid.txt", "STS.gs.SMTeuroparl.txt", "STS.gs.surprise.OnWN.txt",
      "STS.gs.surprise.SMTnews.txt"]

for i in range(len(xs)):
    tran_file("/home/karlo/PycharmProjects/apt_project/Rezultati9/" + xs[i],
              "/home/karlo/PycharmProjects/apt_project/data/test-gold/" + ys[i])