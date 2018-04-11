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
    collection_name_list1 = []
    for collection_name in collection_name_list:
        if 'TM_XF' in collection_name and len(collection_name.split('_')) == 4:
            collection_name_list1.append(collection_name)

    for collection_name in collection_name_list1:

        while 1:
            try:
                id_list = get_id_list(collection_name)
                print('采集：' + collection_name)
                print('未采集商品数： ————' + str(len(id_list)))
                # driver = WebDriver(executable_path='F:/phantomjs-2.1.1-windows/bin/phantomjs.exe')
                # ui.WebDriverWait(driver, 10)
                # firefox_capabilities = DesiredCapabilities.FIREFOX
                # firefox_capabilities['marionette'] = True
                # driver = webdriver.Firefox(capabilities=firefox_capabilities,
                #                    executable_path='F:/geckodriver')
                # driver = loginTmall.login_tmall()
                newOpener = Taobao().main()
                if len(id_list) != 0:
                    p = Process(target=tmallContentAll_request.main(id_list, collection_name, newOpener), args=(id_list, collection_name, newOpener,))
                    p.start()
                    p.join()
                else:
                    print('完成')
                    break
            except Exception as e:

                print("崩溃！ 重启程序！")
                time.sleep(10)