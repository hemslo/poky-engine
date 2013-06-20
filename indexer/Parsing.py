# coding=utf-8
import jieba
from stemming.porter2 import stem


class Parser(object):

    def __init__(self, stopWordFile):
        StopWord = open(stopWordFile)
        SW = eval(StopWord.readline())
        utf_8_sw = set()
        for item in SW:
            utf_8_sw.add(item.decode("utf-8"))
        StopWord.close()
        self.StopWord = utf_8_sw

    def getIndexToken(self, paragraph):
        Index = {}
        if not paragraph:
            return Index
        if paragraph[-1] == '\n':
            paragraph = paragraph[0:len(paragraph)-1]
        seg_list = jieba.cut_for_search(paragraph)
        for item in seg_list:
            item = item.lower()
            try:
                int(item)
                continue
            except:
                if item not in self.StopWord:
                    item = stem(item)
                    if item in Index:
                        Index[item] += 1
                    else:
                        Index[item] = 1
        return Index
