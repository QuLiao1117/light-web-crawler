#!/usr/bin/env python
# encoding=utf-8
import json
import os
import re

import numpy
import pandas as pd
from snownlp import SnowNLP


# 情感分析函数
def analysis_comment(text):
    probs = []
    for i in range(len(text)):
        content = text[i].replace(u'\xa0', u' ')
        result = SnowNLP(content)
        probs.append(result.sentiments)
    return probs


# 计算每个景点情感倾向
def cal_emotion_prob(filePath, landmarkName):
    # 读取json文件
    jsonFilePath = filePath + '/' + landmarkName + '各类评论数统计.json'
    with open(jsonFilePath, 'r', encoding='gbk') as f:
        countSummary = json.load(f)
    # 获取评论计数
    totalOpinionCount = int(countSummary['总评论数'])
    goodOpinionCount = int(re.findall(r'\d+', countSummary['好评'])[0])
    normalOpinionCount = int(re.findall(r'\d+', countSummary['中评'])[0])
    badOpinionCount = int(re.findall(r'\d+', countSummary['差评'])[0])

    # 情感分析
    try:
        goodOpinions = pd.read_csv(filePath + '/好评.CSV', index_col=0)
        goodComments = goodOpinions["评论内容"]
        goodProbs = analysis_comment(goodComments)
        goodProbsAvg = numpy.average(goodProbs)
    except Exception as e:
        print(e)
        goodProbsAvg = 0
        pass
    try:
        normalOpinions = pd.read_csv(filePath + '/中评.CSV', index_col=0)
        normalComments = normalOpinions["评论内容"]
        normalProbs = analysis_comment(normalComments)
        normalProbsAvg = numpy.average(normalProbs)
    except Exception as e:
        print(e)
        normalProbsAvg = 0
        pass
    try:
        badOpinions = pd.read_csv(filePath + '/差评.CSV', index_col=0)
        badComments = badOpinions["评论内容"]
        badProbs = analysis_comment(badComments)
        badProbsAvg = numpy.average(badProbs)
    except Exception as e:
        print(e)
        badProbsAvg = 0
        pass
    # 计算公式
    totalProb = goodProbsAvg * (goodOpinionCount / totalOpinionCount) + \
                normalProbsAvg * (normalOpinionCount / totalOpinionCount) + badProbsAvg * (
                            badOpinionCount / totalOpinionCount)
    return totalProb


def get_location_probs(filePath):
    # 构造文件路径

    landmarks = os.listdir(filePath)
    landmarkProbs = {}
    for i in landmarks:
        landmarkProbs[i] = cal_emotion_prob(filePath + '/' + i, i)
    return landmarkProbs


if __name__ == "__main__":
    # 获取路径
    filePath = '../docs/comments'

    locations = os.listdir(filePath)
    locationProbs = {}
    for i in locations:
        try:
            locationProbs[i] = get_location_probs(filePath + '/' + i)
        except Exception as e:
            print(e)
            pass
    jsonout={"apiVersion": "1.0", "data":locationProbs}
    with open(filePath + "/probs.json", "w", encoding='unicode') as fp:
        fp.write(json.dumps(locationProbs, indent=4, ensure_ascii=True))
