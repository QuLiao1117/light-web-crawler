"""一个从马蜂窝（http://www.mafengwo.cn/）网站抓取地区景点信息的脚本。

利用Selenium自动化操作，打开马蜂窝首页，使用搜索栏搜索地区。
在搜索结果中，查看该地区的景点，利用元素获取打开景点页面。
在景点页中，按元素和class获取景点的信息(中英文名称，地址，网址，电话，交通，门票)，并下载。

Args:
    LOCATIONS: 计划抓取图片的地区（需为准确的专有名词，即在马蜂窝中可直接搜索到）
    GET_LANDMARK_NUM: 计划在选定的地区抓取的景点数量
"""

import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

def get_place_top5_landmark_info(location, landmark_number=5):
    '''
    给定地点名，查找该地点排名前5的景点，将景点的信息写入json文件

    Args:
        location:地点名
        landmark_number:需要获取的top景点数目
    '''
    driver = webdriver.Chrome()
    driver.get("https://www.mafengwo.cn/mdd/")
    dic = {}
    driver.find_element_by_class_name('search-input').send_keys(location)
    driver.find_element_by_class_name('search-button').click()
    driver.find_element_by_link_text('景点').click()
    link = driver.find_elements_by_class_name('_j_search_link')
    link = driver.find_elements_by_partial_link_text('景点 -')
    jingdian = []
    for i in link[:landmark_number]:
        jingdian.append(i.get_attribute('href'))
    for place in jingdian:
        driver.get(place)
        try:
            WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_class_name("title"))
        except TimeoutException:
            raise TimeoutException("页面图片加载超时")
        title = driver.find_element_by_class_name('title')
        place_name = title.text.split('\n')
        dic[place_name[0]] = {}
        if len(place_name) > 1:
            dic[place_name[0]]["英文名"] = place_name[1]
        address = driver.find_element_by_class_name('sub').text  # 地址
        dic[place_name[0]]["地址"] = address
        content = driver.find_elements_by_class_name('content')
        label = driver.find_elements_by_class_name('label')
        for i in range(len(label)):
            dic[place_name[0]][label[i].text] = content[i + 1].text
        dd_content = driver.find_elements_by_tag_name('dd')

        dic[place_name[0]]["交通"] = dd_content[0].text
        dic[place_name[0]]["门票"] = dd_content[1].text
        dic[place_name[0]]["开放时间"] = dd_content[2].text
    driver.close()
    json_str = json.dumps(dic, ensure_ascii=False)
    with open("..\\docs\\city_landmark_info\\" + location + '.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


if __name__ == "__main__":
    LOCATIONS = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建',
                 '江西', '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州',
                 '云南', '陕西', '甘肃', '青海', '台湾', '西藏', '广西', '内蒙古', '宁夏',
                 '新疆', '北京', '上海', '天津', '重庆', '香港', '澳门']
    GET_LANDMARK_NUM = 5
    for loc in LOCATIONS:
        get_place_top5_landmark_info(loc, landmark_number=GET_LANDMARK_NUM)
