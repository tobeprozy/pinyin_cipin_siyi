import jieba
import re
from collections import Counter

import json
import sys
from urllib.parse import urlparse, quote, urlencode, unquote
from urllib.request import urlopen
import re
import time
import pypinyin
import xlrd # 导入xlrd库
import xlwt # 导入xlrd库
import jieba.posseg as pseg
def cipin():
    content = ""
    filename = r"qh.txt";
    result = "result.txt"
    r = '[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;：。？、 ~@#￥%……&*（）]+'
    with open(filename, 'r', encoding='utf-8') as fr:

        content = re.sub(r, " ", fr.read())
        # re.sub(pattern, repl, string, count=0, flags=0)
        # pattern：表示正则表达式中的模式字符串；
        # repl：被替换的字符串（既可以是字符串，也可以是函数）；
        # string：要被处理的，要被替换的字符串；
        # count：匹配的次数, 默认是全部替换
        # flags：具体用处不详
        data = jieba.cut(content, cut_all=False)

    data = dict(Counter(data))  # dict() 函数用于创建一个字典。Counter 是实现的 dict 的一个子类，可以用来方便地计数。
    datasorted = sorted(data.items(), key=lambda x: x[1], reverse=True)
    datasorted=dict(datasorted)


    #print(wordssorted)
    # 写入文件
    writebook = xlwt.Workbook('computer_xx.xls')  # 打开一个excel
    sheetx = writebook.add_sheet('test')  # 在打开的excel中添加一个sheet
    sheetx.write(0, 0, "序号")  # 写入excel，0行0列
    sheetx.write(0, 1, "汉语")
    sheetx.write(0, 2, "词性")
    sheetx.write(0, 3, "词频")  # 写入excel，0行2列
    num=1;


    cixindict={"n":"普通名词",
               "nr" :"人名",
               "nz":"其它专名",
               "a":"形容词",
               "m":"数量词",
               "c":"连词",
               "PER":"人名",
               "f":"方位名词",
                "ns": "地名",
                "v": "普通动词",
                "ad": "副形词",
                "q":"量词",
                "u":"助词",
                "LOC":"地名",
                "s":"处所名词",
                "nt": "机构名",
                "vd": "动副词",
                "an": "名形词",
                "r":"代词",
                "xc":"其他虚词",
                "ORG":"机构名",
                "t":"时间",
                "nw": "作品名",
                "vn": "名动词",
                "d": "副词",
                "p":"介词",
                "w":"标点符号",
                "TIME":"时间",
                "b":"区别词"
               }

    for hanzi, cishu in datasorted.items():
        if (len(hanzi) > 1):
            sheetx.write(num, 0, num)  # 写入excel，0行0列
            sheetx.write(num, 1, hanzi)  # 写入excel，0行0列
            words = pseg.cut(hanzi)
            cixin = (list(map(lambda x: list(x), words)))
            sheetx.write(num, 2, cixin[0][1])  # 写入excel，0行0列
            sheetx.write(num, 3, cishu)  # 写入excel，0行0列
            num=num+1;
        if (num % 100) == 0:
            print(num)
            writebook.save('computer_xx.xls')  # 一定要记得保存


# 带声调的(默认)
def yinjie(word):
    s = ''
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, heteronym=False):
        s = s + ''.join(i) + ""
    return s


def fetch(query_str):
    query = {"q": "".join(query_str)}  # list --> str: "".join(list)
    # print(query)
    url = 'https://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&' + urlencode(query)
    time.sleep(3)
    response = urlopen(url, timeout=3)
    html = response.read().decode('utf-8')
    return html

def parse(html,sheetx,num):
    d = json.loads(html)
    try:
            if d.get('errorCode') == 0:
                explains = d.get('basic').get('explains')
                result = str(explains).replace('\'', "").replace('[', "").replace(']', "")  # .replace真好用~
                sheetx.write(num, 3, result);
                return result
            else:
                print('无法翻译!****')
                sheetx.write(num, 3, "无法翻译!")
                return " "
    except:
            print('****翻译出错!')  # 若无法翻译，则空出来
            sheetx.write(num, 3, "无法翻译!");
            return " "

def fanyi():

    #读取文件
    readbook = xlrd.open_workbook('computer.xlsx')
    sheetr = readbook.sheet_by_index(0)#索引的方式，从0开始
    nrows = sheetr.nrows  # 行
    ncols = sheetr.ncols  # 列

    # 写入文件
    writebook = xlwt.Workbook('computer_1.xls')  # 打开一个excel
    sheetx = writebook.add_sheet('test')  # 在打开的excel中添加一个sheet
    sheetx.write(0, 0, "序号")  # 写入excel，0行0列
    sheetx.write(0, 1, "汉语")
    sheetx.write(0, 2, "拼音")  # 写入excel，0行2列
    sheetx.write(0, 3, "英语")

    tplt = "{0:^2}\t{1:^10}\t{2:^10}\t{3:^15}"
    print(tplt.format("序号", "汉语", "拼音", "英语"))

    num=1
    for i in range(ncols):
            coldate = sheetr.col_values(i)#i行的list
            length=len(coldate)
            for index,hanzi in enumerate(coldate):
                trans=parse(fetch(hanzi),sheetx,num)
                pinyin = yinjie(hanzi)
                sheetx.write(num, 0, num)     # 写入excel，i行0列
                sheetx.write(num, 1, hanzi)
                sheetx.write(num,2, pinyin) # 写入excel，i行0列
                #print(num,a,hanzi)#第i行，a列，数据b
                print(tplt.format(num, hanzi, pinyin, trans))
                num=num+1
                if (num%20)==0:
                    print(num)
                    writebook.save('computer_1.xls')  # 一定要记得保存


if __name__ == "__main__":
    cipin();