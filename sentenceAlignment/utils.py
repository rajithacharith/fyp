import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


def read_sentence_file(path):
    sentences = open(path, "r", encoding='utf-8').read()
    sentences = sentences.split("\n")
    sentences = sentences[:-1]
    sentences = [i.split("\t") for i in sentences]
    return sentences


def read_emb_file(path):
    dim = 1024
    X = np.fromfile(path, dtype=np.float32, count=-1)
    X.resize(X.shape[0] // dim, dim)
    return X


def metric_learning_similarity_ab(loaded_model, tupple_list):
    distance = loaded_model.score_pairs(tupple_list)
    similarity = 1-distance
    return similarity


def cosine_metrix(embA, embB):
    metrix_AB = cosine_similarity(embA, embB)
    return metrix_AB


def euclidean_metrix(embA, embB):
    distances = euclidean_distances(embA, embB)
    metrix_AB = 1 - np.array(distances)
    return metrix_AB


def metriclearning_metrix(embA, embB, loaded_model):
    metrix_AB = []
    for index_a in range(len(embA)):
        vec_a = embA[index_a]
        tupple_list = []
        for vec_b in embB:
            tupple_list.append((vec_a,vec_b))
        similarities = metric_learning_similarity_ab(loaded_model, tupple_list)
        metrix_AB.append(similarities)
    return np.array(metrix_AB)


def get_neighbours(metrix_AB, k=4):
    neighbours_A = {}
    for i in range (len(metrix_AB)):
        neighbour_indexes = np.argsort(metrix_AB[i])[-k:]
        # neighbour_indexes = np.argsort(cs_metrix_AB[i])[0:k]
        neighbours_A[i] = neighbour_indexes
    neighbours_B = {}
    for j in range (len(metrix_AB.T)):
        neighbour_indexes = np.argsort(metrix_AB.T[j])[-k:]
        # neighbour_indexes = np.argsort(cs_metrix_AB.T[j])[0:k]
        neighbours_B[j] = neighbour_indexes
    return neighbours_A, neighbours_B


def margin_based_score_ab(metrix_AB, neighbours_a, neighbours_b, index_a, index_b):
    tot_similarity_of_neighbours_a = 0
    for i in neighbours_a:
        tot_similarity_of_neighbours_a += metrix_AB[index_a, i]
    tot_similarity_of_neighbours_b = 0
    for i in neighbours_b:
        tot_similarity_of_neighbours_b += metrix_AB.T[index_b, i]
    mbs_ab = (len(neighbours_a)+len(neighbours_b)) * metrix_AB[index_a, index_b] / (tot_similarity_of_neighbours_a + tot_similarity_of_neighbours_b)
    return mbs_ab


def get_MBS_metrix(metrix_AB, embA, embB):
    neighbours_A, neighbours_B = get_neighbours(metrix_AB)
    mbs_metrix_AB = []
    for index_a in range (len(metrix_AB)):
        mb_scores = []
        neighbours_a = neighbours_A[index_a]
        for index_b in range (len(metrix_AB.T)):
            neighbours_b = neighbours_B[index_b]
            mb_score = margin_based_score_ab(metrix_AB, neighbours_a, neighbours_b, index_a, index_b)
            mb_scores.append(mb_score)
        mbs_metrix_AB.append(mb_scores)
    mbs_metrix_AB = np.array(mbs_metrix_AB)
    return mbs_metrix_AB
