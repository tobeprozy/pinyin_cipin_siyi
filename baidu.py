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


#提取中文解释
# 请输入单词: 古代
# ['\n                    （名）①距离现代较远的过去时代，我国历史分期多指1840年以前的时期。②特指原始社会、奴隶社会时代。\n                                    ']
# 释义:
# （名）①距离现代较远的过去时代，我国历史分期多指1840年以前的时期。②特指原始社会、奴隶社会时代。
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
        # print('没有释义!')
        return False, "没有合适的释义!"


if __name__ == '__main__':
    while True:
        word = input('请输入单词: ')
        find_baidu(word)