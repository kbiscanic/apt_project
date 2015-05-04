# weighted word overlap

__author__ = 'karlo'

from math import log

'''
FILE_FORMAT = 'googlebooks-{lang}-all-{ngram_len}gram-{version}-{index}.gz'

fname, url, records = next(readline_google_store(ngram_len=1, indices=['w']))
print fname
print url
print next(records)
'''

'''
def test():
    nltk.download('abc')
    print len(nltk.corpus.abc.words())


def freq(word):
    fname, url, records = next(readline_google_store(ngram_len=1))
    next(records)
'''


def read_data(filename):
    f = open(filename, 'r')
    now = int(f.readline())  # number of words

    ws = {}  # words and frequencies
    for line in f:
        l = line.split()
        ws[l[0]] = l[1]

    return now, ws


def calc_ic(word, data):
    if word in data[1]:
        return log(data[0], data[1][word])
    else:
        return 0


def calc_wwc(words1, words2, data):
    w1 = set(words1)
    w2 = set(words2)

    sum1 = 0
    for w in w1 & w2:
        sum1 += calc_ic(w, data)

    sum2 = 0
    for w in w2:
        sum2 += calc_ic(w, data)

    return sum1 / sum2


def calc_wwo(words1, words2):
    data = read_data('data/word-frequencies.txt')
    return 2 / (1 / calc_wwc(words1, words2, data) + 1 / calc_wwc(words2, words1, data))
