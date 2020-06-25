#!/usr/bin/env python
# encoding=utf-8

from selenium import webdriver
import time
#加载浏览器
driver=webdriver.Chrome(executable_path="/Library/chromedriver")
#driver.PhantomJS(executable_path="/Library/phantomjs-2.1.1-macosx/bin/phantomjs")
driver.get("https://www.mafengwo.cn/")
time.sleep(1.5)
driver.find_element_by_id("_j_index_search_input_all").send_keys('北京')
driver.find_element_by_id("_j_index_search_btn_all").click()
time.sleep(1)
ret=driver.find_element(by="data-search-category",value="pois")
print(ret)
'''
time.sleep(5)
driver.close()
'''
