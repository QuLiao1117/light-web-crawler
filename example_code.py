#!/usr/bin/python3
# encoding=utf-8

"""该程序为示例程序：在马蜂窝景点中爬取的景点数据，并进行一定的数据分析。

project中为本项目编写的程序方法。

Args:
    FILE_PATH: 爬取数据保存路径
    LOCATIONS: 计划抓取图片的地区（需为准确的专有名词，即在马蜂窝中可直接搜索到）
    GET_LANDMARK_NUM: 计划在选定的地区抓取的景点数量
    DOWNLOAD_PIC_NUM: 每个景点抓取的图片数
    PROCESSING_POOL: 指定最大运行进程数

"""

import os
import sys
from multiprocessing import Pool

from selenium import webdriver

FILE_PATH = os.path.abspath('.')  # projects项目函数API地址，默认与示例程序同目录

sys.path.append(FILE_PATH + '/projects')
from projects import comments_analysis as cm
from projects import landmark_pic_crawler as lpc
from projects import landmark_comment_crawler as lcc
from projects import landmark_info_crawler as lic

# 参数配置
LOCATIONS = ['陕西', '北京', '安徽']  # 爬取地点
GET_LANDMARK_NUM = 5  # 爬取景点数
DOWNLOAD_PIC_NUM = 9  # 每个景点爬取图片数


# 图片抓取
def _pic_clawer():
    browser_obj1 = webdriver.Chrome()
    fail_download_locations = []  # 下载失败的地区
    # 循环下载
    for location1 in LOCATIONS:
        if not lpc.location_landmark_pic_download(
                browser_obj1, location1, GET_LANDMARK_NUM, DOWNLOAD_PIC_NUM, FILE_PATH + '/docs/pic'):
            print(location1 + "下载失败")
            fail_download_locations.append(location1)
    # 输出下载失败的地区
    if len(fail_download_locations) > 0:
        print("下载失败地点：", end='')
        print(fail_download_locations)
    else:
        print("所有地点下载完成")
    browser_obj1.quit()  # 退出浏览器


def _comment_clawer_analysis():
    browser_obj2 = webdriver.Chrome()
    for location2 in LOCATIONS:
        lcc.get_place_top5_comments(location2, browser_obj2, GET_LANDMARK_NUM, FILE_PATH + '/docs/comments')
    cm.texts_analysis(FILE_PATH + '/docs/comments',
                      FILE_PATH + '/projects/stopwords/stopwords.txt')
    browser_obj2.quit()  # 退出浏览器


def _info_clawer():
    browser_obj3 = webdriver.Chrome()
    for location3 in LOCATIONS:
        lic.get_place_top5_landmark_info(browser_obj3, location3,
                                         FILE_PATH + '/docs/city_landmark_info/', GET_LANDMARK_NUM)
    browser_obj3.quit()  # 退出浏览器


PROCESSING_POOL = Pool(3)  # 最多同时运行进程数

PROCESSING_POOL.apply_async(func=_comment_clawer_analysis, args=())
PROCESSING_POOL.apply_async(func=_info_clawer, args=())
PROCESSING_POOL.apply_async(func=_pic_clawer, args=())
PROCESSING_POOL.close()
PROCESSING_POOL.join()
#_pic_clawer()
print('示例程序运行完毕！')
