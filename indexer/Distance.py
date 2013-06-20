__author__ = 'Administrator'
import math
from Parsing import Parser


def getFreqDict(string):
    dict = {}
    for item in string:
        if item not in dict:
            dict[item] = 0
        dict[item] += 1
    return dict


def Cosine(string1, string2):
    dict1 = getFreqDict(string1)
    dict2 = getFreqDict(string2)
    sum = 0
    for value in dict1.values():
        sum += (value*value)
    dis1 = math.sqrt(sum)
    sum = 0
    for value in dict2.values():
        sum += (value*value)
    dis2 = math.sqrt(sum)
    set1 = set(dict1.keys())
    set2 = set(dict2.keys())
    intersection = set1 & set2
    sum = 0
    for key in intersection:
        sum += (dict1[key] * dict2[key])
    return float(sum)/(dis1*dis2)
f = open("TestCose.txt")
s1 = f.readline()
s2 = f.readline()
s1 = s1.split('\n')[0]
s2 = s2.split('\n')[0]
p = Parser("SW3.txt")
list1 = p.getIndexToken(s1)
list2 = p.getIndexToken(s2)
print list1
print list2
print Cosine(list1, list2)
