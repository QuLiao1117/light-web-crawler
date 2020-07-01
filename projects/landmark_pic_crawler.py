#!/usr/bin/python3
# encoding=utf-8

"""一个从马蜂窝（http://www.mafengwo.cn/）网站抓取地区景点的图片脚本。

利用Selenium自动化操作，打开马蜂窝首页，使用搜索栏搜索地区。
在搜索结果中，查看该地区的景点，利用元素获取打开景点页面。
在景点页中，单击图片进入该景点的图片页。通过元素获取每一张图片的真实URL，并下载。

Args:
    LOCATIONS: 计划抓取图片的地区（需为准确的专有名词，即在马蜂窝中可直接搜索到）
    GET_LANDMARK_NUM: 计划在选定的地区抓取的景点数量
    DOWNLOAD_PIC_NUM: 每个景点抓取的图片数
    BROWSER_OBJ: 一个Selenium浏览器对象
    FAIL_DOWNLOAD_LOCATIONS: 下载失败的地区

Print:
    如有下载失败的地区，则会打印出来

"""

import os
import re

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


# 保存图片函数
def _pic_link_save_as_png(pic_link, png_name, pic_path):

    # Args:
    #   pic_link: 一张图片的超链接
    #   pic_path: 保存图片的相对地址
    #   png_name: 图片名称

    # 存储地址检查
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)
    pic_binary_data = requests.get(pic_link)
    png_path = pic_path + '/' + str(png_name) + ".png"
    # 保存图片
    with open(png_path, "wb") as png_file:
        for chunk in pic_binary_data:
            png_file.write(chunk)


def location_landmark_pic_download(
        browser, location_name="北京", landmark_number=5,
        pic_number_per_landmark=9, save_path=os.path.abspath('.')):

    """从马蜂窝（http://www.mafengwo.cn/）网站抓取地区景点的图片方法。

    利用Selenium自动化操作，打开马蜂窝首页，使用搜索栏搜索地区。
    在搜索结果中，查看该地区的景点，利用元素获取打开景点页面。
    在景点页中，单击图片进入该景点的图片页。通过元素获取每一张图片的真实URL，并下载。

    Args:
        browser: 一个Selenium浏览器对象
        location_name: 搜索的地区名称
        landmark_number: 计划在选定的地区抓取的景点数量
        pic_number_per_landmark: 每个景点抓取的图片数
        save_path: 保存路径

    Return:
        返回布尔值。
        True表示输入的地区图片全部下载成功；
        False表示该地区指定数量的部分图片未下载成功。

    Raise:
        TimeoutException: 由于网页元素加载太久（默认10s）而报错。
        浏览器显示操作模式下，误操作改变自动操作的浏览器，关闭浏览器等行为皆有可能导致该错误的抛出。
        建议浏览器自动操作过程中，将浏览器置于置顶页面，并不进行其他操作，保证浏览器页面正常加载并识别。
        由于爬虫过程中，网络资源消耗较大。如出现网络波动或者同时有其他较大网络消耗的进程，都有可能触发该错误。
        报错时，会抛出超时网页的名称。

    """

    # 打开景点页
    def _landmark_pic_download(site_link, location_path):

        # Args:
        #   site_link: 一个景点网址
        #   location_path: 保存图片路径

        # 下载图片页的图片
        def _site_pic_download(pic_num, landmark_path):

            # Args:
            #   pic_num: 下载图片数
            #   landmark_path: 保存目录的相对索引

            # 获得图片所在元素
            try:
                WebDriverWait(browser, 10).until(lambda x: x.find_elements_by_class_name("a-pic"))
            except TimeoutException:
                raise TimeoutException("  页面图片加载超时")
            elements_have_pic = browser.find_elements_by_class_name("a-pic")
            # 下载指定数量的大图
            for pic_count in range(pic_num):
                if pic_count >= len(elements_have_pic) - 1:
                    browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight); "
                        "var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                    elements_have_pic = browser.find_elements_by_class_name("a-pic")
                    if pic_count >= len(elements_have_pic) - 1:
                        raise TimeoutException("  无法加载更多图片")
                thumbnail_link = elements_have_pic[pic_count].get_attribute('src')
                jpeg_link = thumbnail_link[0:re.search(r'\?', thumbnail_link).span()[0]]
                print(jpeg_link)
                _pic_link_save_as_png(jpeg_link, pic_count + 1, landmark_path)
                print("  第%d张下载完成" % (pic_count + 1))

        # 打开景点页
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

    location_path = save_path + "/" + location_name  # 构造保存地区的文件夹路径
    browser.get("https://www.mafengwo.cn/")  # 打开马蜂窝，搜索相应地点
    # 搜索地区
    try:
        WebDriverWait(browser, 10).until(
            lambda x: x.find_element_by_id("_j_index_search_input_all"))
    except TimeoutException:
        print("首页加载超时")
        return False
    browser.find_element_by_id("_j_index_search_input_all").send_keys(location_name)
    print(location_name)
    browser.find_element_by_id("_j_index_search_btn_all").click()
    # 打开该地区景点一览
    try:
        WebDriverWait(browser, 10).until(lambda x: x.find_element_by_link_text("景点"))
    except TimeoutException:
        print("地区页面加载超时")
        return False
    browser.find_element_by_link_text("景点").click()

    # 获得景点URL
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
    # 调用景点图片下载函数
    for landmark_count in range(landmark_number):
        try:
            _landmark_pic_download(landmark_links[landmark_count], location_path)
        except TimeoutException as time_exception_msg:
            print(time_exception_msg)
            return False
    return True


# 执行脚本
if __name__ == "__main__":
    # 参数
    LOCATIONS = ['陕西', '北京', '安徽']  # 爬取地点
    GET_LANDMARK_NUM = 5  # 爬取景点数
    DOWNLOAD_PIC_NUM = 9  # 每个景点爬取图片数
    BROWSER_OBJ = webdriver.Chrome()  # 加载浏览器，括号为浏览器连接程序位置（默认为python.exe文件位置），需要与本机安装的浏览器版本一致
    ROOT_DIR = os.path.dirname(os.path.abspath('.')) + '/docs/pic'  # 图片保存的根路径
    FAIL_DOWNLOAD_LOCATIONS = []  # 下载失败的地区
    # 循环下载
    for location in LOCATIONS:
        if not location_landmark_pic_download(
                BROWSER_OBJ, location, GET_LANDMARK_NUM, DOWNLOAD_PIC_NUM, ROOT_DIR):
            print(location + "下载失败")
            FAIL_DOWNLOAD_LOCATIONS.append(location)
    BROWSER_OBJ.quit()  # 退出浏览器
    # 输出下载失败的地区
    if len(FAIL_DOWNLOAD_LOCATIONS) > 0:
        print("下载失败地点：", end='')
        print(FAIL_DOWNLOAD_LOCATIONS)
    else:
        print("所有地点下载完成")
