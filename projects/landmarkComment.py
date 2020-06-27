import json
import time
import re
from selenium import webdriver
import pandas as pd
from pandas import DataFrame
import numpy as np
from selenium.webdriver.common.keys import Keys

citynames = ['陕西','安徽', '北京']

def get_place_top5_comments(city_name):#爬取'city_name'城市的top5的景点评论信息
    # path = 'D:\Software\chromedriver\chromedriver_win32\chromedriver.exe'
    path = '.\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)
    driver.get("https://www.mafengwo.cn/mdd/")
    #模拟浏览器搜索要爬取的城市
    driver.find_element_by_class_name('search-input').send_keys(city_name)
    driver.find_element_by_class_name('search-button').click()
    driver.find_element_by_link_text('景点').click()
    link=driver.find_elements_by_class_name('_j_search_link')
    link=driver.find_elements_by_partial_link_text('景点 -')
    #保存top5景点的五个链接
    jingdian=[]
    for i in link[:5]:
        jingdian.append(i.get_attribute('href'))

    #遍历五个景点，分别爬取
    for place in jingdian:
        driver.get(place)
        time.sleep(5)
        # driver.wait(until.elementLocated(orgOpt))
        title=driver.find_element_by_class_name('title')
        # print(title)
        #获得景点名称
        place_name=title.text.split('\n')
        #print(place_name[0])#景点名
        dic={}
        # ----------------汇总信息--------------------------------------------------------------------------------------
            #总评论数
        sum = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/span/em')
        dic['总评论数'] = sum.text
            #分别获得"有图"、"好评"、"中评"、"差评"的评论条数信息
        for i in range(2,6):
            xlablepath = '/ html / body / div[2] / div[4] / div / div / div[2] / ul / li['+str(i)+'] / a / span[1]'
            xcountpath = '/ html / body / div[2] / div[4] / div / div / div[2] / ul / li['+str(i)+'] / a / span[2]'
            key = driver.find_element_by_xpath(xlablepath).text
            value = driver.find_element_by_xpath(xcountpath).text
            dic[key] = value
            # 分别获得其他类型的评论条数信息
        for i in range(6, 11):
            xlablepath = '/html/body/div[2]/div[4]/div/div/div[2]/ul/li['+str(i)+']/a'
            xcountpath = xlablepath+'/span'
            key = driver.find_element_by_xpath(xlablepath).text.split('（')
            value = driver.find_element_by_xpath(xcountpath).text
            dic[key[0]] = value
        # 获得金牌点评数的信息、
        xlablepath = '/ html / body / div[2] / div[4] / div / div / div[2] / ul / li[11] / a / span[1]'
        xcountpath = '/ html / body / div[2] / div[4] / div / div / div[2] / ul / li[11] / a / span[2]'
        key = driver.find_element_by_xpath(xlablepath).text
        value = driver.find_element_by_xpath(xcountpath).text
        dic[key] = value

        fenglei = ['好评', '中评', '差评']
        #--------------------检测差评数---------------------------------------------------------------------------------
        s = dic['差评']
            # 正则表达式识别数字
        NumOfBadRe = re.findall(r"\d+", s)
        NumOfBadRes = int(NumOfBadRe[0]) # 差评数
        print(NumOfBadRes)
        if NumOfBadRes<75:
            fenglei.remove('差评')
        # --------------------检测中评数--------------------------------------------------------------------------------
        s = dic['中评']
            # 正则表达式识别数字
        NumOfBadRe = re.findall(r"\d+", s)
        NumOfBadRes = int(NumOfBadRe[0])  # 差评数
        print(NumOfBadRes)
        if NumOfBadRes < 75:
            fenglei.remove('中评')
        # 按好评中评差评分别爬取
        for f in fenglei:
            # print(f)
            driver.find_element_by_partial_link_text(f).click()
            username = []  # 用户名
            starlevel = []  # 评论星级
            times = []  # 评论时间
            comment = [] #评论内容
            for i in range(5):#五页
                #实现翻页
                if i != 0:
                    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[4]/div[2]/a[5]').click()
                    time.sleep(5)

                # 用户名爬取
                users = driver.find_elements_by_class_name('name')
                for u in users:
                    username.append(u.text)

                # 评论星级爬取
                for k in range(1,16):#每页15条评论
                    xstarpath = '/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li['+str(k)+']/span'
                    star = driver.find_element_by_xpath(xstarpath)
                    sNumOfStar = star.get_attribute('class')
                    #正则表达式识别数字
                    NumOfStar = re.findall(r"\d", sNumOfStar)
                    starlevel.append(int(NumOfStar[0]))

                # 评论时间数据的爬取
                Time = driver.find_elements_by_class_name('time')
                for T in Time:
                    if len(T.text) > 1:
                        times.append(T.text)

                # 评论内容的爬取
                reviews = driver.find_elements_by_class_name('rev-txt')
                for r in reviews:
                    r = r.text
                    r = r.replace('\n','')
                    comment.append(r)

            #------------------保存到文件--------------------------------------------------------------------------------
            username_array = np.array(username)[:, np.newaxis]
            starlevel_array = np.array(starlevel)[:, np.newaxis]
            times_array = np.array(times)[:, np.newaxis]
            comment_array = np.array(comment)[:, np.newaxis]
            concatenate_array = np.concatenate((username_array, starlevel_array, times_array[0:75], comment_array), axis=1)
            data = DataFrame(concatenate_array, columns=["用户名", "评论星级","评论时间", "评论内容"])
            filepath = './docs/comments'+'/'+city_name+'/'+place_name[0]+'/'+f+'.CSV'
            # writer = pd.ExcelWriter(filepath)
            print(filepath)
            data.to_csv(filepath, encoding='utf_8_sig')

        json_str = json.dumps(dic, ensure_ascii = False)
        summaryfilepath = './docs/comments' + '/' + city_name +'/'+place_name[0]+'/' + place_name[0] + '各类评论数统计' + '.json'
        with open(summaryfilepath, 'w') as json_file:
            json_file.write(json_str)
                #------------------保存到文件-------------------------------------------------------------------------------
    driver.close()

if __name__ == "__main__":
    for city_name in citynames:
        get_place_top5_comments(city_name)