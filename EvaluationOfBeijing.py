import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
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
for place in jingdian:
    driver.get(place)
    title=driver.find_element_by_class_name('title')
    place_name=title.text.split('\n')
    dic[place_name[0]]={}
    if len(place_name)>1:
        dic[place_name[0]]["英文名"]=place_name[1]
    address=driver.find_element_by_class_name('sub').text#地址
    dic[place_name[0]]["地址"]=address
    content=driver.find_elements_by_class_name('content')
    label=driver.find_elements_by_class_name('label')
    for i in range(len(label)):
        dic[place_name[0]][label[i].text]=content[i+1].text
    dd=driver.find_elements_by_tag_name('dd')
    dic[place_name[0]]["交通"]=dd[0].text
    dic[place_name[0]]["门票"]=dd[1].text
    dic[place_name[0]]["开放时间"]=dd[1].text
json_str = json.dumps(dic)
with open(".\\docs\\"+city_name+'.json', 'w') as json_file:
    json_file.write(json_str)