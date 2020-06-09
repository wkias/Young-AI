import os
import time
import json
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir
from jieba.analyse import ChineseAnalyzer


class se:
    def __init__(self, idxd=True, faqfile='faq.csv', indexdir='indexdir/'):
        # 创建schema, stored为True表示能够被检索
        self.schema = Schema(
            Q=TEXT(stored=True,
                   analyzer=ChineseAnalyzer()),
            A=TEXT(stored=True,
                   analyzer=ChineseAnalyzer()))
        # 存储schema信息至indexdir
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
        if idxd:
            self.idx = open_dir(indexdir)
        else:
            self.idx = create_in(indexdir, self.schema)
            self.index(faqfile)
        # 创建检索器
        self.searcher = self.idx.searcher()

    def index(self, faqfile):
        # csv
        with open(faqfile, 'r', encoding='utf-8') as f:
            self.texts = [_.strip().split(',')
                          for _ in f.readlines()
                          if len(_.strip().split(',')) == 2]
        # 按照schema定义信息，增加需要建立索引的文档
        self.writer = self.idx.writer()
        for i in range(1, len(self.texts)):
            q, a = self.texts[i]
            self.writer.add_document(Q=q, A=a)
        self.writer.commit()

    def search(self, factor):
        stime = time.time()
        results = self.searcher.find('Q', factor)
        duration = time.time()-stime
        return duration, results


if __name__ == "__main__":
    import pretty_errors

    def prt(duration, results, factor):
        print('在%fs内发现%d个结果：%s'
              % (duration, len(results), factor))
        for i in range(len(results)):
            print(json.dumps(results[i].fields(), ensure_ascii=False))

    test = se(idxd=False)
    # 测试时只需向列表中添加关键词
    factors = ['借书', '还书', '期限', '多久', '我真好看']
    for i in factors:
        d, r = test.search(i)
        prt(d, r, i)
