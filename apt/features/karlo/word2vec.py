__author__ = 'karlo'

from gensim.models import Word2Vec
from gensim import matutils
from numpy import dot, array

from WWO import calc_ic


def sentence_vec(words, use_ic=False):
    vec = None
    for w in words:
        try:
            v = w2v_model[w]
            if vec is None:
                if use_ic:
                    ic = calc_ic(w)
                    vec = [ic * v[i] for i in range(len(v))]
                else:
                    vec = [v[i] for i in range(len(v))]
            else:
                if use_ic:
                    ic = calc_ic(w)
                    vec = [ic * v[i] + vec[i] for i in range(len(v))]
                else:
                    vec = [v[i] + vec[i] for i in range(len(v))]
        except KeyError:
            pass
    if vec is not None:
        return vec
    else:
        return [0] * w2v_dimension


def calc_w2v_similarity(words, use_ic=False):
    words1 = words[0]
    words2 = words[1]

    vec1 = sentence_vec(words1, use_ic)
    vec2 = sentence_vec(words2, use_ic)

    return [dot(matutils.unitvec(array(vec1)), matutils.unitvec(array(vec2)))]


def w2v_model_load():
    global w2v_model
    global w2v_dimension
    if w2v_model is None:
        # w2v_model = Word2Vec.load_word2vec_format("features/karlo/GoogleNews-vectors-negative300.bin", binary=True)
        #w2v_dimension = 300
        w2v_model = Word2Vec.load_word2vec_format("features/karlo/vectors.6B.50d.txt", binary=False)
        w2v_dimension = 50

def w2v_model_unload():
    global w2v_model
    w2v_model = None


w2v_model = None
w2v_dimension = 0

