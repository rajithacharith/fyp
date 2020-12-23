import numpy as np
import os

import pickle
import time
# from DictionaryWeighting import calcDicWeightForLine

dim = 1024
filename = 'kishky\model2_itm2.sav'
loaded_model = pickle.load(open(filename, 'rb'))

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
    def greedyMoversDistance(self,docA, docB, weightsA, weightsB, embedpathA, embedpathB, dataPathA, dataPathB, wordDictionary, distance_metric):
        docVecA = self.getDocVec(docA, embedpathA)
        docVecB = self.getDocVec(docB, embedpathB)
        docFileA = self.getDocFile(docA, dataPathA)
        docFileB = self.getDocFile(docB, dataPathB)

        maxSortedVecs = self.getSortedDistances(docVecA, docVecB, distance_metric)
        minSortedVecs = np.flipud(maxSortedVecs)
        # minSortedVecs = maxSortedVecs
        # print(minSortedVecs)
        distance = 0
        for sortedPair in minSortedVecs:
            weigVecA = weightsA[sortedPair["i"]]
            weigVecB = weightsB[sortedPair["j"]]
            flow = min(weigVecA, weigVecB)
            weightsA[sortedPair["i"]] = weigVecA - flow
            weightsB[sortedPair["j"]] = weigVecB - flow
            vecA = docVecA[sortedPair["i"]]
            vecB = docVecB[sortedPair["j"]]
            if (distance_metric == 1):
                distance = distance + ((loaded_model.score_pairs([(vecB, vecA)])[0]) + np.linalg.norm(vecA - vecB) + (1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA) * np.linalg.norm(vecB)))) * (
                    flow #* calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
                )
            elif (distance_metric == 2):
                distance = distance + ((1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA) * np.linalg.norm(vecB))) + (loaded_model.score_pairs([(vecB, vecA)])[0])) * (
                    flow #* calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
                )
            elif (distance_metric == 3):
                distance = distance + ((1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA) * np.linalg.norm(vecB))) + np.linalg.norm(vecA - vecB)) * (
                    flow #* calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
                )
            elif (distance_metric == 4):
                distance = distance + ((loaded_model.score_pairs([(vecB, vecA)])[0]) + np.linalg.norm(vecA - vecB)) * (
                    flow #* calcDicWeightForLine(docFileA[sortedPair["i"]], docFileB[sortedPair["j"]], wordDictionary)
                )
            elif (distance_metric == 5):
                distance = distance + (
                    (loaded_model.score_pairs([(vecB, vecA)])[0])
                        * flow
                    )
            elif (distance_metric == 6):
                distance = distance + (
                        np.linalg.norm(vecA - vecB)
                            * flow
                        )
            elif (distance_metric == 7):
                distance = distance + ((1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA) * np.linalg.norm(vecB))) * flow)
            else:
                print("error")
        return distance

    def getSortedDistances(self, docVecA, docVecB, distance_metric):
        eucDistances = np.array([])
        for i in range(len(docVecA)):
            for j in range(len(docVecB)):
                if (distance_metric == 1):
                    eucDistances = np.append(eucDistances, [loaded_model.score_pairs([(docVecA[i], docVecB[j])])[0] + np.linalg.norm(docVecA[i] - docVecB[j]) + 1 - np.dot(docVecA[i], docVecB[j])/(np.linalg.norm(docVecA[i]) * np.linalg.norm(docVecB[j]))])
                elif (distance_metric == 2):
                    eucDistances = np.append(eucDistances, [1 - np.dot(docVecA[i], docVecB[j])/(np.linalg.norm(docVecA[i]) * np.linalg.norm(docVecB[j])) + loaded_model.score_pairs([(docVecA[i], docVecB[j])])[0]])
                elif (distance_metric == 3):
                    eucDistances = np.append(eucDistances, [1 - np.dot(docVecA[i], docVecB[j])/(np.linalg.norm(docVecA[i]) * np.linalg.norm(docVecB[j])) + np.linalg.norm(docVecA[i] - docVecB[j])])
                elif (distance_metric == 4):
                    eucDistances = np.append(eucDistances, [loaded_model.score_pairs([(docVecA[i], docVecB[j])])[0] + np.linalg.norm(docVecA[i] - docVecB[j])])
                elif (distance_metric == 5):
                    eucDistances = np.append(eucDistances, [loaded_model.score_pairs([(docVecA[i], docVecB[j])])[0]])
                elif (distance_metric == 6):
                    eucDistances = np.append(eucDistances, [np.linalg.norm(docVecA[i] - docVecB[j])])
                elif (distance_metric == 7):
                    eucDistances = np.append(eucDistances, [1 - np.dot(docVecA[i], docVecB[j])/(np.linalg.norm(docVecA[i]) * np.linalg.norm(docVecB[j]))])
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
        docFile = open(path + doc.replace("raw", "txt"), "r",encoding='latin-1')
        lines = []
        for line in docFile.readlines():
            lines.append(line.strip().replace("\n", ""))
        return lines
