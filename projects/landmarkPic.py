#!/usr/bin/env python
# encoding=utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

#保存图片函数
def saveImg(pic_link, path,x):
    if not os.path.exists(path):
        os.makedirs(path)
    pp = requests.get(pic_link)
    pth = path + str(x) + ".png"
    with open(pth, "wb") as f:
        for chunk in pp:
            f.write(chunk)
    print("第%s张下载完成" % x)

#加载浏览器
driver=webdriver.Chrome(executable_path="/Library/chromedriver")
#driver.PhantomJS(executable_path="/Library/phantomjs-2.1.1-macosx/bin/phantomjs")
#打开选取的省份（北京、安徽、陕西）
URL=["https://www.mafengwo.cn/jd/10065/gonglve.html",
    "https://www.mafengwo.cn/jd/12719/gonglve.html",
    "https://www.mafengwo.cn/jd/13083/gonglve.html"]
driver.get(URL[0])
#打开景点
time.sleep(1.5)
pois=driver.find_elements_by_class_name("rev-total")
pois[0].click()
#打开获取景点图片页URL
driver.switch_to.window(driver.window_handles[1])
ss=driver.current_url
url=ss[0:24]+'photo/'+ss[24:]
driver.get(url)
#打开大图
time.sleep(1.5)
driver.find_element_by_class_name("a-pic").click()
driver.switch_to.window(driver.window_handles[2])
root_dir = os.path.dirname(os.path.abspath('.'))
path = root_dir+"/docs/pic/beijing/"

#下载前9张大图
for i in range(1,10):
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("s-pic"))
    except:
        print("加载图片超时")
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME,("s-next"))))
    except:
        print("寻找下一张图片超时")
    driver.find_element_by_class_name("s-next").click()
    posi=driver.find_element_by_xpath('//*[@id="_j_stageimg"]').get_attribute('src')
    try:
        saveImg(posi,path,i)
    except:
        print("图片保存失败")
