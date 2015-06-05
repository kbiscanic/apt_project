__author__ = 'karlo'

from gensim.models import Word2Vec
from gensim import matutils
from numpy import dot, array

from WWO import calc_ic

def sentence_vec(words):
    vec = None
    for w in words:
        try:
            v = w2v_model[w]
            ic = calc_ic(w)
            if vec is None:
                vec = [ic * v[i] for i in range(len(v))]
            else:
                vec = [ic * v[i] + vec[i] for i in range(len(v))]
        except KeyError:
            pass
    return vec


def calc_w2v_similarity(words):
    words1 = words[0]
    words2 = words[1]

    vec1 = sentence_vec(words1)
    vec2 = sentence_vec(words2)

    return [dot(matutils.unitvec(array(vec1)), matutils.unitvec(array(vec2)))]


def w2v_model_load():
    global w2v_model
    if w2v_model is None:
        w2v_model = Word2Vec.load_word2vec_format("features/karlo/GoogleNews-vectors-negative300.bin", binary=True)
        # w2v_model = Word2Vec.load_word2vec_format("features/karlo/vectors.6B.50d.txt", binary=False)


def w2v_model_unload():
    global w2v_model
    w2v_model = None


w2v_model = None


