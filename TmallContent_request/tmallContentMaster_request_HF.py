import time
from multiprocessing import Process
from random import uniform

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.support import ui

from Config.Tmall_Products_Config import urls_collections_config
from Config.config import *
from Models import GetProxy, Login
from Models.Login import Taobao
from TmallContent_request import tmallContentAll_request
from TmallContent_request.tmallContentAll_request import get_id_list
from Tools import loginTmall

if __name__ == '__main__':

    mongo_conn = MongoClient(mongodb_host, mongodb_port)

    db = mongo_conn['power']
    collection_name_list = db.collection_names()
    print(len(collection_name_list))
    # 取出TM_XY_前缀的集合名称
    collection_name_list1 = ['s_TM_MZ_唇妆_润唇膏啫喱',
                             's_TM_MZ_唇妆_唇膜',  ##
                             's_TM_MZ_眼妆_眼线',
                             's_TM_MZ_眼妆_眼影',
                             's_TM_HF_身体清洁_搓泥浴宝',
                             's_TM_HF_身体清洁_磨砂浴盐',
                             's_TM_HF_身体清洁_沐浴啫喱',
                             's_TM_HF_身体护理_润肤水喷雾',
                             's_TM_HF_身体护理_精油',  ##
                             's_TM_HF_身体护理_抑汗香氛', ##
                             's_TM_HF_身体护理_其他',
                             's_TM_MZ_底妆_遮瑕膏笔',
                             's_TM_MZ_底妆_修容高光阴影粉']


    for collection_name in collection_name_list1:

        while 1:
            try:
                id_list = get_id_list(collection_name)
                print('采集：' + collection_name)
                print('未采集商品数： ————' + str(len(id_list)))

                res = Taobao().main()
                if len(id_list) != 0:
                    p = Process(target=tmallContentAll_request.main(id_list, collection_name, res), args=(id_list, collection_name, res,))
                    p.start()
                    p.join()
                else:
                    print('完成')
                    break
            except Exception as e:
                print("崩溃！ 重启程序！")
                time.sleep(15)