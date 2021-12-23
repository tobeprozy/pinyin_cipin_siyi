from openpyxl import load_workbook
from openpyxl import Workbook
import json
import sys
from urllib.parse import urlparse, quote, urlencode, unquote
from urllib.request import urlopen
import re
import time
import pypinyin
import xlrd # 导入xlrd库
import xlwt # 导入xlrd库
from translate import Translator

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

def main1():
    tplt = "{0:^2}\t{1:^10}\t{2:^10}\t{3:^15}"
    strlist=["汉语","数学","文学","阿姨","爱好","爱心","安静","运动","提高"]
    print(tplt.format("序号", "汉语", "拼音","英语"))
    for index, hanzi in enumerate(strlist):
        trans=parse(fetch(hanzi))
        pinyin=yinjie(hanzi)
        # print(str(index)+'\t',end="")
        # print(hanzi+'\t',end="")
        # print(pinyin+'\t',end="")
        # print(trans)
        print(tplt.format(index+1, hanzi, pinyin, trans))
    # parse(fetch(str("生命")));
    # print("有音调：" + yinjie("我叫张志远"))
    # print("translate：")

def main2():

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
    main2();