#!/usr/bin/env python3
import bs4
import urllib.request
import jieba_fast
import json
import xlwt
import xlrd
import os
import xlutils.copy
import wordcloud
import matplotlib.pyplot


def getAll(soup):
    content = ''
    bs = bs4.BeautifulSoup(soup)
    clist = bs.find("div", {"class": "zhj-bbqw"}).find_all("p", {"style": "text-indent: 2em; font-family: 宋体; font-size: 12pt;"})
    for a in clist:
        content = content + '\n' + "  " + a.get_text()
    textSplit(content)
    saveText(content, "政府工作报告全文")


def getQuickLook(soup):
    pass


def getInterpretation(soup):
    dic = {}
    bs = bs4.BeautifulSoup(soup).find_all("ul", {"class": "o zhj-bbjd"})[0]
    clist = bs.find_all("a")
    for a in clist:
        dic[a.get_text()] = a["href"]
    saveJson(dic, "报告解读")
    saveSheet(dic, "报告解读")


def getDiscussion(soup):
    dic = {}
    bs = bs4.BeautifulSoup(soup).find_all("ul", {"class": "o zhj-bbjd"})[1]
    clist = bs.find_all("a")
    for a in clist:
        dic[a.get_text()] = a["href"]
    saveJson(dic, "代表委员议")
    saveSheet(dic, "代表委员议")


def getReserved(soup):
    dic = {}
    bs = bs4.BeautifulSoup(soup).find_all("ul", {"class": "o zhj-bbjd"})[2]
    clist = bs.find_all("a")
    for a in clist:
        dic[a.get_text()] = a["href"]
    saveJson(dic, "创意产品")
    saveSheet(dic, "创意产品")


def wordCloud(splitedText):
    wc = wordcloud.WordCloud(font_path=fontPath, background_color="white", max_font_size=200, max_words=2000, width=3840, height=2160).generate(splitedText)
    matplotlib.pyplot.figure()
    matplotlib.pyplot.imshow(wc)
    matplotlib.pyplot.axis("off")
    matplotlib.pyplot.show()
    wc.to_file(path + "词云.jpg")


def textSplit(content):
    dic = {}
    splitedText = ""
    seqlist = jieba_fast.cut(content)
    for word in seqlist:
        splitedText = splitedText + word + " "
        if word not in dic:
            dic[word] = 1
        else:
            dic[word] += 1
    wordCloud(splitedText)
    saveJson(dic, "报告全文")
    saveSheet(dic, "报告全文")
    # sortedDic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    # saveJson(sortedDic)     # Sort value and save


def saveJson(dic, fileName):
    with open(path + fileName + ".json", "w", encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False)


def saveText(content, fileName):
    with open(path + fileName + ".txt", "w", encoding="utf-8") as f:
        f.write(content)


def saveSheet(dic, sheetName):
    if(os.path.isfile(path+xlsName)):
        oldBook = xlrd.open_workbook(path + xlsName)
        book = xlutils.copy.copy(oldBook)
    else:
        book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet(sheetName)
    i = 0
    for key in dic:
        sheet.write(i, 0, key)
        sheet.write(i, 1, dic[key])
        i += 1
    book.save(path + xlsName)


fontPath = "C:\Windows\Fonts\msyh.ttf"
path = "."
xlsName = "2019 政府工作报告.xls"
url = "http://www.gov.cn/zhuanti/2019qglh/2019lhzfgzbg/index.htm"
html = urllib.request.urlopen(url)
soup = str(bs4.BeautifulSoup(html).find("div", {"class": "zhj-report-right fr bd"}))
getAll(soup)
getQuickLook(soup)
getInterpretation(soup)
getDiscussion(soup)
getReserved(soup)
