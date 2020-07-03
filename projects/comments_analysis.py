#!/usr/bin/python3
# encoding=utf-8

"""分析马蜂窝景点中爬取的评论内容，计算情感概率并进行词频计算脚本。

使用snowNLP训练好的模型计算评论情感概率。
使用jieba分词（paddle训练模型）计算词频。
结果输出在原目录的json中，并导出词云。

Args:
    FILE_PATH: 所有评论的文件夹路径
    STOPWORDS_FILE_PATH: 停用词路径

"""

import json
import os
import re

import jieba
import jieba.analyse
import numpy
import pandas as pd
import wordcloud
from snownlp import SnowNLP


# 查询目录下非隐藏文档名
def _listdir_no_hidden(file_path):
    # Args:
    #   file_path: 查询的目录

    # Return：
    #   返回generator生成器对象，其中包含非隐藏的文档名称.

    for dir_obj in os.listdir(file_path):
        if not dir_obj.startswith('.'):
            yield dir_obj


# 创建停用词列表
def _get_stopwords_list(file_path):
    # Args:
    #   file_path: stopwords地址

    # Return：
    #   一个list对象，其中包含每一个停止词

    stopwords = [line.strip() for line in open(file_path, encoding='UTF-8').readlines()]
    stopwords.extend(['', ' ', '~', '…'])
    stopwords = tuple(stopwords)
    return stopwords


# 语句情感分析函数
def _analysis_comments(texts):
    # Args:
    #   texts: 包含一串语句的list

    # Return：
    #   一个list对象，其中包含每一个语句对应的情感概率

    texts_prob = []
    for text in texts:
        content = text.replace(u'\xa0', u' ')
        result = SnowNLP(content)
        texts_prob.append(result.sentiments)
    return texts_prob


# 计算每个景点情感倾向
def _cal_emotion_probs(good_comments, normal_comments, bad_comments, count_summary):
    # Args:
    #   good_comments: 分类为好评的一组评论list
    #   normal_comments: 分类为中评的一组评论list
    #   bad_comments: 分类为差评的一组评论list
    #   count_summary: 一个包含景点所有评论的统计数据

    # Return：
    #   一个浮点数，表示该景点总体评论情感概率

    # 获取评论计数
    total_opinion_count = int(count_summary['总评论数'])
    good_opinion_count = int(re.findall(r'\d+', count_summary['好评'])[0])
    normal_opinion_count = int(re.findall(r'\d+', count_summary['中评'])[0])
    bad_opinion_count = int(re.findall(r'\d+', count_summary['差评'])[0])
    # 情感分析
    if len(good_comments) != 0:
        good_comments_prob = _analysis_comments(good_comments)
        good_comment_prob_avg = numpy.average(good_comments_prob)
    else:
        good_comment_prob_avg = 0
    if len(normal_comments) != 0:
        normal_comments_prob = _analysis_comments(normal_comments)
        normal_comment_prob_avg = numpy.average(normal_comments_prob)
    else:
        normal_comment_prob_avg = 0
    if len(bad_comments) != 0:
        bad_comments_prob = _analysis_comments(bad_comments)
        bad_comment_prob_avg = numpy.average(bad_comments_prob)
    else:
        bad_comment_prob_avg = 0
    # 计算公式
    total_comment_prob = good_comment_prob_avg * (
        good_opinion_count / total_opinion_count) + normal_comment_prob_avg * (
            normal_opinion_count / total_opinion_count) + bad_comment_prob_avg * (
                bad_opinion_count / total_opinion_count)
    return total_comment_prob


