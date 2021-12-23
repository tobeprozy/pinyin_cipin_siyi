import pypinyin
from translate import Translator
# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

# 带声调的(默认)
def yinjie(word):
    s = ''
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, heteronym=True):
        s = s + ''.join(i) + " "
    return s

#if __name__ == "__main__":
    translator=Translator(from_lang='chinese',to_lang='english')
    result=translator.translate("生命")
    print("张启辉同学，你好")
    #print("无音调："+pinyin("张启辉同学，你好呀"))
    print("有音调：" + yinjie("张启辉同学，你好！"))
    print("translate：" + result)

    result = translator.translate("我叫张志远")
    print("我叫张志远")
   # print("无音调：" + pinyin("我叫张志远"))
    print("有音调：" + yinjie("我叫张志远"))
    print("translate：" + result)


