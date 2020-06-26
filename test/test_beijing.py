import json
import time
import re
from selenium import webdriver
import pandas as pd
from pandas import DataFrame
import numpy as np
from selenium.webdriver.common.keys import Keys

path='D:\Software\chromedriver\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)
driver.get("https://www.mafengwo.cn/mdd/")
city_name='北京'
dic={}
driver.find_element_by_class_name('search-input').send_keys(city_name)
driver.find_element_by_class_name('search-button').click()
driver.find_element_by_link_text('景点').click()
link=driver.find_elements_by_class_name('_j_search_link')
link=driver.find_elements_by_partial_link_text('景点 -')
jingdian=[]
for i in link[:5]:
    jingdian.append(i.get_attribute('href'))

    # j = 0
for place in jingdian:#top5景点
    # j = j+1
    # if j<=3:
    #     continue
    driver.get(place)
    time.sleep(2)
    # driver.wait(until.elementLocated(orgOpt))
    title=driver.find_element_by_class_name('title')
    # print(title)
    place_name=title.text.split('\n')
    print(place_name[0])#景点名
    dic[place_name[0]]={}
    sum = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/span/em')
    dic[place_name[0]]['总评论数'] = sum.text
    #----------------汇总信息------------------------------
    for i in range(2,6):
        xlablepath = '/ html / body / div[2] / div[4] / div / div / div[2] / ul / li['+str(i)+'] / a / span[1]'
        xcountpath = '/ html / body / div[2] / div[4] / div / div / div[2] / ul / li['+str(i)+'] / a / span[2]'
        key = driver.find_element_by_xpath(xlablepath).text
        value = driver.find_element_by_xpath(xcountpath).text
        dic[place_name[0]][key] = value

    for i in range(6, 12):
        xlablepath = '/html/body/div[2]/div[4]/div/div/div[2]/ul/li['+str(i)+']/a'
        xcountpath = xlablepath+'/span'
        key = driver.find_element_by_xpath(xlablepath).text.split('（')
        value = driver.find_element_by_xpath(xcountpath).text
        dic[place_name[0]][key[0]] = value
    # ----------------汇总信息------------------------------

    fenglei = ['好评', '中评', '差评']
    s = dic[place_name[0]]['差评']
    NumOfBadRe = re.findall(r"\d+", s)
    NumOfBadRes = int(NumOfBadRe[0]) # 差评数
    print(NumOfBadRes)
    if NumOfBadRes<75:
        fenglei = ['好评', '中评']
    for f in fenglei:
        print(f)
        driver.find_element_by_partial_link_text(f).click()
        username = []  # 用户名
        starlevel = []  # 评论星级
        times = []  # 评论时间
        comment = [] #评论内容
        for i in range(5):#五页
            if i != 0:
                driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[4]/div[2]/a[5]').click()
                time.sleep(5)

            # 用户名
            users = driver.find_elements_by_class_name('name')
            for u in users:
                username.append(u.text)

            # 评论星级
            for k in range(1,16):#每页15条评论
                xstarpath = '/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li['+str(k)+']/span'
                star = driver.find_element_by_xpath(xstarpath)
                sNumOfStar = star.get_attribute('class')
                NumOfStar = re.findall(r"\d", sNumOfStar)
                starlevel.append(int(NumOfStar[0]))#改

            Time = driver.find_elements_by_class_name('time')#时间
            for T in Time:
                if len(T.text) > 1:
                    times.append(T.text)

            # 评论内容
            reviews = driver.find_elements_by_class_name('rev-txt')
            for r in reviews:
                r = r.text
                r = r.replace('\n','')
                comment.append(r)
        username_array = np.array(username)[:, np.newaxis]
        starlevel_array = np.array(starlevel)[:, np.newaxis]
        times_array = np.array(times)[:, np.newaxis]
        comment_array = np.array(comment)[:, np.newaxis]
        concatenate_array = np.concatenate((username_array, starlevel_array, times_array[0:75], comment_array), axis=1)
        data = DataFrame(concatenate_array, columns=["用户名", "评论星级","评论时间", "评论内容"])
        filepath = './result/北京/'+place_name[0]+'/'+f+'.CSV'
        # writer = pd.ExcelWriter(filepath)
        print(filepath)
        data.to_csv(filepath, encoding='utf_8_sig')

    json_str = json.dumps(dic, ensure_ascii = False)
    summaryfilepath = './result/北京/'+place_name[0]+'/'+place_name[0]+'评论汇总'+'.json'
    with open(summaryfilepath, 'w') as json_file:
        json_file.write(json_str)
driver.close()


