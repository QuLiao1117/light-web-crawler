#!/usr/bin/python3
# encoding=utf-8

"""从马蜂窝（http://www.mafengwo.cn/）网站抓取地区景点的图片脚本。

Retrieves rows pertaining to the given keys from the Table instance
represented by big_table.  Silly things may happen if
other_silly_variable is not None.

Args:
    LOCATIONS: 计划抓取图片的地区（需为准确的专有名词，即在马蜂窝中可直接搜索到）
    GET_LANDMARK_NUM: 计划在选定的地区抓取的景点数量
    DOWNLOAD_PIC_NUM: 每个景点抓取的图片数
    BROWSER_OBJ: 一个Selenium浏览器对象
    FAIL_DOWNLOAD_LOCATIONS: 下载失败的地区

Returns:
    A dict mapping keys to the corresponding table row data
    fetched. Each row is represented as a tuple of strings. For
    example:

    {'Serak': ('Rigel VII', 'Preparer'),
     'Zim': ('Irk', 'Invader'),
     'Lrrr': ('Omicron Persei 8', 'Emperor')}

    If a key from the keys argument is missing from the dictionary,
    then that row was not found in the table.

Raises:
    IOError: An error occurred accessing the bigtable.Table object.
"""

import os
import re

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def location_landmark_pic_download(
        browser, location_name, landmark_number, pic_number_per_landmark, save_path):
    # driver为浏览器
    # location为景点所在地名称
    # LandmarkNum为保存景点数
    # PicNum为保存图片数

    # 打开景点页
    def _landmark_pic_download(site_link, location_path):
        # driver为浏览器
        # link为景点网址
        # name为景点所在地名称
        # PicNum为保存图片数

        # 下载图片
        def _site_pic_download(pic_num, landmark_path):
            # driver为浏览器
            # num为下载图片数
            # addr保存相对索引

            # 保存图片函数
            def _pic_link_save_as_png(pic_link, png_name, pic_path):
                # pic_link为图片超链接
                # path为保存相对地址
                # x为图片名称

                # 存储地址检查
                if not os.path.exists(pic_path):
                    os.makedirs(pic_path)
                pic_binary_data = requests.get(pic_link)
                png_path = pic_path + '/' + str(png_name) + ".png"

                # 保存图片
                with open(png_path, "wb") as png_file:
                    for chunk in pic_binary_data:
                        png_file.write(chunk)

            # 获得URL
            try:
                WebDriverWait(browser, 10).until(lambda x: x.find_elements_by_class_name("a-pic"))
            except TimeoutException:
                raise TimeoutException("  页面图片加载超时")
            elements_have_pic = browser.find_elements_by_class_name("a-pic")[1:pic_num + 1]

            # 下载前num张大图
            for pic_count in range(pic_num):
                thumbnail_link = elements_have_pic[pic_count].get_attribute('src')
                jpeg_link = thumbnail_link[0:re.search(r'\?', thumbnail_link).span()[0]]
                _pic_link_save_as_png(jpeg_link, pic_count + 1, landmark_path)
                print("  第%d张下载完成" % (pic_count + 1))

        browser.get(site_link)
        try:
            WebDriverWait(browser, 10).until(
                lambda x: x.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]'))
        except TimeoutException:
            raise TimeoutException(" 景点页加载超时")

        # 获得景点名
        title = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]')
        landmark_title = title.text.split('\n')
        landmark_name = landmark_title[0].replace("（已关/暂停营业）", "")
        # 构造存储相对地址
        print(" " + landmark_name)
        landmark_path = location_path + "/" + landmark_name
        # 进入景点图片页
        try:
            WebDriverWait(browser, 10).until(lambda x: x.find_element_by_class_name("pic-big"))
        except TimeoutException:
            raise TimeoutException(" 景点页加载超时")
        browser.find_element_by_class_name("pic-big").click()
        browser.switch_to.window(browser.window_handles[-1])

        # 下载图片
        _site_pic_download(pic_number_per_landmark, landmark_path)
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])

    location_path = save_path + "/" + location_name
    # 打开马蜂窝，搜索相应地点
    browser.get("https://www.mafengwo.cn/")
    try:
        WebDriverWait(browser, 10).until(
            lambda x: x.find_element_by_id("_j_index_search_input_all"))
    except TimeoutException:
        print("首页加载超时")
        return False
    browser.find_element_by_id("_j_index_search_input_all").send_keys(location_name)
    print(location_name)
    browser.find_element_by_id("_j_index_search_btn_all").click()

    # 打开该省份热门景点一览
    try:
        WebDriverWait(browser, 10).until(lambda x: x.find_element_by_link_text("景点"))
    except TimeoutException:
        print("地区加载超时")
        return False
    browser.find_element_by_link_text("景点").click()

    # 获得热门景点URL
    try:
        WebDriverWait(browser, 10).until(
            ec.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT, ('景点 -'))))
    except TimeoutException:
        print("地区景点加载超时")
        return False
    landmark_elements = browser.find_elements_by_partial_link_text('景点 -')
    landmark_number = landmark_number if landmark_number <= len(
        landmark_elements) else len(landmark_elements)
    landmark_links = []
    for landmark_count in range(landmark_number):
        landmark_links.append(landmark_elements[landmark_count].get_attribute("href"))

    for landmark_count in range(landmark_number):
        try:
            _landmark_pic_download(landmark_links[landmark_count], location_path)
        except TimeoutException as time_exception_msg:
            print(time_exception_msg)
            return False

    return True


if __name__ == "__main__":
    # 参数配置
    # 爬取地点
    LOCATIONS = ['陕西', '北京', '安徽']

    # 爬取景点数
    GET_LANDMARK_NUM = 5
    # 每个景点爬取图片数
    DOWNLOAD_PIC_NUM = 9
    # 加载浏览器，括号为浏览器连接程序位置，需要与本机安装的浏览器版本一致
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    BROWSER_OBJ = webdriver.Chrome()  # executable_path="/Library/chromedriver", options=option)
    ROOT_DIR = os.path.dirname(os.path.abspath('.')) + '/docs/pic'
    FAIL_DOWNLOAD_LOCATIONS = []
    # 循环下载
    for i in LOCATIONS:
        if ~location_landmark_pic_download(
                BROWSER_OBJ, i, GET_LANDMARK_NUM, DOWNLOAD_PIC_NUM, ROOT_DIR):
            print(i + "下载失败")
            FAIL_DOWNLOAD_LOCATIONS.append(i)
    # 退出浏览器
    BROWSER_OBJ.quit()
    if len(FAIL_DOWNLOAD_LOCATIONS) > 0:
        print("下载失败地点：", end='')
        print(FAIL_DOWNLOAD_LOCATIONS)
    else:
        print("所有地点下载完成")
