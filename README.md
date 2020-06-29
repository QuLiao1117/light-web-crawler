# Light Web Crawler for  Tourists Attraction

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme) ![Python 3.7](https://img.shields.io/badge/Python-3.7-blue?style=flat-square) ![HTML-JavaScript](https://img.shields.io/badge/HTML-JavaScript-blue?style=flat-square) [![Selenium Python](https://img.shields.io/badge/Selenium-Python-orange?style=flat-square)](https://www.selenium.dev/) [![ECHARTS 4.8.0](https://img.shields.io/badge/ECHARTS-4.8.0-orange?style=flat-square)](https://echarts.apache.org/zh/download.html)

## 目录

- [项目背景](#项目背景)
- [项目进度](#项目进度)
  - [第一阶段](#第一阶段：抓取数据)
  - [第二阶段](#第二阶段：数据处理、网页实现)
  - [第三阶段](#第三阶段：扩展网页内容)
- [使用指南](#使用指南)
- [文件目录](#文件目录)
- [项目成员](#项目成员)
- [致谢](#致谢)
- [使用许可](#使用许可)

## 项目背景

本项目为中国农业大学2019-2020年夏季学期web技术及数据采集与处理实训课程大作业。目标为以爬虫实现为基础，综合展示代码学习成果。本项目以<a href="https://www.mafengwo.cn/">马蜂窝网站</a>景点数据为爬取目标，抓取景点相关数据，最后通过网页的形式展示爬取结果。

数据获取和处理：Python, Selenium

网页实现：HTML, JavaScript, ECHARTS

## 项目进度

### 第一阶段：抓取数据

##### 抓取省份TOP5景点（3个）：

1、陕西：https://www.mafengwo.cn/jd/13083/gonglve.html

2、安徽：https://www.mafengwo.cn/jd/12719/gonglve.html

3、北京：https://www.mafengwo.cn/jd/10065/gonglve.html

##### 抓取内容：

1. 林邦皓：景点图 --> 文件夹（已完成）
2. 瞿李傲：景点基本信息（电话、交通、门票等等）--> json (已完成,脚本封装完毕)
3. 李海霞：相关评论 --> csv/json（已完成）

爬虫语言：Python、Selenium

完成时间：2020年6月28日

### 第二阶段：数据处理、网页实现

##### 网页逻辑：地图首页 -> 省份景点Top5 -> 景点详细

地图首页：景点轮播图+echarts地图

省份景点Top5：具体地点景点导航

景点详细：基本信息、景点图、评论词云、条形图、情感倾向

数据处理：Python

相关技术：HTML、Echarts、JavaScript、Python

##### 分工：

1. 李海霞：地图首页
2. 周芳宇：省份景点Top5
3. 瞿李傲：景点详细页
4. 林邦皓：数据处理、代码规范

要求：至少每两天提交内容并讨论

DDL：2020年7月5日

### 第三阶段：扩展网页内容

待定

## 使用指南

待编辑

## 文件目录

```
├── Readme.md                   // 项目说明书
├── test                        // 项目的测试文件夹
├── project                     // 项目主体部分的代码
│   ├── landmarkInfo.py         // 景点信息爬虫
│   ├── 爬取城市景点信息.ipynb     // 景点信息爬虫
│   ├── geoCode.py              // 景点经纬度获取
│   ├── landmarkComment.py      // 景点评论爬虫
│   └── landmarkPic.py          // 景点图片爬虫
├── docs                        // 爬取内容
│   ├── city_landmark_info      // 景点信息
│   ├── comments                // 景点评论
│   └── pic                     // 景点图片
└── LICENSE
```

## 项目成员

<a href="https://github.com/Terrensou">@Terrensou (林邦皓)</a>

<a href="https://github.com/QuLiao1117">@QuLiao1117 (瞿李傲)</a>

<a href="https://github.com/lhx007">@lhx007 (李海霞)</a>

<a href="https://github.com/zfy611">@zfy611 (周芳宇)</a>

## 致谢

非常感谢课程老师和助教对我们小组技术和代码规范方面的支持！

<a href="http://faculty.cau.edu.cn/xxdqxy/wcc/list.htm">吴才聪老师</a>

<a href="https://github.com/Terrensou">@cauqiaopeng (小乔帮主)</a>

<a href="https://github.com/prefect-of-gryffindor">@prefect-of-gryffindor</a>

## 使用许可

[MIT](LICENSE) © 2020

