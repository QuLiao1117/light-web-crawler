"""一个从马蜂窝（http://www.mafengwo.cn/）网站抓取评论信息的脚本。
利用Selenium自动化操作，打开马蜂窝首页，使用搜索栏搜索地区。
在搜索结果中，查看该地区的景点，利用元素获取打开景点页面。
在景点页中，按元素和class获取评论并下载。
Args:
    LOCATIONS: 计划抓取评论的地区（需为准确的专有名词，即在马蜂窝中可直接搜索到）
    GET_LANDMARK_NUM: 计划在选定的地区抓取的景点数量
"""

import json
import os
import re
import time
from pathlib import Path, PureWindowsPath

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


def get_place_top5_comments(location, driver, landmark_number=5, save_path=os.path.abspath('.')):
    """
        给定地点名，查找该地点排名前5的景点，将景点的信息写入json文件
        Args:
            location:地点名
            driver : 一个Selenium浏览器对象
            landmark_number:需要获取的top景点数目
            save_path: 保存路径
    """
    # 加载浏览器，括号为浏览器连接程序位置（默认为python.exe文件位置），需要与本机安装的浏览器版本一致
    # driver = webdriver.Chrome()
    driver.get("https://www.mafengwo.cn/mdd/")
    # 模拟浏览器搜索要爬取的城市
    driver.find_element_by_class_name('search-input').send_keys(location)
    driver.find_element_by_class_name('search-button').click()
    driver.find_element_by_link_text('景点').click()
    link = driver.find_elements_by_class_name('_j_search_link')
    link = driver.find_elements_by_partial_link_text('景点 -')
    # 保存top5景点的五个链接
    jingdian = []
    for i in link[:landmark_number]:
        jingdian.append(i.get_attribute('href'))
    # 遍历五个景点，分别爬取
    for place in jingdian:
        driver.get(place)
        try:
            WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_class_name("title"))
        except TimeoutException:
            raise TimeoutException("页面加载超时")
        title = driver.find_element_by_class_name('title')
        # 获得景点名称
        place_name = title.text.split('\n')
        dic = {}
        # 总评论数
        sum_comment = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div'
                                                   '/div/div[1]/span/em')
        dic['总评论数'] = sum_comment.text
        # 分别获得"有图"、"好评"、"中评"、"差评"的评论条数信息
        for i in range(2, 6):
            xlablepath = '/ html / body / div[2] / div[4] / div / div ' \
                         '/ div[2] / ul / li[' + str(i) + '] / a / span[1]'
            xcountpath = '/ html / body / div[2] / div[4] / div / div / ' \
                         'div[2] / ul / li[' + str(i) + '] / a / span[2]'
            key = driver.find_element_by_xpath(xlablepath).text
            value = driver.find_element_by_xpath(xcountpath).text
            dic[key] = value
        # 分别获得其他类型的评论条数信息
        for i in range(6, 11):
            xlablepath = '/html/body/div[2]/div[4]/div/div/div[2]/ul/li[' + str(i) + ']/a'
            xcountpath = xlablepath + '/span'
            key = driver.find_element_by_xpath(xlablepath).text.split('（')
            value = driver.find_element_by_xpath(xcountpath).text
            dic[key[0]] = value
        # 获得金牌点评数的信息、
        xlablepath = '/ html / body / div[2] / div[4] / div / div ' \
                     '/ div[2] / ul / li[11] / a / span[1]'
        xcountpath = '/ html / body / div[2] / div[4] / div / div / ' \
                     'div[2] / ul / li[11] / a / span[2]'
        key = driver.find_element_by_xpath(xlablepath).text
        value = driver.find_element_by_xpath(xcountpath).text
        dic[key] = value

        fenglei = ['好评', '中评', '差评']
        # 检测差评数
        strs = dic['差评']
        # 正则表达式识别数字
        num_of_bad_re = re.findall(r"\d+", strs)
        num_of_bad_res = int(num_of_bad_re[0])  # 差评数
        if num_of_bad_res < 75:
            fenglei.remove('差评')
        # 检测中评数
        strss = dic['中评']
        # 正则表达式识别数字
        num_of_middle_re = re.findall(r"\d+", strss)
        num_of_middle_res = int(num_of_middle_re[0])  # 差评数
        if num_of_middle_res < 75:
            fenglei.remove('中评')
        # 按好评中评差评分别爬取
        for elem in fenglei:
            # print(f)
            driver.find_element_by_partial_link_text(elem).click()
            username = []  # 用户名
            starlevel = []  # 评论星级
            times = []  # 评论时间
            comment = []  # 评论内容
            for i in range(5):  # 五页
                # 实现翻页
                if i != 0:
                    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div'
                                                 '/div/div[4]/div[2]/a[5]').click()
                    time.sleep(5)

                # 用户名爬取
                users = driver.find_elements_by_class_name('name')
                for user in users:
                    username.append(user.text)

                # 评论星级爬取
                for k in range(1, 16):  # 每页15条评论
                    xstarpath = '/html/body/div[2]/div[4]/div/div/div[4]/div[1]' \
                                '/ul/li[' + str(k) + ']/span'
                    star = driver.find_element_by_xpath(xstarpath)
                    s_num_of_star = star.get_attribute('class')
                    # 正则表达式识别数字
                    num_of_star = re.findall(r"\d", s_num_of_star)
                    starlevel.append(int(num_of_star[0]))

                # 评论时间数据的爬取
                date = driver.find_elements_by_class_name('time')
                for dat in date:
                    if len(dat.text) > 1:
                        times.append(dat.text)

                # 评论内容的爬取
                reviews = driver.find_elements_by_class_name('rev-txt')
                for rev in reviews:
                    rev = rev.text
                    rev = rev.replace('\n', '')
                    comment.append(rev)

            # 保存到文件
            username_array = np.array(username)[:, np.newaxis]
            starlevel_array = np.array(starlevel)[:, np.newaxis]
            times_array = np.array(times)[:, np.newaxis]
            comment_array = np.array(comment)[:, np.newaxis]
            concatenate_array = np.concatenate((username_array, starlevel_array,
                                                times_array[0:75], comment_array), axis=1)
            data = pd.DataFrame(concatenate_array, columns=["用户名", "评论星级", "评论时间", "评论内容"])
            file_path = Path(save_path + '/' + location + '/' + place_name[0] + '/')
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            summary_filename = file_path / (elem + '.CSV')
            correct_path = Path(summary_filename)
            data.to_csv(correct_path, encoding='utf_8_sig')
        json_str = json.dumps(dic, ensure_ascii=False)
        file_path = Path(save_path + '/' + location + '/' +
                           place_name[0] + '/')
        summary_filepath = file_path / (place_name[0] + '各类评论数统计' + '.json')
        correct_path = Path(summary_filepath)
        with open(correct_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_str)


# 执行脚本
if __name__ == "__main__":
    # 参数
    LOCATIONS = ['陕西', '北京', '安徽']  # 爬取地点
    GET_LANDMARK_NUM = 5  # 爬取景点数
    BROWSER_OBJ = webdriver.Chrome()  # 加载浏览器，括号为浏览器连接程序位置（默认为python.exe文件位置），需要与本机安装的浏览器版本一致
    ROOT_DIR = os.path.dirname(os.path.abspath('.')) + '/docs/comments' # 图片保存的根路径
    print(ROOT_DIR)
    # 循环下载
    for loc in LOCATIONS:
        get_place_top5_comments(loc, BROWSER_OBJ, GET_LANDMARK_NUM, ROOT_DIR)  # 调用函数爬取
    BROWSER_OBJ.close()

