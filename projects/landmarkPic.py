#!/usr/bin/env python
# encoding=utf-8
import os
import re

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# 保存图片函数
def saveImg(pic_link, path, x):
    # pic_link为图片超链接
    # path为保存相对地址
    # x为图片名称

    # 存储地址检查
    if not os.path.exists(path):
        os.makedirs(path)
    pp = requests.get(pic_link)
    pth = path + str(x) + ".png"

    # 保存图片
    with open(pth, "wb") as f:
        for chunk in pp:
            f.write(chunk)
    print("  第%s张下载完成" % x)


# 下载图片
def DownLoadPic(driver, num, addr):
    # driver为浏览器
    # num为下载图片数
    # addr保存相对索引
    # 打开大图

    try:
        WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_css_selector("#container > li:nth-child(1) > a:nth-child(1) > img"))
    except Exception as e:
        print("  页面图片加载超时")
        print(e)
    driver.find_element_by_css_selector("#container > li:nth-child(1) > a:nth-child(1) > img").click()
    driver.switch_to.window(driver.window_handles[-1])

    # 构造存储相对地址
    root_dir = os.path.dirname(os.path.abspath('.'))
    path = root_dir + "/docs/pic" + addr + '/'

    # 下载前num张大图
    for i in range(1, num + 1):
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, ('//*[@id="_j_stageimg"]'))))
        except Exception as e:
            print("  加载图片超时")
            print(e)
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, ("s-next"))))
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "block-loading _j_stageloading")))
        except Exception as e:
            print("  寻找下一张图片超时")
            print(e)
        element = driver.find_element_by_class_name("s-next")
        driver.execute_script("arguments[0].click();", element)
        link = driver.find_element_by_xpath('//*[@id="_j_stageimg"]').get_attribute('src')
        link=link[0:re.search('\?',link).span()[0]]
        try:
            saveImg(link, path, i)
        except Exception as e:
            print("  图片保存失败")
            print(e)
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


# 打开景点页
def OpenLandmark(driver, link, name, PicNum):
    # driver为浏览器
    # link为景点网址
    # name为景点所在地名称
    # PicNum为保存图片数

    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]'))
    except Exception as e:
        print(" 景点页面加载超时")
        print(e)

    # 获得景点名
    title = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]')
    place_name = title.text.split('\n')
    place_name[0] = place_name[0].replace("（已关/暂停营业）", "")
    # 构造存储相对地址
    print(" " + place_name[0])
    addr = "/" + name + "/" + place_name[0]

    # 关闭底部广告栏
    try:
        WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_css_selector("#banner-con-gloable > div.banner-btn-con > img"))
        element = driver.find_element_by_css_selector("#banner-con-gloable > div.banner-btn-con > img")
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        print(" 底部广告遮挡取消失败")
        print(e)

    # 进入景点图片页
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("pic-big"))
    except Exception as e:
        print(" 景点页面加载超时")
        print(e)
    driver.find_element_by_class_name("pic-big").click()
    driver.switch_to.window(driver.window_handles[-1])

    # 下载图片
    DownLoadPic(driver, PicNum, addr)
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


def LoadLocation(driver, location, LandmarkNum, PicNum):
    # driver为浏览器
    # location为景点所在地名称
    # LandmarkNum为保存景点数
    # PicNum为保存图片数

    # 打开马蜂窝，搜索相应地点
    driver.get("https://www.mafengwo.cn/")
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("_j_index_search_input_all"))
    except Exception as e:
        print("首页加载超时")
        print(e)
    driver.find_element_by_id("_j_index_search_input_all").send_keys(location)
    print(location)
    driver.find_element_by_id("_j_index_search_btn_all").click()

    # 打开该省份热门景点一览
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_link_text("景点"))
    except Exception as e:
        print("地区加载超时")
        print(e)
    driver.find_element_by_link_text("景点").click()

    # 获得热门景点URL
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT, ('景点 -'))))
    except Exception as e:
        print("地区景点加载超时")
        print(e)
    link = driver.find_elements_by_partial_link_text('景点 -')
    ll = LandmarkNum if LandmarkNum <= len(link) else len(link)
    Landmarklink = []
    for i in range(ll):
        Landmarklink.append(link[i].get_attribute("href"))

    for i in range(ll):
        OpenLandmark(driver, Landmarklink[i], location, PicNum)


if __name__ == "__main__":
    # 参数配置
    # 爬取地点
    Location = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东',
                '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '西藏', '广西', '内蒙古', '宁夏', '新疆',
                '北京', '上海', '天津', '重庆', '香港', '澳门']

    # 爬取景点数
    LandmarkNum = 5
    # 每个景点爬取图片数
    PicNum = 9
    # 加载浏览器，括号为浏览器连接程序位置，需要与本机安装的浏览器版本一致
    #option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    driver = webdriver.Chrome()  #executable_path="/Library/chromedriver", options=option)

    failLocation = []
    # 循环下载
    for i in Location:
        try:
            LoadLocation(driver, i, LandmarkNum, PicNum)
        except Exception as e:
            print(i + "下载失败")
            print(e)
            failLocation.append(i)
            pass
    # 退出浏览器
    driver.quit()
    if len(failLocation) > 0:
        print("下载失败地点：", end='')
        print(failLocation)
    else:
        print("所有地点下载完成")
