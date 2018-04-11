import time
from multiprocessing import Process
from random import uniform

from pymongo import MongoClient


from Config.config import *
from Models import GetProxy, Login
from Models.Login import Taobao
from TmallContent_request import tmallContentAll_request_append_name
from TmallContent_request.tmallContentAll_request_append_name import get_id_list

if __name__ == '__main__':

    mongo_conn = MongoClient(mongodb_host, mongodb_port)

    db = mongo_conn['power']
    collection_name_list = db.collection_names()
    print(len(collection_name_list))
    # 取出TM_XY_前缀的集合名称
    collection_name_list1 = []
    for collection_name in collection_name_list:
        if 's_TM_HF_脸部润肤' in collection_name and len(collection_name.split('_')) == 5:
            collection_name_list1.append(collection_name)

    for collection_name in collection_name_list1:
        print(collection_name)
        while 1:
            try:
                id_list = get_id_list(collection_name)
                print('采集：' + collection_name)
                print('未采集商品数： ————' + str(len(id_list)))

                res = Taobao().main()
                if len(id_list) != 0:
                    p = Process(target=tmallContentAll_request_append_name.main(id_list, collection_name, res), args=(id_list, collection_name, res,))
                    p.start()
                    p.join()
                else:
                    print('完成')
                    break
            except Exception as e:
                print("崩溃！ 重启程序！")
                time.sleep(15)