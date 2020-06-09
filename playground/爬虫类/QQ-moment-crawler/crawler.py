import csv
import requests
import selenium.webdriver
import time
import os
import re
import xlwt
import json


header = {
    'Host': 'h5.qzone.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://user.qzone.qq.com/',
    'Connection': 'keep-alive'
}


def webLogin():
    driver = selenium.webdriver.Chrome('Z:\\chromedriver.exe')
    Url = "https://qzone.qq.com/"
    driver.get(Url)
    time.sleep(3)
    cookie = {}
    for element in driver.get_cookies():
        cookie[element['name']] = element['value']
    html = driver.page_source
    g_qzonetoken = re.search(
        r'window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)', html)
    g_tk = get_g_tk(cookie)
    driver.quit()
    print(g_qzonetoken.group(1))
    return (cookie, g_tk, g_qzonetoken.group(1))


def get_g_tk(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)  # ord()用来返回字符ascii码
    return hashes & 0x7fffffff


# friends = {'sun': '1466771495'}
friends = {}
csvSheet = csv.reader(open('Z:\\QQmail.csv'))
for row in csvSheet:
    friends[row[0]] = row[2][:-7]
friends.pop('姓名')
session = requests.session()
cookie, g_tk, g_qzonetoken = webLogin()
book = xlwt.Workbook()
try:
    os.mkdir('QQ Zone')
except FileExistsError as FEE:
    print(FEE)
for friend in friends:
    n = 1
    sheet = book.add_sheet(friend, cell_overwrite_ok=True)
    sheet.write(0, 0, "号码")
    sheet.write(0, 1, "日期")
    sheet.write(0, 2, "时间")
    sheet.write(0, 3, "年份")
    sheet.write(0, 4, "月份")
    sheet.write(0, 5, "时间点")
    sheet.write(0, 6, "图片数量")
    sheet.write(0, 7, "评论数量")
    sheet.write(0, 8, "手机型号")
    sheet.write(0, 9, "经度")
    sheet.write(0, 10, "地点")
    sheet.write(0, 11, "纬度")
    sheet.write(0, 12, "位置")
    sheet.write(0, 13, "内容")
    for i in range(2000):
        pos = i*20
        param = {
            'uin': friends[friend],
            'ftype': '0',
            'sort': '0',
            'pos': pos,
            'num': '20',
            'replynum': '100',
            'g_tk': g_tk,
            'callback': '_preloadCallback',
            'code_version': '1',
            'format': 'jsonp',
            'need_private_comment': '1',
            'qzonetoken': g_qzonetoken
        }
        respond = session.get("https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
                              params=param, headers=header, cookies=cookie)
        strr = respond.text.encode('utf-8')
        with open('.\\QQ Zone\\'+friend+'.json', 'a+b') as jsonFile:
            try:
                jsonFile.write(strr)
            except:
                jsonFile.write(strr)
        # print(respond.text)
        r = re.sub("_preloadCallback", "", respond.text)
        test = r[1:-2]
        Data = json.loads(test)
        if not re.search('lbs', test):  # 通过lbs判断此qq是否爬取完毕
            print(friend+':'+friends[friend]+'\tOK')
            break
        try:
            for eachData in Data["msglist"]:
                # QQ号码
                sheet.write(n, 0, friends[friend])
                # 发表日期1
                sheet.write(n, 1, eachData["createTime"])
                # 发表时间2
                sheet.write(n, 2, time.strftime(
                    "%H:%M:%S", time.localtime(eachData["created_time"])))
                # 发表年份3
                sheet.write(n, 3, time.strftime(
                    "%Y", time.localtime(eachData["created_time"])))
                # 发表月份4
                sheet.write(n, 4, time.strftime(
                    "%m", time.localtime(eachData["created_time"])))
                # 发表小时5
                sheet.write(n, 5, time.strftime(
                    "%H", time.localtime(eachData["created_time"])))
                # 统计图片数量6，以及用手机型号8
                if "pic" in eachData:
                    sheet.write(n, 6, eachData["pictotal"])
                    sheet.write(n, 8, eachData["source_name"])
                else:
                    sheet.write(n, 6, 0)
                    sheet.write(n, 8, "")
                # 统计每个评论数量7
                if eachData["commentlist"]:
                    sheet.write(n, 7, eachData["commentlist"][-1]["tid"])
                else:
                    sheet.write(n, 7, 0)

                # 获取该条发表位置：9,10,11,12
                if "story_info" in eachData:
                    sheet.write(
                        n, 9, eachData["story_info"]["lbs"]["pos_x"])
                    sheet.write(
                        n, 11, eachData["story_info"]["lbs"]["name"])
                    sheet.write(
                        n, 10, eachData["story_info"]["lbs"]["pos_y"])
                    sheet.write(
                        n, 12, eachData["story_info"]["lbs"]["idname"])
                else:
                    sheet.write(n, 9, "")
                    sheet.write(n, 11, "")
                    sheet.write(n, 10, "")
                    sheet.write(n, 12, "")

                # 获取每一条内容13
                if eachData["content"]:
                    sheet.write(n, 13, eachData["conlist"][0]["con"])
                else:
                    sheet.write(n, 13, "")
                n = n + 1
        except:
            sheet.write(16, 0, "Error")
            print(friend+':'+friends[friend]+"\tERROR")
book.save("QQFriends-Moments.xls")
