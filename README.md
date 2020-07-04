# Light Web Crawler for  Tourists Attraction

[![China Agricultural University College of Information and Electical Engineering](https://img.shields.io/static/v1?label=CAU&message=CIEE&color=R0-G135-B60&link=https://www.cau.edu.cn&link=http://ciee.cau.edu.cn/)](https://www.cau.edu.cn) [![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

[![Python 3.7](https://img.shields.io/badge/Python-3.7-blue?style=flat-square&logo=python)](https://www.python.org/) [![HTML Bootstrap](https://img.shields.io/badge/HTML-Bootstrap-blue?style=flat-square&logo=html5)](https://getbootstrap.com/) [![Selenium Python](https://img.shields.io/badge/Selenium-Python-orange?style=flat-square)](https://www.selenium.dev/) [![ECHARTS 4.8.0](https://img.shields.io/badge/ECHARTS-4.8.0-orange?style=flat-square&logo=apache-echarts)](https://echarts.apache.org/zh/index.html)

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
  - [文档规范](#文档规范)
- [使用指南](#使用指南)
  - [环境配置](#环境配置)
  - [示例程序变量](#示例程序变量)
  - [运行示例程序](#运行示例程序)
- [API](#API)
  - [数据获取](#数据获取API)
  - [数据处理](#数据处理API)
- [已知问题](#已知问题)
- [文件目录](#文件目录)
- [项目成员](#项目成员)
- [致谢](#致谢)
- [使用许可](#使用许可)

## 项目背景

本项目为中国农业大学2019-2020年夏季学期web技术及数据采集与处理实训课程大作业。目标为以爬虫实现为基础，综合展示代码学习成果。本项目以<a href="https://www.mafengwo.cn/">马蜂窝网站</a>景点数据为爬取目标，抓取景点相关数据，最后通过网页的形式展示爬取结果。

考虑到仓库大小及不同省份和不同景点均需单独制作页面，项目只选取3个省份的Top5的景点进行样例展示。抓取代码提供API，直接调用即可；同时提供示例程序运行所有API。

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

省份景点Top5：具体地点景点页导航

景点详细：基本信息、景点图、评论词云、条形图、情感倾向

##### 分工

1. 李海霞：地图首页（已完成）
2. 周芳宇：省份景点Top5（已完成）
3. 瞿李傲：景点详细页（已完成）
4. 林邦皓：数据处理（已完成）

要求：至少每两天提交内容并讨论

DDL：2020年7月3日

### 第三阶段：完善各项内容

1. 网页上传到服务器
2. 编写示例程序（基本完成）
3. 制作总结视频
4. 优化代码
5. 规范文档

6. 统一数据编码、接口、引用


DDL：2020年7月5日

## 项目亮点

项目过程

#### 数据获取（Python3）

1. 使用Selenium自动化操作访问网站。

   优点：模拟人的操作行为，避免被反爬虫机制判定为爬虫操作

   不足：抓取速度较慢

2. 封装为API接口可直接调用，亦可以直接运行函数文件，其中含有自动运行的脚本。

3. 提供一个同时调用所有API的示例程序，使用多进程技术，加快获取速度。

#### 网页实现（HTML）

1. 采用Bootstrap框架，实现了不同尺寸页面下，元素位置自动调整至最佳展示效果。

2. 采用轮播图技术展示图片。

3. 使用导航栏跳转。
4. 采用ECHARTS实现地图展示。

#### 数据处理（Python3）

1. 利用PaddlePaddle深度学习框架，训练序列标注（双向GRU）网络模型实现评论分词。

   优点：贴合中文词汇含义的分词模型

2. 使用SnowNLP自有训练模型计算情感倾向。

3. 使用四川大学机器智能实验室、哈工大停用词库。

#### 文档规范

1. Python文件使用pylint检测代码规范。
2. Python、HTML、JavaScript、CSS、json文件遵循Google风格。（待完成）

3. CSV文件遵循IETF的RFC4180标准。（待完成）

## 使用指南

#### 环境配置

最少下载内容

```
文件夹：project和sources
示例程序：example_code.py
```

在运行的Python3环境中安装`requirements.txt`文件中列出的所有外部Python包。

```shell
$ pip install *
Eg. $ pip install selenium>=3.141.0
```

此外，还需下载与系统和浏览器版本匹配的驱动程序（示例程序默认使用Google Chrome，Chrome 测试稳定）。下载完成后将驱动程序文件移动至运行的Python3环境目录下的 `/bin` 文件夹中。

Google Chrome驱动下载：<a href='https://npm.taobao.org/mirrors/chromedriver'> npm.taobao.org/mirrors/chromedriver </a>

#### 示例程序变量

##### FILE_PATH

```python
FILE_PATH = os.path.abspath('.')
```

指明项目函数API和停用词的`/projects`文件夹所在目录，同时表示抓取数据的存储目录。

###### 默认值

示例程序所在目录

##### LOCATIONS

```python
LOCATIONS = list
```

包含要搜索的地区名称，需为专有名词（建议为省、直辖市）

###### 默认值

['陕西', '北京', '安徽']

##### GET_LANDMARK_NUM

```python
GET_LANDMARK_NUM = int
```

每个搜索地区抓取的景点数量

###### 默认值

5

##### DOWNLOAD_PIC_NUM

```python
DOWNLOAD_PIC_NUM = int
```

每个景点抓取的图片数量

###### 默认值

9

##### PROCESSING_POOL

```python
PROCESSING_POOL = Pool(int)
```

最多同时运行进程数

###### 默认值

Pool(3)

#### 运行示例程序

如需更换浏览器对象或者添加浏览器驱动程序路径，替换示例程序中如下标明的文字。

```python
def _pic_clawer():
browser_obj = webdriver."浏览器名称"("驱动程序路径")
...
```

直接示例运行程序，获取和处理的数据结果保存在`$FILE_PATH$/docs`文档目录中。

## API

#### 数据获取API

##### get_place_top5_landmark_info

从马蜂窝网站抓取地区景点信息,存储到/docs/city_landmart_info/地区名.json文件中

```
import landmart_info_crawler
get_place_top5_landmark_info(location="北京", landmark_number=5)
```

###### 参数

location:搜索的地区名称

landmark_number: 计划在选定的地区抓取的景点数量（默认为5）



##### location_landmark_pic_download

从马蜂窝网站抓取地区景点图片

```python
import landmark_pic_crawler
location_landmark_pic_download(browser, location_name="北京", landmark_number=5,
        pic_number_per_landmark=9, save_path=os.path.abspath('.'))
```

###### 参数

browser: 一个Selenium浏览器对象

location_name: 搜索的地区名称（默认为"北京"）

landmark_number: 计划在选定的地区抓取的景点数量（默认为5）

pic_number_per_landmark: 每个景点抓取的图片数（默认为9）

save_path: 保存路径（默认为文件所在目录）

###### 返回值

布尔值

True表示输入的地区图片全部下载成功；

False表示该地区指定数量的部分图片未下载成功。

###### 事件

TimeoutException: 由于网页元素加载太久（默认10s）而报错。

------

##### pic_link_save_as_png

```python
import landmark_pic_crawler
pic_link_save_as_png(pic_link, png_name, pic_path)
```

保存链接图片为png格式

###### 参数

pic_link: 一张图片链接

png_name: 图片名称

pic_path: png图片保存路径

------

#### 数据处理API

##### cal_words_freq

对给出的文本list进行分词

```python
import comments_analysis
cal_words_freq(texts, stopwords)
```

###### 参数

texts: 一组评论list

stopwords: 停止词的list

###### 返回值

字典对象

key为词，value为频率

------

##### texts_analysis

计算文本整体情感概率并进行词频计算

```python
import comments_analysis
texts_analysis(comments_file_path, stopwords_file_path):
```

###### 参数

comments_file_path: 所有评论的文件夹路径

stopwords_file_path: 停用词文件路径

###### 输出

在comments_file_path目录中创建comments analysis.json文件，json包含整体情感概率和词频数据；同时生成comments wordcloud.png词云图。

## 已知问题

1. 数据获取API均无法正常运行Safari浏览器。
2. 若`$FILE_PATH$/docs/*/*/*`目录中包含其他非数据获取阶段获取的文档，则会导致数据处理出错。
3. 使用echarts实现各省份地图之后得到的网页不能通过浏览器直接打开本地HTML文件，会出现跨域问题（浏览器（Webkit内核）的安全策略决定了file协议访问的应用无法使用XMLHttpRequest对象）目前的解决方案是将文件放到服务器上进行访问，可以正常加载！

## 文件目录

```
├── README.md                   // 项目说明书
├── requirements.txt            // 依赖的外部Python包列表
├── test                        // 项目的测试文件夹
├── example_code.py             // 示例程序
├── project                     // 项目数据获取代码
│   ├── landmarkInfo.py              // 基本信息爬虫
│   ├── landmarkComment.py           // 评论爬虫
│   ├── landmark_pic_crawler.py      // 图片爬虫
│   ├── commens_analysis.py          // 评论分析
│   └── stopword                     // 停用词库
│       └── stopword.txt
├── docs                        // 项目相关数据
│   ├── city_landmark_info           // 景点基本信息
│   │   └── *.json                          // 各地区景点信息
│   ├── comments                     // 景点评论相关
│   │   └── *                        // 各地区文件夹
│   │       └── *                           // 各景点文件夹
│   │           ├── 好评.CSV                       // 好评评论
│   │           ├── 中评.CSV                       // 中评评论
│   │           ├── 差评.CSV                       // 差评评论
│   │           ├── *各类评论数统计.json             // 景点评价数统计
│   │           ├── comments wordcloud.png        // 评价词云
│   │           └── comments analysis.json        // 评论词频和情感概率
│   └── pic                          // 景点图片
│       └── *                               // 各地区文件夹
│           └── *                                  // 各景点文件夹
│               └── *.png                                // 景点图片
├── sources                          // 网页文件夹
│   ├── HEAD.png                            // 项目Logo
│   ├── HomePage                            // 首页HTML文件夹
│   ├── scene-intro                         // 各景点HTML文件夹
│   └──                                     // 
└── LICENSE
```

## 项目成员

<a href="https://github.com/Terrensou">@Terrensou (林邦皓)</a>

<a href="https://github.com/QuLiao1117">@QuLiao1117 (瞿李傲)</a>

<a href="https://github.com/lhx007">@lhx007 (李海霞)</a>

<a href="https://github.com/zfy611">@zfy611 (周芳宇)</a>

## 致谢

非常感谢课程教授和助教对我们小组技术和代码规范方面的支持！

<a href="http://faculty.cau.edu.cn/xxdqxy/wcc/list.htm">吴才聪教授</a>

<a href="https://github.com/Terrensou">@cauqiaopeng (小乔帮主)</a>

<a href="https://github.com/prefect-of-gryffindor">@prefect-of-gryffindor</a>

## 使用许可

[MIT](LICENSE) © 2020