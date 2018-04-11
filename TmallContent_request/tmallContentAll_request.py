"""
商品信息
"""
import re
import time
import urllib
from random import uniform
from urllib.error import HTTPError

import requests
from bs4 import BeautifulSoup
from pip._vendor.retrying import retry
from selenium.common.exceptions import NoSuchElementException
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

headers = {'Host': 'detail.tmall.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://list.tmall.com/search_product.htm?q=%CF%B4%D2%C2%D2%BA&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&xl=xiyiye_1&from=mallfp..pc_1_suggest',
            'Cookie': 'isg=AgsLXuk41hirMAtSpG3H4h5vm681CB3IM6dl9X0Io8qhnCv-BXCvcqk2AKeM; cna=IrdbERkyLB4CAXHh2Ea/wiwF; l=AgcHYmF30Z8B-d6QcmfLPr5Xl7HSQtrQ; cq=ccp%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; sm4=210100; pnm_cku822=098%23E1hv29vUvbpvUpCkvvvvvjiPP2dp1jEVP25ptj1VPmPUgjnvP2LWtjEbRLLUtji2RvyCvhQWFlZvCzPxAfev%2BulsbSoxfwoKHkx%2FAjc6D46XjL4xfw1lHdUf8jc6D764degmDfea6Lp7EcqhaNoxdXyaWWoQD70Xd56OfwCl3ETAuphvmvvv9mMY4%2BS0kphvC9QvvOClpbyCvm9vvvvvphvvvvvv96CvpvQKvvm2phCvhRvvvUnvphvppvvv963vpCmvvphvC9vhvvCvpvGCvvpYjRIERphvCvvvvvm5vpvhvvmv99%3D%3D; uss=BvcmJsN2Lg8VP96ydnWDvHjXy%2B%2BgyFwTfsWWcCPQQy1i0n%2BMQYfQ5Hbn%2BA%3D%3D; tk_trace=1; uc1=cookie14=UoTcCfQkkLf%2Fmg%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7oPIg&tag=8&cookie15=WqG3DMC9VAQiUQ%3D%3D&pas=0; uc3=sg2=U7f2wdEPk7GDMX%2FM25d4ID1QuFCf%2FIksRUfBlSnU%2FKQ%3D&nk2=1z6Ehu9TJVE%3D&id2=UNQ2ltmCm8K1WA%3D%3D&vt3=F8dBzWk%2BT6HjyG5FFGk%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; tracknick=%5Cu6253%5Cu8001%5Cu864E%5Cu00B7; _l_g_=Ug%3D%3D; unb=3416958410; lgc=%5Cu6253%5Cu8001%5Cu864E%5Cu00B7; cookie1=U7lUrnJnINE2VCdRljoDY9jOu2DasfcjF3YmxT%2BBnjs%3D; login=true; cookie17=UNQ2ltmCm8K1WA%3D%3D; cookie2=3f47a348194e88049c30a7058db7de6f; _nk_=%5Cu6253%5Cu8001%5Cu864E%5Cu00B7; t=1d8219bf9181116ffb9d47f9eedbcb85; sg=%C2%B709; _tb_token_=3ee49d4fbbb80; swfstore=212599; whl=-1%260%260%260',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'}

def get_id_list(collection_name):
    conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
    db = conn[MONGODB_DB]
    collection = db[collection_name]
    id_list = []
    cursor = collection.find({})

    for item in cursor:
        if "appended" not in item.keys():
            if 'removeTime' in item.keys():
                continue
            if 'aliyaofang' in item.keys():
                continue
            if '阿里大药房' in item.values():
                continue
            if '阿里健康大药房' in item.values():
                continue
            dic = {}
            dic['original_id'] = item['original_id']
            dic['href'] = item['href']
            dic['shop_name'] = item['shop_name']
            id_list.append(dic)

    cursor.close()
    conn.close()
    return id_list

def dealWithItem(attributes, name_dic, original_id, collection_name):
    conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
    db = conn[MONGODB_DB]
    collection = db[collection_name]

    cursor = collection.find({"original_id": original_id})
    res = list(cursor)
    doc = res[0]

    if len(res) == 1 and ('appended' not in doc.keys()):
        tag = {}
        tag["attributes"] = attributes
        tag['name'] = name_dic['name']
        tag['appended'] = True
        # tag["exit_tag"] = True
        #根据item_id 执行update: item_content,item_create_time,tag
        flag = int(collection.update({"original_id": original_id}, {"$set": tag})['ok'])
        if flag == 1:
            print(str(original_id)+":")
            print(tag)
            print(str(original_id)+"已插入属性++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    else:
        flag = 0
        print(str(original_id) + "未更改++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    cursor.close()
    conn.close()
    return flag


def tagRemovedItem(original_id, collection_name):
    conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
    db = conn[MONGODB_DB]
    collection = db[collection_name]
    removeTime = time.strftime("%d/%m/%Y")

    collection.update({'original_id': original_id}, {'$set': {'removeTime': removeTime}})
    conn.close()


def dealWithNames(str):
    name_dic = {}

    new_str = str.replace('\n', '').replace('\t', '').replace('\r', '').split('        ')[0]
    name_dic['name'] = new_str

    return name_dic


def dealWithAttributes(attribute_list):
    attribute_dict = {}
    # attribute_list = str.split('\n')
    for attribute in attribute_list:
        # if '产品参数' in attribute:
        #     continue
        #
        #
        # if '：' in attribute and ':' in attribute:
        #     a = re.split(':|：', attribute)
        #     attribute_dict[a[0]] = attribute.replace(a[0], '')
        if '：\xa0' in attribute:
            a = attribute.split('：\xa0')
            attribute_dict[a[0]] = a[1]
        elif ':\xa0' in attribute:
            a = attribute.split(':\xa0')
            attribute_dict[a[0]] = a[1]
        else:
            attribute_dict['description'] = attribute

    return attribute_dict


def setAliyaofang(original_id, collection_name):
    conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
    db = conn[MONGODB_DB]
    collection = db[collection_name]
    aliyaofang = True

    collection.update({'original_id': original_id}, {'$set': {'aliyaofang': aliyaofang}})
    conn.close()
def getContent(id_dic, collection_name, newOpener):
    # driver = WebDriver(executable_path='F:/phantomjs-2.1.1-windows/bin/phantomjs.exe', port=5003)

    url = id_dic['href']
    original_id = id_dic['original_id']
    print(id_dic)


    time.sleep(uniform(0.5, 2))
    try:
        # response = requests.request(method='GET', url=url, headers=headers, verify=False)
        # page_data = urllib.request.urlopen(url).read().decode('gbk', 'ignore')
        response = newOpener.open(url)
        # driver.get(url)
    except HTTPError:
        setAliyaofang(id_dic['original_id'], collection_name)
        return 0

    except Exception as e:
        print("访问异常" + str(e))
        print("当前item_id：" + str(original_id))
        raise

    try:
        page_data = response.read().decode('gbk')
        bs_obj = BeautifulSoup(page_data, 'lxml')
        name_str = bs_obj.find('div', {'class', 'tb-detail-hd'}).text
        tag_list = bs_obj.find('ul',  {'id': 'J_AttrUL'}).find_all('li')
        attribute_list = []
        for tag in tag_list:
            attribute_list.append(tag.text)



        # try:
        #     attributes_str = driver.find_element_by_xpath('//div[@class="content"]').text
        # except NoSuchElementException:
        # attributes_str = driver.find_element_by_xpath('//div[@class="mlh-content"]').text
    except AttributeError:
        if '天猫超市' == id_dic['shop_name']:
            name_dic = dealWithNames(name_str)
            return dealWithItem('', name_dic, original_id, collection_name)
        else:
            print('商品已经下架')
            tagRemovedItem(original_id, collection_name)
            return 0
    except UnicodeDecodeError:
        # raise
        tagRemovedItem(original_id, collection_name)
        return 0
    attribute_dict = dealWithAttributes(attribute_list)
    name_dic = dealWithNames(name_str)
    flag = dealWithItem(attribute_dict, name_dic, original_id, collection_name)
    return flag

def main(id_list, collection_name, newOpener):

    time.sleep(5)
    count = 0
    for i in range(len(id_list)):
        count = count + getContent(id_list[i], collection_name, newOpener)
        time.sleep(uniform(1, 5))


