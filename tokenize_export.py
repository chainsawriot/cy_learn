import jieba
import pickle

pr2012 = pickle.load(open("pr2012.p", "r"))
pr2013 = pickle.load(open("pr2013.p", "r"))

jieba.load_userdict("userdict.txt")

prall = pr2012 + pr2013

for i in prall:
    res = jieba.cut("".join(i['cleantxt']))
    i['tokenized'] = " ".join(res)

import csv

f = open("tokenized.csv", "wb")
csvwriter = csv.writer(f)
for i in prall:
    csvwriter.writerow([i['date'].encode("utf-8"), i['tokenized'].encode('utf-8')])
f.close()
