import time
from random import uniform

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.support import ui

from Config.config import *
import pymongo
import xlrd

from Tools import loginTaobao, loginTmall
from Config.Tmall_Products_Config import urls_collections_config

def get_id_list(collection_name):
    conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
    db = conn[MONGODB_DB]
    collection = db[collection_name]
    id_list = []
    cursor = collection.find({})
    for item in cursor:
        if "attributes" not in item.keys():
            id_list.append(item['product_id'])
    cursor.close()
    conn.close()
    return id_list

def getUrl(id):
    return 'https://detail.tmall.com/item.htm?spm=a220o.1000855.w4023-14438540921.4.5c90c3485rvz5X&id='+str(id)

def dealWithItem(attributes, product_id, collection_name):
    conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
    db = conn[MONGODB_DB]
    collection = db[collection_name]

    cursor = collection.find({"product_id": product_id})
    res = list(cursor)
    doc = res[0]

    if len(res) == 1 and (not 'attributes' in doc.keys()):
        tag = {}
        tag["attributes"] = attributes
        # tag["exit_tag"] = True
        #根据item_id 执行update: item_content,item_create_time,tag
        flag = int(collection.update({"product_id": product_id}, {"$set": tag})['ok'])
        if flag == 1:
            print(str(product_id)+":")
            print(tag)
            print(str(product_id)+"已插入属性++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    else:
        flag = 0
        print(str(product_id) + "未更改++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    cursor.close()
    conn.close()
    return flag

    conn.close()

def removeItem(item_id):
    conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
    db = conn[MONGODB_DB]
    collection = db[MONGODB_ITEM_COLLECTION]
    collection.remove({'item_id': item_id})
    conn.close()

def dealWithAttributes(str):
    attribute_dict = {}
    attribute_list = str.split('\n')
    attribute_dict['description'] = ''
    for attribute in attribute_list:
        if '：' in attribute:
            a = attribute.split('：')
            attribute_dict[a[0]] = a[1]
        elif ':' in attribute:
            a = attribute.split(':')
            attribute_dict[a[0]] = a[1]
        else:
            attribute_dict['description']+attribute

    return attribute_dict

def getContent(product_id, driver, collection_name):
    print("采集id:"+str(product_id))

    url = getUrl(product_id)
    time.sleep(uniform(5, 10))
    print(url)
    try:
        driver.get(url)
    except Exception as e:
        print("浏览器访问异常" + str(e))
        print("当前item_id：" + str(product_id))
        raise
    # time.sleep(uniform(0.5, 1.5))
    # 获得selenium.webdriver.firefox.webelement.FirefoxWebElement列表

    time.sleep(uniform(3, 5))
    driver.implicitly_wait(20)
    driver.execute_script("scrollTo(0,1000)")
    time.sleep(uniform(3, 5))
    driver.execute_script("scrollTo(0,5000)")
    time.sleep(uniform(3, 5))
    driver.execute_script("scrollTo(0,10000)")
    time.sleep(uniform(3, 5))
    driver.execute_script("scrollTo(0,30000)")
    time.sleep(uniform(3, 5))
    try:
        attributes_str = driver.find_elements_by_xpath('//*[@id="J_AttrUL"]')[0].text
    except Exception as e:
        try:
            attributes_str = driver.find_element_by_xpath('//div[@class="mlh-content"]').text

        except Exception as e:
            attributes_str = driver.find_element_by_xpath('//div[@id="description"]').text

    attributes = dealWithAttributes(attributes_str)
    flag = dealWithItem(attributes, product_id, collection_name)
    return flag

def main(id_list, collection_name):
    driver = WebDriver(executable_path='F:/phantomjs-2.1.1-windows/bin/phantomjs.exe', port=5003)
    ui.WebDriverWait(driver, 10)
    # firefox_capabilities = DesiredCapabilities.FIREFOX
    # driver = webdriver.Firefox(capabilities=firefox_capabilities, executable_path='F:/py_enviroment/Library/bin/geckodriver')
    # wait = ui.WebDriverWait(driver, 10)
    count = 0

    for i in range(len(id_list)):
        try:
            count = count + getContent(id_list[i], driver, collection_name)
        except:
            driver.quit()
            raise
