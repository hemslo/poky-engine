# coding=utf-8
from Parsing import Parser
import math
import codecs
from pymongo import MongoClient


# class PostingNode(object):

#     def __init__(self, TF):
#         self.TF = TF

#     def __str__(self):
#         return str(self.TF)


class DocumentReverseList(object):
    def __init__(self, list, DocumentID):
        self.documentID = DocumentID
        self.reverseList = list


class InverseTable(object):
    def __init__(self, table={}):
        self.table = table
        self.DocID = []

    def merge(self, DRL):
        if DRL.documentID not in self.DocID:
            self.DocID.append(DRL.documentID)
        for key in DRL.reverseList:
            if key not in self.table:
                self.table[key] = {}
                self.table[key]["df"] = 0
                self.table[key]["posting"] = {}
            if DRL.documentID not in self.table[key]:
                self.table[key]["posting"][DRL.documentID] = DRL.reverseList[key]
                self.table[key]["df"] += 1
            else:
                self.table[key]["posting"][DRL.documentID] += DRL.reverseList[key]

    def CalIDF(self):
        for value in self.table.values():
            value["idf"] = math.log(len(self.DocID)/float(value["df"]))

    def CalNormalizingPara(self):
        self.CalIDF()
        self.Normalization = {}
        for item in self.DocID:
            self.Normalization[item] = 0
        for key in self.table:
            for DocumentID in self.table[key]["posting"]:
                tf_idf = math.log(float(1+self.table[key]["posting"][DocumentID])) * self.table[key]["idf"]
                self.Normalization[DocumentID] += tf_idf ** 2
        for key in self.Normalization:
            self.Normalization[key] = math.sqrt(self.Normalization[key])

    def printRT(self):
        w = codecs.open("result.txt", "w", "utf-8")
        for key in self.table:
            try:
                w.write(key+" : "+str(self.table[key])+'\n')
            except:
                pass
        w.close()
        w = open("Normalization.txt", "w")
        for key in self.Normalization:
            w.write(str(key) + " : " + str(self.Normalization[key]) + '\n')
        w.close()


def main():
    db = MongoClient().poky
    inverse_table = InverseTable()
    parser = Parser("Stopword.txt")
    for document in db.documents.find({"text": {"$exists": True}}):
        for textlist in document[u'text'].values():
            for text in textlist:
                DRL = DocumentReverseList(parser.getIndexToken(text), document[u'_id'])
                inverse_table.merge(DRL)
    inverse_table.CalNormalizingPara()
    # inverse_table.printRT()

    # for key in inverse_table.table:
    #     term = {}
    #     term['word'] = key
    #     term['df'] = inverse_table.table[key]['df']
    #     term['idf'] = inverse_table.table[key]['idf']
    #     term['posting'] = [{'doc_id': id,
    #                         'tf': inverse_table.table[key]['posting'][id]
    #                         } for id in inverse_table.table[key]['posting']]
    #     db.terms.save(term)

    for key in inverse_table.Normalization:
        document = db.documents.find_one({"_id": key})
        document["normalization"] = inverse_table.Normalization[key]
        db.documents.save(document)


if __name__ == '__main__':
    main()
