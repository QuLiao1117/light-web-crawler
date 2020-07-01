# Light Web Crawler for  Tourists Attraction

![CAU CIEE](https://img.shields.io/static/v1?label=CAU&message=CIEE&color=R0-G135-B60&link=https://www.cau.edu.cn&link=http://www.ciee.cau.edu.cn) [![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

![Python 3.7](https://img.shields.io/badge/Python-3.7-blue?style=flat-square&logo=python) ![HTML-JavaScript](https://img.shields.io/badge/HTML-JavaScript-blue?style=flat-square&logo=html5) [![Selenium Python](https://img.shields.io/badge/Selenium-Python-orange?style=flat-square)](https://www.selenium.dev/) [![ECHARTS 4.8.0](https://img.shields.io/badge/ECHARTS-4.8.0-orange?style=flat-square&logo=apache-echarts)](https://echarts.apache.org/zh/download.html)

## 目录

- [项目背景](#项目背景)
- [项目进度](#项目进度)
  - [第一阶段](#第一阶段：抓取数据)
  - [第二阶段](#第二阶段：数据处理、网页实现)
  - [第三阶段](#第三阶段：完善各项内容)
- [项目亮点](#项目亮点)
  - [数据获取](#数据获取（Python3）)
  - [网页实现](#网页实现（HTML）)
  - [数据处理](#数据处理（Python3）)
  - [文件规范](#文件规范)
- [使用指南](#使用指南)
  - [环境配置](#环境配置)
- [文件目录](#文件目录)
- [项目成员](#项目成员)
- [致谢](#致谢)
- [使用许可](#使用许可)

## 项目背景

本项目为中国农业大学2019-2020年夏季学期web技术及数据采集与处理实训课程大作业。目标为以爬虫实现为基础，综合展示代码学习成果。本项目以<a href="https://www.mafengwo.cn/">马蜂窝网站</a>景点数据为爬取目标，抓取景点相关数据，最后通过网页的形式展示爬取结果。考虑到仓库大小及不同省份和不同景点均需单独制作页面，项目只选取3个省份的Top5的景点进行样例展示。抓取代码提供API，直接调用即可。

## 项目进度

### 第一阶段：抓取数据

##### 抓取省份TOP5景点（3个）

陕西、安徽、北京

##### 抓取内容

1. 林邦皓：景点图 --> 文件夹（已完成）
2. 瞿李傲：景点基本信息（电话、交通、门票等等）--> json (已完成,脚本封装完毕)
3. 李海霞：相关评论 --> csv/json（已完成）

完成时间：2020年6月28日

### 第二阶段：数据处理、网页实现

##### 网页逻辑：地图首页 --> 省份景点Top5 --> 景点详细

地图首页：景点轮播图 + echarts地图

省份景点Top5：具体地点景点导航

景点详细：基本信息、景点图、评论词云、条形图、情感倾向

##### 分工

1. 李海霞：地图首页
2. 周芳宇：省份景点Top5
3. 瞿李傲：景点详细页
4. 林邦皓：数据处理（已完成）

要求：至少每两天提交内容并讨论

DDL：2020年7月3日

### 第三阶段：完善各项内容

制作总结报告

规范代码及文件

统一数据编码

DDL：2020年7月5日

## 项目亮点

#### 数据获取（Python3）

1、使用Selenium自动化操作访问网站。

优点：模拟人的操作行为，避免被反爬虫机制判定为爬虫操作

不足：抓取速度较慢

2、封装为API接口可直接调用，亦可以直接运行函数文件，其中含有自动运行的脚本。

3、提供一个同时调用所有API的示范代码，使用多线程技术，加快获取速度。（待完成）

#### 网页实现（HTML）

1、实现了不同尺寸页面下，元素位置自动调整至最佳展示效果。

2、采用轮播图技术展示图片。

3、使用导航栏跳转。

#### 数据处理（Python3）

1、利用PaddlePaddle深度学习框架，训练序列标注（双向GRU）网络模型实现评论分词。

优点：贴合中文词汇含义的分词模型

2、使用SnowNLP自有训练模型计算情感倾向。

3、使用四川大学机器智能实验室、哈工大停用词库。

#### 文件规范

1、Python文件使用pylint检测代码规范。

2、Python、HTML、JavaScript、CSS、json文件遵循Google风格。（待完成）

3、CSV文件遵循IETF的RFC4180标准。（待完成）

## 使用指南

#### 环境配置

在运行的Python3环境中安装requirements.txt文件中列出的所有外部Python包。

```shell
pip install *
eg. pip install selenium>=3.141.0
```

此外，还需下载与系统和浏览器版本匹配的驱动程序（示例程序默认使用Google Chrome，测试稳定）。下载完成后将驱动程序文件移动至运行的Python3环境目录下的 `/bin` 文件夹中。

Google Chrome驱动下载：<a href='https://npm.taobao.org/mirrors/chromedriver'> npm.taobao.org/mirrors/chromedriver </a>

## 文件目录

```
├── Readme.md                   // 项目说明书
├── requirements.txt            // 依赖的外部Python包列表
├── test                        // 项目的测试文件夹
├── project                     // 项目主体部分的代码
│   ├── landmarkInfo.py              // 基本信息爬虫
│   ├── 爬取城市景点信息.ipynb          // 基本信息爬虫
│   ├── geoCode.py                   // 经纬度获取
│   ├── landmarkComment.py           // 评论爬虫
│   ├── landmark_pic_crawler.py      // 图片爬虫
│   ├── commens_analysis.py          // 评论分析
│   └── stopword                     // 停用词库
│       └── stopword.txt
├── docs                        // 项目相关数据
│   ├── city_landmark_info           // 景点基本信息
│   ├── comments                     // 景点评论相关
│   │   └── *                        // 各地区文件夹
│   │       └── *                           // 各景点文件夹
│   │           ├── 好评.CSV                       // 好评评论
│   │           ├── 中评.CSV                       // 中评评论
│   │           ├── 差评.CSV                       // 差评评论
│   │           ├── *各类评论数统计.json             // 景点评价数统计
│   │           └── comments analysis.json        // 评论词频和情感概率
│   └── pic                          // 景点图片
│       └── *                               // 各地区文件夹
│           └── *                                  // 各景点文件夹
│               └── *.png                                // 各景点文件夹
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