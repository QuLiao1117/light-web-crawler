#!/usr/bin/env python
# encoding=utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os


# 保存图片函数
def saveImg(pic_link, path, x):
    if not os.path.exists(path):
        os.makedirs(path)
    pp = requests.get(pic_link)
    pth = path + str(x) + ".png"
    with open(pth, "wb") as f:
        for chunk in pp:
            f.write(chunk)
    print("  第%s张下载完成" % x)


# 下载图片
def DownLoadPic(driver, num, addr):
    # 打开大图
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="container"]/li[1]/a[1]'))
    except:
        print("  页面图片超时")
    driver.find_element_by_xpath('//*[@id="container"]/li[1]/a[1]').click()
    driver.switch_to.window(driver.window_handles[-1])
    root_dir = os.path.dirname(os.path.abspath('.'))
    path = root_dir + "/docs/pic" + addr + '/'

    # 下载前num张大图
    for i in range(1, num + 1):
        try:
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("s-pic"))
        except:
            print("  加载图片超时")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, ("s-next"))))
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME,"block-loading _j_stageloading")))
        except:
            print("  寻找下一张图片超时")
        driver.find_element_by_class_name("s-next").click()
        posi = driver.find_element_by_xpath('//*[@id="_j_stageimg"]').get_attribute('src')
        try:
            saveImg(posi, path, i)
        except:
            print("  图片保存失败")
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


# 打开景点页
def OpenLandmark(driver, link, name, PicNum):
    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]'))
    except:
        print(" 景点页面加载超时")
    title = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]')
    place_name = title.text.split('\n')
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("pic-big"))
    except:
        print(" 景点页面加载超时")
    driver.find_element_by_class_name("pic-big").click()
    driver.switch_to.window(driver.window_handles[-1])
    print(" " + place_name[0])
    addr = "/" + name + "/" + place_name[0]
    # 下载图片
    DownLoadPic(driver, PicNum, addr)
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


def LoadLocation(driver, location, LandmarkNum, PicNum):
    # 打开马蜂窝，搜索相应地点
    driver.get("https://www.mafengwo.cn/")
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("_j_index_search_input_all"))
    except:
        print("首页加载超时")
    driver.find_element_by_id("_j_index_search_input_all").send_keys(location)
    print(location)
    driver.find_element_by_id("_j_index_search_btn_all").click()
    # 打开该省份热门景点一览
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_link_text("景点"))
    except:
        print("地区加载超时")
    driver.find_element_by_link_text("景点").click()
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT, ('景点 -'))))
    except:
        print("地区景点加载超时")
    link = driver.find_elements_by_partial_link_text('景点 -')
    ll = LandmarkNum if LandmarkNum <= len(link) else len(link)
    Landmarklink = []
    for i in range(ll):
        Landmarklink.append(link[i].get_attribute("href"))
    for i in range(ll):
        OpenLandmark(driver, Landmarklink[i], location, PicNum)


if __name__ == "__main__":
    PicNum = 9
    province = [  '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东',
                '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '西藏', '广西', '内蒙古', '宁夏', '新疆',
                '北京', '上海', '天津', '重庆', '香港', '澳门']
    LandmarkNum = 5

    # 加载浏览器
    driver = webdriver.Chrome(executable_path="/Library/chromedriver")
    for i in province:
        LoadLocation(driver, i, LandmarkNum, PicNum)
    driver.quit()
