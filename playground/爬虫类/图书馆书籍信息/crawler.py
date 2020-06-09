import pysnooper
import pretty_errors
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
import json
import time


def detail(link):
    soup = bs(requests.get(link).text, features='html.parser')
    info_keys = [i.string[:-1] for i in soup.find_all('dt')[:-2]]
    info_values = [i.get_text() for i in soup.find_all('dd')[:-2]]
    info = {}
    for k, v in zip(info_keys, info_values):
        info[k] = v
    coll_keys = [i.string for i in soup.find('tr').find_all('td')]
    tag_td = [i.get_text() for i in soup.find_all('td')[6:-19]]
    coll = {}
    for i in range(int(len(tag_td)/len(coll_keys))):
        for k in range(len(coll_keys)):
            coll[coll_keys[k]] = tag_td[i*len(coll_keys)+k]
        info['collection'+str(i)] = coll.copy()
    return info


# @pysnooper.snoop()
def lookup(keyword, elaborate=False):
    meta_url = 'http://210-44-1-3-8080-p.vpn.sdnu.edu.cn'
    rss_url = meta_url + '/opac/search_rss.php?title=' + keyword
    books = []
    root = ET.fromstring(requests.get(rss_url).text)
    items = root.find('channel').findall('item')
    for item in items:
        books.append([
            item.find('title').text,
            item.find('link').text,
            item.find('description').text
        ])
        if(elaborate):
            books[-1].append(detail(books[-1][1]))
    return books


if __name__ == "__main__":
    title = ''
    print('keyword\t\t\t', title)

    stime = time.time()
    string = lookup(title)
    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(string, f, ensure_ascii=False)
    print("获取简略信息耗时\t" + str(time.time() - stime))

    stime = time.time()
    string = lookup(title, True)
    with open('books_elaborate.json', 'w', encoding='utf-8') as f:
        json.dump(string, f, ensure_ascii=False)
    print("获取详尽信息耗时\t" + str(time.time() - stime))
