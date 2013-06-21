# coding=utf-8
from InverseTable import *
from Parsing import Parser
import math
import os


class QueryAnalysis(object):

    def __init__(self):
        self.parser = Parser(os.path.join(os.path.dirname(__file__),
                             "Stopword.txt"))

    def analysis(self, Query):
        return self.parser.getIndexToken(Query)


class Ranker(object):
    db = MongoClient().poky

    def __init__(self):
        self.inverseTable = {}
        terms = self.db.terms.find()
        for term in terms:
            self.inverseTable[term["word"]] = {
                "df": term["df"],
                "idf": term["idf"],
                "posting": {}
            }
            for node in term["posting"]:
                self.inverseTable[term["word"]]["posting"][node["doc_id"]] = node["tf"]

        self.pageRank = {}
        self.normalization = {}
        documents = self.db.documents.find({"pagerank": {"$exists": True}, "normalization": {"$exists": True}})
        for document in documents:
            self.pageRank[document["_id"]] = document["pagerank"]
            self.normalization[document["_id"]] = document["normalization"]

    def __queryVec(self, query):
        for key in query:
            if key in self.inverseTable:
                query[key] = (1 + math.log(query[key])) * self.inverseTable[key]["idf"]
            else:
                query[key] = 0
        return query

    def __cosine(self, queryVec):
        Rank = {}
        ResultList = {}
        for word in queryVec:
            if queryVec[word] != 0:
                ResultList[word] = self.inverseTable[word]["posting"]
        for word in ResultList:
            for document in ResultList[word]:
                if document not in Rank:
                    Rank[document] = 0
                Rank[document] += (queryVec[word]*ResultList[word][document])
        #calculate Cosine
        queryNormalization = self.__getNormalization(queryVec)
        for document in Rank:
            Rank[document] /= (queryNormalization * self.normalization[document])
        return Rank

    def __getNormalization(self, queryVec):
        sum = 0.0
        for word in queryVec:
            sum += (queryVec[word] * queryVec[word])
        return math.sqrt(sum)

    def rank(self, query):
        queryVec = self.__queryVec(query)
        cosine = self.__cosine(queryVec)

        PR = {}
        for item in cosine:
            PR[item] = self.pageRank[item]
        maxCos = max(cosine.values())
        maxPR = max(PR.values())
        finalRank = PR
        for key in finalRank:
            finalRank[key] = 0.4 * PR[key] + 0.6 * cosine[key] * maxPR / maxCos
        return [item[0] for item in sorted(finalRank.items(), key=lambda x: x[1], reverse=True)]
