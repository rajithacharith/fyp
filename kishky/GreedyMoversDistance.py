import numpy as np
import os

import pickle
import time
# from DictionaryWeighting import calcDicWeightForLine

dim = 1024

# Input for the method must be array of tuples

# def greedyMoversDistance(docA, docB, weightsA, weightsB, embedpathA, embedpathB):
#     docVecA = getDocVec(docA, embedpathA)
#     docVecB = getDocVec(docB, embedpathB)
#     maxSortedVecs = getSortedDistances(docVecA, docVecB)
#     minSortedVecs = np.flipud(maxSortedVecs)
#     distance = 0
#     for sortedPair in minSortedVecs:
#         weigVecA = weightsA[sortedPair["i"]]
#         weigVecB = weightsB[sortedPair["j"]]
#         flow = min(weigVecA, weigVecB)
#         weightsA[sortedPair["i"]] = weigVecA - flow
#         weightsB[sortedPair["j"]] = weigVecB - flow
#         vecA = docVecA[sortedPair["i"]]
#         vecB = docVecB[sortedPair["j"]]
#         distance = distance + np.linalg.norm(vecA - vecB) * flow
#     return distance
class GreedyMoversDistance:
    def greedyMoversDistance(self,docA, docB, weightsA, weightsB, embedpathA, embedpathB, wordDictionary):
        docVecA = self.getDocVec(docA, embedpathA)
        docVecB = self.getDocVec(docB, embedpathB)
        docFileA = self.getDocFile(docA, embedpathA)
        docFileB = self.getDocFile(docB, embedpathB)

        maxSortedVecs = self.getSortedDistances(docVecA, docVecB)
        minSortedVecs = np.flipud(maxSortedVecs)
        # minSortedVecs = maxSortedVecs
        # print(minSortedVecs)
        distance = 0
        for sortedPair in minSortedVecs:
            # print(sortedPair)
            # print(len(weightsA))
            weigVecA = weightsA[sortedPair["i"]]
            weigVecB = weightsB[sortedPair["j"]]
            flow = min(weigVecA, weigVecB)
            weightsA[sortedPair["i"]] = weigVecA - flow
            weightsB[sortedPair["j"]] = weigVecB - flow
            vecA = docVecA[sortedPair["i"]]
            vecB = docVecB[sortedPair["j"]]
            # only euclidean
            distance = distance + (
                np.linalg.norm(vecA - vecB) * flow
                )
            # only cosine
            # distance = distance + (1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) * flow
            # cosine + euclidean
            # distance = distance + ((1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) + np.linalg.norm(vecA - vecB)) * (
            #     flow * calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
            #     )
            # metric learning distance
            # distance = distance + (
            #     (
            #         loaded_model.score_pairs([(vecB, vecA)])[0]) * flow
            #         )

            # print(distance)
        # dicWeight = calcDictionaryWeight(docA, docB, embedpathA, embedpathB, wordDictionary)
        # return distance * dicWeight
        return distance

    def getSortedDistances(self,docVecA, docVecB):
        eucDistances = np.array([])
        for i in range(len(docVecA)):
            for j in range(len(docVecB)):
                eucDistances = np.append(eucDistances, [np.linalg.norm(docVecA[i] - docVecB[j])])
                # eucDistances = np.append(eucDistances,
                #     [((1 - np.dot(docVecA[i], docVecB[j])/(np.linalg.norm(docVecA[i])*np.linalg.norm(docVecB[j]))) + np.linalg.norm(docVecA[i] - docVecB[j]))])
                # eucDistances = np.append(eucDistances,
                #     [loaded_model.score_pairs([(docVecA[i], docVecB[j])])[0]])
                # print(eucDistances)
        sortedVecs = []
        for i in range(len(eucDistances)):
            maxi = eucDistances.argmax()
            sortedVecs.append({"dist": eucDistances[maxi], "i": maxi//len(docVecB), "j": maxi % len(docVecB)})
            eucDistances[maxi] = 0
        return sortedVecs

    def getDocVec(self,doc, path):
        docVec = np.fromfile(path + doc, dtype = np.float32, count = -1)
        docVec.resize(docVec.shape[0] // dim, dim)
        return docVec

    def getDocFile(self,doc, path):
        docFile = open(path.replace("embeddings", "txtfiles") + doc.replace("raw", "txt"), "r",encoding='latin-1')
        lines = []
        for line in docFile.readlines():
            lines.append(line.strip().replace("\n", ""))
        return lines