# 计算所给文本的词频
def cal_words_freq(texts, stopwords):
    """对给出的文本list进行分词

    使用PaddlePaddle序列标注（双向GRU）网络模型标注分词

    Args:
       texts: 一组评论list
       stopwords: 停止词的list

    Return：
       一个字典对象，key为词，value为频率

    """

    segments = {}
    jieba.enable_paddle()  # 激活paddle训练模型
    for text in texts:
        words = jieba.cut(text, use_paddle=True)
        for word in words:
            # 停用词判断，如果当前的关键词不在停用词库中才进行记录
            if word not in stopwords:
                # 记录全局分词
                if word in segments:  # 直接判断key在不在字典中
                    segments[word] += 1
                else:
                    segments[word] = 1
    segments_order = dict(sorted(segments.items(), key=lambda x: x[1], reverse=True))
    return segments_order


# 主要函数
def texts_analysis(comments_file_path, stopwords_file_path):
    """分析马蜂窝景点中爬取的评论内容，计算情感概率并进行词频计算。

    使用snowNLP训练好的模型计算评论情感概率。
    使用jieba分词（paddle训练模型）计算词频。
    结果输出在原目录的json中，并导出词云。

    Args:
        comments_file_path: 所有评论的文件夹路径
        stopwords_file_path: 停用词文件路径

    输出:
        在comments_file_path目录中创建comments analysis.json文件，json包含整体情感概率和词频数据；
        同时生成comments wordcloud.png词云图。

    """

    locations = _listdir_no_hidden(comments_file_path)
    for location in locations:
        # 构造文件路径
        print(location)
        location_file_path = comments_file_path + '/' + location
        landmarks = os.listdir(location_file_path)
        for landmark in landmarks:
            landmark_file_path = location_file_path + '/' + landmark
            # 读取json文件
            json_file_path = landmark_file_path + '/' + landmark + '各类评论数统计.json'
            with open(json_file_path, 'r', encoding='gbk') as json_file:
                count_summary = json.load(json_file)
            # 评论内容读取
            comments = []
            try:
                good_comments = pd.read_csv(landmark_file_path + '/好评.CSV', index_col=0)
                good_comments = good_comments["评论内容"]
                comments.extend(good_comments)
            except FileNotFoundError as file_no_find_msg:
                print(file_no_find_msg)
                good_comments = []
            try:
                normal_comments = pd.read_csv(landmark_file_path + '/中评.CSV', index_col=0)
                normal_comments = normal_comments["评论内容"]
                comments.extend(normal_comments)
            except FileNotFoundError as file_no_find_msg:
                print(file_no_find_msg)
                normal_comments = []
            try:
                bad_comments = pd.read_csv(landmark_file_path + '/差评.CSV', index_col=0)
                bad_comments = bad_comments["评论内容"]
                comments.extend(bad_comments)
            except FileNotFoundError as file_no_find_msg:
                print(file_no_find_msg)
                bad_comments = []
            landmark_prob = _cal_emotion_probs(
                good_comments, normal_comments, bad_comments, count_summary)
            # 词频计算
            stopwords = _get_stopwords_list(stopwords_file_path)
            landmark_words_freq = cal_words_freq(comments, stopwords)
            # 输出json
            json_data = {"emotional_prob": landmark_prob}
            json_data.update({"words_freq": landmark_words_freq})
            json_out = {"apiVersion": "1.0", "data": json_data}
            with open(landmark_file_path
                      + '/' + "comments analysis.json", "w", encoding='utf-8') as json_file:
                json_file.write(json.dumps(json_out, indent=4, ensure_ascii=False))
            # 输出词云
            landmark_wordcloud = wordcloud.WordCloud(scale=4, font_path="./SimHei.ttf",
                                                     background_color='white', max_words=50,
                                                     max_font_size=100, random_state=20,
                                                     width=300, height=300
                                                     ).generate_from_frequencies(
                                                         landmark_words_freq)
            landmark_wordcloud.to_file(landmark_file_path + '/' + "comments wordcloud.png")
            print(' ' + landmark + " 分析完成")


if __name__ == "__main__":
    # 获取路径
    FILE_PATH = '../docs/comments'
    STOPWORDS_FILE_PATH = os.path.dirname(
        os.path.abspath('.')) + '/projects/stopwords/stopwords.txt'
    texts_analysis(FILE_PATH, STOPWORDS_FILE_PATH)
