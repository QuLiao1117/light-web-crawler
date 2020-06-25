import json
from selenium import webdriver

province_lis = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东',
                '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '西藏', '广西', '内蒙古', '宁夏', '新疆',
                '北京', '上海', '天津', '重庆', '香港', '澳门']


def get_place_top5_landmark_info(city_name):
    driver = webdriver.Chrome()
    driver.get("https://www.mafengwo.cn/mdd/")
    dic = {}
    driver.find_element_by_class_name('search-input').send_keys(city_name)
    driver.find_element_by_class_name('search-button').click()
    driver.find_element_by_link_text('景点').click()
    link = driver.find_elements_by_class_name('_j_search_link')
    link = driver.find_elements_by_partial_link_text('景点 -')
    jingdian = []
    for i in link[:5]:
        jingdian.append(i.get_attribute('href'))
    for place in jingdian:
        driver.get(place)
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
        dd = driver.find_elements_by_tag_name('dd')

        dic[place_name[0]]["交通"] = dd[0].text
        dic[place_name[0]]["门票"] = dd[1].text
        dic[place_name[0]]["开放时间"] = dd[2].text
    driver.close()
    json_str = json.dumps(dic)
    with open(".\\docs\\" + city_name + '.json', 'w') as json_file:
        json_file.write(json_str)


if __name__ == "__main__":
    for province in province_lis:
        get_place_top5_landmark_info(province)