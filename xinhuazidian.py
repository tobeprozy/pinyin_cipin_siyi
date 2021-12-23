#!/usr/bin/python
# encoding:utf-8

from urllib.parse import urlparse, quote, urlencode, unquote
from urllib.request import urlopen

import time
import pypinyin
import xlrd # 导入xlrd库
import xlwt # 导入xlrd库



import json
import urllib.request,urllib,urllib.error,urllib.parse

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
# 1、新华字典查询
def cidian(word):
    data = {}
    data["appkey"] = "6f368d6e368ae582"
    data["word"] = word
    num=len(word)
    print(num)
    url_values = urllib.parse.urlencode(data)
    if len(word)==1:
        url = "https://api.jisuapi.com/zidian/word" + "?" + url_values
    else:
        url = "https://api.jisuapi.com/cidian/word" + "?" + url_values

    print(url)
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request)
    jsonarr = json.loads(result.read())

    result = jsonarr["result"]
    strr = ""


    if num == 1:
        for val in result["explain"]:
            strr=result["name"]+"念"+val["pinyin"]+":"+val["content"]+strr;
            print(strr)
        return strr, num
    else:
        print(result["content"])  # 写入excel，i行0列
        print(result["example"])  # 写入excel，i行0列
        return result,num

import urllib.request as ur
import urllib.parse as up
from  lxml import etree

def openUrl(url='http://dict.baidu.com/s?wd=apple'):
    request = ur.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0')
    response = ur.urlopen(request)
    html = response.read()
    return html

def getMeaning(word):
    # 根据单词生成百度汉语url
    url = 'http://dict.baidu.com/s?wd=' + up.quote(word.replace(' ', '+'))  # 使用quote将中文转码
    # print(url)
    url = url.replace('%2B', '+')
    html = openUrl(url).decode('utf-8',errors='ignore')
    # print(html)
    html=etree.HTML(html)
    # print(html)
    #提取释义
    area=html.xpath('//div[@class="tab-content"]/dl/dd/p/text()')
    return area



def find_baidu(word):
    meanings = getMeaning(word)
    print(meanings)
    if len(meanings) != 0:
        print('释义:')
        str_dict=''
        for meaning in meanings:
            str_dict=str_dict+''.join(meaning.split())
            print(str_dict)
        return str_dict
    else:
        str_dict = '';
        print('没有释义!')
        return  str_dict;

def main():
    # 读取文件
    readbook = xlrd.open_workbook('select.xlsx')
    sheetr = readbook.sheet_by_index(0)  # 索引的方式，从0开始
    nrows = sheetr.nrows  # 行
    ncols = sheetr.ncols  # 列

    # 写入文件
    writebook = xlwt.Workbook('math1210.xls')  # 打开一个excel
    sheetx = writebook.add_sheet('math1210')  # 在打开的excel中添加一个sheet
    sheetx.write(0, 0, "序号")  # 写入excel，0行0列
    sheetx.write(0, 1, "汉语")
    sheetx.write(0, 2, "拼音")  # 写入excel，0行2列
    sheetx.write(0, 3, "英语")
    sheetx.write(0, 4, "中文释义")


    tplt = "{0:^2}\t{1:^10}\t{2:^10}\t{3:^15}\t{4:^15}"
    print(tplt.format("序号", "汉语", "拼音", "英语", "中文释义"))

    num = 1
    for i in range(ncols):
        coldate = sheetr.col_values(i)  # i行的list
        length = len(coldate)
        for index, hanzi in enumerate(coldate):
            trans = parse(fetch(hanzi), sheetx, num)
            pinyin = yinjie(hanzi)
            sheetx.write(num, 0, num)  # 写入excel，i行0列
            sheetx.write(num, 1, hanzi)
            sheetx.write(num, 2, pinyin)  # 写入excel，i行0列
            # 3在另一个函数内
            zhongwen=find_baidu(hanzi)
            sheetx.write(num, 4, zhongwen)  # 写入excel，i行0列
            # print(num,a,hanzi)#第i行，a列，数据b
            print(tplt.format(num, hanzi, pinyin, trans, zhongwen))
            num = num + 1
            if (num % 20) == 0:
                print(num)
                writebook.save('math1210.xls')  # 一定要记得保存
        writebook.save('math1210.xls')  # 一定要记得保存
if __name__ == "__main__":
    main();