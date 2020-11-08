#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# function 自动统计英语单词词频，带翻译
import re
import os
import sys
import time
import json
import urllib.request
import urllib.parse
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(300, 150)
    w.move(300, 300)
    w.setWindowTitle("英语词频统计")
    w.show()

    sys.exit(app.exec_())

file_library = "./file_library_txt"
txt_file_name = 'combine.txt'
result_file_name = 'result.txt'


def translate(word):
    """
    功能：寻有道词典翻译
        word:要翻译的内容，可以是单词，可以是中文
    """
    # 翻译地址
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {'i': word, 'doctype': 'json'}
    data = urllib.parse.urlencode(data).encode('utf-8')
    response = urllib.request.urlopen(url, data)
    html = response.read().decode('utf-8')
    target = json.loads(html)
    # 返回第一个翻译结果
    result = (target['translateResult'][0][0]['tgt'])
    return result


def find_txt(folder, ret):
    """
    功能：寻找指定文件夹下的所有txt文档路径
        folder:指定文件夹
        ret:保存txt文件路径的列表
    """
    file_list = os.listdir(folder)
    for filename in file_list:
        de_path = os.path.join(folder, filename)
        if os.path.isfile(de_path):
            if de_path.endswith(".txt"):
                ret.append(de_path)
        else:
            find_txt(de_path, ret)


def combine_txt(folder, combine_file_name):
    """
    功能：合并指定文件夹下的所有txt文件
        folder:指定文件夹
        combine_file_name:合并后的txt文件名
    """
    # 打开当前目录下的result.txt文件，如果没有则创建
    f = open(combine_file_name, 'w', encoding='utf-8')
    ret = []
    # 获取目标文件夹中的所有txt文件路径列表
    find_txt(folder, ret)
    for filepath in ret:
        # print(filepath)
        # 遍历单个txt文件，读取行数
        for line in open(filepath, encoding='utf-8'):
            f.writelines(line)
            f.write('\n')
    # 关闭文件
    f.close()


def gettext(file_name):
    """
        功能：获取txt文件内容,并将英语单词全部转换为小写字母
        file_name:txt文件名
    """
    txt = open(file_name, "r", errors='ignore', encoding='utf-8').read()
    txt = txt.lower()
    return txt


def stat_freq(file_name, min_len=2, max_len=20):
    """
    功能：统计txt文件中英文单词出现频率
        file_name:txt文件名
        min_len:单词最小长度，默认值2
        max_len:单词最大长度，默认值20
    """
    content = gettext(file_name)
    words = re.split(r'[^A-Za-z\'\-]+', content)
    new_words = []
    for word in words:
        word_len = len(word)
        if (word_len >= min_len) and (word_len <= max_len):
            new_words.append(word)
    total_word = len(new_words)
    counts = {}
    for word in new_words:
        counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda w: w[1], reverse=True)
    f = open(result_file_name, 'w', encoding='utf-8')
    f.writelines("{0:<6}\t{1:<20}\t{2:<20}\t{3:<6}\t{4:<5}\t{5:>5}".format
                 ("No",
                  "Word",
                  "Translate",
                  "Count",
                  "Freq",
                  "Cum_Freq"))
    f.write('\n')
    f.writelines("{0:<6}\t{1:<20}\t{2:<20}\t{3:<6}\t{4:<5}\t{5:>5}".format
                 (len(items),
                  "all_word",
                  "翻译",
                  total_word,
                  "100%",
                  "100%"))
    f.write('\n')
    f.writelines(
        "_____________________________________________"
        "_____________________________________________")
    f.write('\n')
    # 单词出现次数列表
    cnt = []
    # 单词累计出现次数列表
    cum_cnt = []
    # 单词累计出现次数
    cum_count = 0
    # 单词累计频率列表
    cum_fre = []
    for i in range(len(items)):
        word, count = items[i]
        cum_count = cum_count + count
        freq = count / total_word
        cum_freq = cum_count / total_word
        f.writelines("{0:<6}\t{1:<20}\t{2:<20}\t{3:<6}\t{4:.4%}\t{5:.4%}".format
                     (i + 1,
                      word,
                      # translate(word),
                      " ",
                      count,
                      freq,
                      cum_freq))
        f.write('\n')
        cnt.append(count)
        cum_cnt.append(cum_count)
        cum_fre.append(cum_freq*100)
    # 关闭文件
    f.close()

    print(cnt)
    cnt_len = len(cnt)
    # 绘制频率图
    plt.bar(list(range(1, cnt_len + 1)), cnt, align='center')
    plt.axis([1, cnt_len + 1, 1, cnt[cnt_len // 30]])
    plt.title('Word frequency')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.savefig('freq.png')
    plt.show()

    # 绘制累计频率图
    bins = range(0, 101, 5)
    plt.hist(cum_fre, bins=bins, rwidth=0.9)
    plt.title("Word cumulative frequency")
    plt.show()

    # 统计报告
    # 绘制累计频率图
    plt.hist(cnt, rwidth=0.9)
    plt.title("Word cumulative frequency")
    plt.show()

    result = dict()
    for a in set(cnt):
        result[a] = cnt.count(a)
    # print(result)
    key = []
    value = []
    for k in result:
        key.append(k)
        value.append(result[k])
    # plt.plot(key[5:-1], value[5:-1])
    # plt.show()


start = time.time()
# combine_txt(file_library, txt_file_name)
# stat_freq(txt_file_name)
end = time.time()
print("程序运行" + str(end-start) + "s")
