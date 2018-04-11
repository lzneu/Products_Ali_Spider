import time
from multiprocessing import Process
from random import uniform
from threading import Thread

from Config.Tmall_Products_Config import urls_collections_config
from TmallContentSpider import tmallContentAll
from TmallContentSpider.tmallContentAll import get_id_list


def oneProcess(collection_name):
    while 1:
        try:
            id_list = get_id_list(collection_name)
            print('采集：' + collection_name)
            if len(id_list) != 0:
                thread = Thread(target=tmallContentAll.main, args=(id_list, collection_name,))
                thread.start()
                thread.join()
            else:
                print('完成')
                break
        except Exception as e:
            print(e.args)

            print("崩溃！ 重启程序！")
            time.sleep(uniform(1, 2))
    print('done...')

if __name__ == '__main__':

    key_list = []
    for cat in urls_collections_config.keys():
        key = urls_collections_config[cat][1]
        key_list.append(key)

    proc_record = []

    for i in range(len(key_list)):
        print(key_list[i])
        p = Process(target=oneProcess, args=(key_list[i],))
        p.start()
        proc_record.append(p)

    for p in proc_record:
        p.join()
