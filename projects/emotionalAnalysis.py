#!/usr/bin/env python
# encoding=utf-8
import json
import os
import re

import jieba
import jieba.analyse
import numpy
import pandas as pd
from snownlp import SnowNLP

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

# 创建停用词列表
def _get_stopwords_list(file_path):
    stopwords = [line.strip() for line in open(file_path, encoding='UTF-8').readlines()]
    stopwords.extend(['', ' ', '~', '…'])
    stopwords = tuple(stopwords)
    return stopwords


# 情感分析函数
def _analysis_comment(text):
    probs = []
    for i in range(len(text)):
        content = text[i].replace(u'\xa0', u' ')
        result = SnowNLP(content)
        probs.append(result.sentiments)
    return probs


# 计算每个景点情感倾向
def _cal_emotion_prob(goodComments, normalComments, badComments, countSummary):
    # 获取评论计数
    totalOpinionCount = int(countSummary['总评论数'])
    goodOpinionCount = int(re.findall(r'\d+', countSummary['好评'])[0])
    normalOpinionCount = int(re.findall(r'\d+', countSummary['中评'])[0])
    badOpinionCount = int(re.findall(r'\d+', countSummary['差评'])[0])

    # 情感分析
    if len(goodComments):
        goodProbs = _analysis_comment(goodComments)
        goodProbsAvg = numpy.average(goodProbs)
    else:
        goodProbsAvg=0
    if len(normalComments):
        normalProbs = _analysis_comment(normalComments)
        normalProbsAvg = numpy.average(normalProbs)
    else:
        normalProbsAvg=0
    if len(badComments):
        badProbs = _analysis_comment(badComments)
        badProbsAvg = numpy.average(badProbs)
    else:
        badProbsAvg=0
    # 计算公式
    totalProb = goodProbsAvg * (goodOpinionCount / totalOpinionCount) + \
                normalProbsAvg * (normalOpinionCount / totalOpinionCount) + badProbsAvg * (
                        badOpinionCount / totalOpinionCount)
    return totalProb


def _cal_words_freq(sentenses, stopwords):
    segments = {}
    jieba.enable_paddle()
    for sentense in sentenses:
        # TextRank 关键词抽取，只获取固定词性
        words = jieba.cut(sentense, use_paddle=True)
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


def comments_analysis(comment_file_path, stopwords_file_path):
    locations = listdir_nohidden(comment_file_path)
    for location in locations:
        # 构造文件路径
        print(location)
        location_file_path = comment_file_path + '/' + location
        landmarks = os.listdir(location_file_path)
        for landmark in landmarks:
            landmark_file_path = location_file_path + '/' + landmark
            # 读取json文件
            jsonFilePath = landmark_file_path+ '/'+ landmark+'各类评论数统计.json'
            with open(jsonFilePath, 'r', encoding='gbk') as f:
                countSummary = json.load(f)
            try:
                goodOpinions = pd.read_csv(landmark_file_path + '/好评.CSV', index_col=0)
                goodComments = goodOpinions["评论内容"]
            except Exception as e:
                goodComments = []
                pass
            try:
                normalOpinions = pd.read_csv(landmark_file_path + '/中评.CSV', index_col=0)
                normalComments = normalOpinions["评论内容"]
            except Exception as e:
                normalComments = []
                pass
            try:
                badOpinions = pd.read_csv(landmark_file_path + '/差评.CSV', index_col=0)
                badComments = badOpinions["评论内容"]
            except Exception as e:
                badComments = []
                pass
            landmark_prob = _cal_emotion_prob(goodComments, normalComments, badComments, countSummary)

            stopwords = _get_stopwords_list(stopwords_file_path)
            comments=[]
            for good_comment in goodComments:
                comments.append(good_comment)
            for normal_comment in goodComments:
                comments.append(normal_comment)
            for bad_comment in goodComments:
                comments.append(bad_comment)
            landmark_words_freq = _cal_words_freq(comments, stopwords)
            json_data={"emotional_prob": landmark_prob}
            json_data.update({"words_freq": landmark_words_freq})
            json_out = {"apiVersion": "1.0","data": json_data}
            with open(landmark_file_path + '/' + "comments analysis.json", "w", encoding='utf-8') as fp:
                fp.write(json.dumps(json_out, indent=4, ensure_ascii=False))
            print(landmark + " 分析完成")
    return True


if __name__ == "__main__":
    # 获取路径
    filePath = '../docs/comments'
    stopwords_file_path = os.path.dirname(os.path.abspath('.')) + '/projects/stopwords/stopwords.txt'
    comments_analysis(filePath, stopwords_file_path)
