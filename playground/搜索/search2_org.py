import os
from whoosh.index import create_in
from jieba.analyse import ChineseAnalyzer
import json
from whoosh.fields import *


class search_3:
    def search_fx3():
        # 创建schema, stored为True表示能够被检索
        schema = Schema(问题=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                        回答=TEXT(stored=True, analyzer=ChineseAnalyzer())
                        )

        # 解析poem.csv文件
        with open('faq.csv', 'r', encoding='utf-8') as f:
            texts = [_.strip().split(',')
                     for _ in f.readlines() if len(_.strip().split(',')) == 4]

        # 存储schema信息至indexdir目录
        indexdir = 'indexdir/'
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
        ix = create_in(indexdir, schema)

        # 按照schema定义信息，增加需要建立索引的文档
        writer = ix.writer()
        for i in range(1, len(texts)):
            问题, 回答 = texts[i]
            writer.add_document(问题=问题, 回答=回答)
        writer.commit()

        # 创建一个检索器
        searcher = ix.searcher()

        # find = input("请输入检索内容：")
        results = searcher.find("问题", "还书")
        print('一共发现%d个回答。' % len(results))
        for i in range(min(10, len(results))):
            print(json.dumps(results[i].fields(), ensure_ascii=False))


point3 = search_3
point3.search_fx3()
