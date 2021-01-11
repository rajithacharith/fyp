import os
import pickle
import numpy as np
from .utils import read_sentence_file, read_emb_file, cosine_metrix, euclidean_metrix, metriclearning_metrix, get_MBS_metrix

filename = 'kishky\model2_itm2.sav'
loaded_model = pickle.load(open(filename, 'rb'))

def alignSentences(aligned_documents, distance_metric):
    ratio = False
    aligned_sentences = []
    for i in aligned_documents:
        path_embA = i[2]
        path_embB = i[3]
        path_sentences_A = i[0]
        path_sentences_B = i[1]

        embA = read_emb_file(path_embA)
        embB = read_emb_file(path_embB)
        sentences_A = read_sentence_file(path_sentences_A)
        sentences_B = read_sentence_file(path_sentences_B)

        if (distance_metric == 1):
            cosine = cosine_metrix(embA, embB)
            euclidean = euclidean_metrix(embA, embB)
            metriclearning = metriclearning_metrix(embA, embB, loaded_model)
            metrix_AB = np.add(cosine, euclidean)
            metrix_AB = np.add(metrix_AB, metriclearning)
            metrix_AB = metrix_AB / 3

        elif (distance_metric == 2):
            cosine = cosine_metrix(embA, embB)
            metriclearning = metriclearning_metrix(embA, embB, loaded_model)
            metrix_AB = np.add(cosine, metriclearning)
            metrix_AB = metrix_AB / 2

        elif (distance_metric == 3):
            cosine = cosine_metrix(embA, embB)
            euclidean = euclidean_metrix(embA, embB)
            metrix_AB = np.add(cosine, euclidean)
            metrix_AB = metrix_AB / 2

        elif (distance_metric == 4):
            euclidean = euclidean_metrix(embA, embB)
            metriclearning = metriclearning_metrix(embA, embB, loaded_model)
            metrix_AB = np.add(euclidean, metriclearning)
            metrix_AB = metrix_AB / 2

        elif (distance_metric == 5):
            metrix_AB = metriclearning_metrix(embA, embB, loaded_model)

        elif (distance_metric == 6):
            metrix_AB = euclidean_metrix(embA, embB)

        elif (distance_metric == 7):
            metrix_AB = cosine_metrix(embA, embB)

        else:
            print("error")

        if ratio == True:
            metrix_AB = get_MBS_metrix(metrix_AB, embA, embB)

        alignment = forward(metrix_AB, sentences_A, sentences_B)
        # alignment = backward(metrix_AB, sentences_A, sentences_B)
        # alignment = intersection(metrix_AB, sentences_A, sentences_B)
        aligned_sentences.extend(alignment)

    aligned_sentences.sort(key = lambda x:-x[-1])
    return aligned_sentences


def forward(metrix_AB, sentences_A, sentences_B):
    alignment = []
    for i in range (len(metrix_AB)):
        index_a = i
        score = np.max(metrix_AB[i])
        index_b = np.argmax(metrix_AB[i])
        alignment.append(
            (sentences_A[index_a][0], sentences_B[index_b][0], score)
        )
    return alignment


def backward(metrix_AB, sentences_A, sentences_B):
    alignment = []
    for i in range (len(metrix_AB.T)):
        index_b = i
        score = np.max(metrix_AB.T[i])
        index_a = np.argmax(metrix_AB.T[i])
        alignment.append(
            (sentences_A[index_a][0], sentences_B[index_b][0], score)
        )
    return alignment


def intersection(metrix_AB, sentences_A, sentences_B):
    alignment = []
    forw = forward(metrix_AB, sentences_A, sentences_B)
    backw = backward(metrix_AB, sentences_A, sentences_B)
    for i in range(len(forw)):
        if forw[i] in backw:
            alignment.append(forw[i])
    return alignment
