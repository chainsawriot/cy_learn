# -*- coding: utf-8 -*-
### Quick and dirty script to pull data from mep.gov.cn
### Answer to this question: https://www.facebook.com/groups/hkrusers/permalink/793249694038527

from bs4 import BeautifulSoup
import urllib2
import csv
import re
#import iconv_codecs

indexpage = "http://www.ceo.gov.hk/chi/press/press2012.html"
indexpage2013 = "http://www.ceo.gov.hk/chi/press/press2013.html"

def url2soup(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    htmldata = urllib2.urlopen(req).read()
    htmldatasoup = BeautifulSoup(htmldata)
    return htmldatasoup

allprlink = url2soup(indexpage).find_all("li")
allprlink2013 = url2soup(indexpage2013).find_all("li")


def bfurl2soup(url):
    os.system("wget %s" % url)
    fname = re.findall("P[0-9]+\.htm", url)
    os.system("iconv -c -f big5 -t utf8 %s -o %s" % (fname[0], fname[0] + ".utf8"))
    readback = open(fname[0] + ".utf8", "r")
    data = readback.read()
    readback.close()
    htmldatasoup = BeautifulSoup(data)
    return htmldatasoup
    

def extractpr(liitem):
    title = liitem.get_text()
    date = re.findall("[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}", title)[0]
    pr_url = liitem.a['href']
    prsoup = bfurl2soup(pr_url)
    prraw = prsoup.find_all(id = "pressrelease")[0].get_text()
    cleanpr = [x.lstrip() for x in re.sub("\\t|\\r", "", prraw).split("\n") if x != '']
    for x in cleanpr[2:len(cleanpr)-2]:
        print x
    #print endindex
    #print startindex
    return {"title": title, "date": date, "pr_url": pr_url, "prraw": prraw, "cleantxt": cleanpr[2:len(cleanpr)-2]}

pr2012 = [extractpr(liitem) for liitem in allprlink]
pr2013 = [extractpr(liitem) for liitem in allprlink2013]

import pickle
pickle.dump(pr2012, open("pr2012.p", "wb"))
pickle.dump(pr2013, open("pr2013.p", "wb"))


# def checkGoodtr(tr):
#     return tr.td['class'][0] == 'report1_2'

# def extractTr(tr):
#     alltd = tr.find_all("td")
#     res = {}
#     res['serial'] = alltd[0].get_text()
#     res['city'] = alltd[1].get_text()
#     res['date'] = alltd[2].get_text()
#     res['pollIndex'] = alltd[3].get_text()
#     res['major'] = alltd[4].get_text()
#     res['pollClass'] = alltd[5].get_text()
#     res['pollCondition'] = alltd[6].get_text()
#     return res

# extracted_data = [extractTr(tr) for tr in alltr if checkGoodtr(tr)]

# def export_csv(extracted_data, csvfilename):
#     keys = extracted_data[0].keys()
#     f = open(csvfilename, "wb")
#     csvwriter = csv.writer(f)
#     csvwriter.writerow(keys)
#     for row in extracted_data:
#         csvwriter.writerow([row[k].encode('utf-8') for k in row])

# export_csv(extracted_data, "testing.csv")

# ### file the max page from this firstpage

# def seekMaxPage(alltr):
#     for tr in alltr:
#         alltd = tr.find_all('td')
#         for td in alltd:
#             if td['class'][0] == 'report1_12':
#                 return [font.get_text() for font in td.find_all("font")]

# seekMaxPage(alltr) ## second item is the max page


### ecap the whole thing into a function
### change the pagenum in the url from 1 to range of 2 to maxPage seek by seekMaxPage
### lather, rinse, repeat. But remember to add some try excepts...

### acknowledge me in your paper, perhaps?

### Chung-hong Chan, PhD Student, JMSC, HKU
### Fuk Chan, a.k.a. Chainsaw Riot, HKRUG
