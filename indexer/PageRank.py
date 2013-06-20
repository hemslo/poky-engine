import copy
from pymongo import MongoClient


class PageRank(object):

    def __init__(self, graph, Ep):
        self.graph = graph
        self.lastIter = {}
        self.currentIter = {}
        for key in graph:
            self.lastIter[key] = float(1)/len(graph.keys())
            self.currentIter[key] = 0
        self.Ep = Ep/len(graph.keys())

    def __converse(self):
        for key in self.lastIter:
            if abs(self.currentIter[key] -
                   self.lastIter[key]) / max(self.currentIter[key],
                                             self.lastIter[key]) >= 0.05:
                return False
        return True

    def __update(self):
        for key in self.graph:
            N = len(self.graph[key])
            for item in self.graph[key]:
                if item in self.graph:
                    self.currentIter[item] += self.lastIter[key]/N
        c = 0
        for key in self.currentIter:
            self.currentIter[key] += self.Ep
            c += self.currentIter[key]
        for key in self.currentIter:
            self.currentIter[key] = self.currentIter[key]/c

    def __clear(self):
        for key in self.currentIter.keys():
            self.currentIter[key] = 0.0

    def CalPR(self):
        self.__update()
        count = 1
        while not self.__converse():
            self.lastIter = copy.copy(self.currentIter)
            self.__clear()
            self.__update()
            count += 1
        print count

    def printPR(self):
        results = sorted(self.currentIter.items(), key=lambda d: d[1], reverse=True)
        print results
        # for key in self.graph:
            # print key, self.currentIter[key]


def main():
    # g = {1: [2, 4], 2: [4], 3: [4], 4: []}
    db = MongoClient().poky
    graph = {}
    for document in db.documents.find({"text": {"$exists": True}}):
        graph[document["_id"]] = document["links"]
    PR = PageRank(graph, 0.15)
    PR.CalPR()
    PR.printPR()

if __name__ == '__main__':
    main()
