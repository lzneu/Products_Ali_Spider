# -*- coding: UTF-8 -*-
import pandas as pd
from pymongo import MongoClient
from Config.config import *
# import tkinter


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if isLocal:
        if username and password:
            # print('mongo username')
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
            conn = MongoClient(mongo_uri)
        else:
            # print('mongo no username')
            conn = MongoClient(host, port)
    else:
         #获取mongoclient
        conn = MongoClient([Mongo_CONN_ADDR1, Mongo_CONN_ADDR2], replicaSet=Mongo_REPLICAT_SET)
        if username and password:
            #授权. 这里的user基于admin数据库授权
            conn.admin.authenticate(username, password)

    return conn


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """
    from pymongo import DESCENDING as mongoDescending
    # Connect to MongoDB
    conn = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    dataBase = conn[db]
    # Make a query to the specific DB and Collection.sort({"creationTime":1}
    cursor = dataBase[collection].find(query) #.limit(1000)#.sort('creationTime',direction =mongoDescending)
    # cursor = dataBase['dafafa'].find(query)
    # print(cursor)

    # cursor = db[collection].find({'platform':1})  #条件查找
    # cursor = db[collection].find()  # 查到所有
    # print (cursor)
    # print('dkdkk', list(cursor))
    df = pd.DataFrame(list(cursor))
    # print(df)
    if(len(list(cursor))>0):   #数据量为0 返回 Empty DataFrame
        # Expand the cursor and construct the DataFrame
        for i in range(0,len(df.columns)):
            pass
            # print ('kslsk', df.columns[i] ,i)
        # Delete the _id
        if no_id:
            # print('删除')
            del df['_id']

    cursor.close()
    conn.close()
    return df
''''连接mongodb, 返回mongodb的connnection
'''''
def connect_mongo(host, port, username, password):
    """ A util for making a connection to mongo """

    if isLocal:
        if username and password:
            # print('mongo username')
            mongo_uri = 'mongodb://%s:%s@%s:%s' % (username, password, host, port)
            conn = MongoClient(mongo_uri)
        else:
            # print('mongo no username')
            conn = MongoClient(host, port)
    else:
         #获取mongoclient
        conn = MongoClient([Mongo_CONN_ADDR1, Mongo_CONN_ADDR2], replicaSet=Mongo_REPLICAT_SET)
        if username and password:
            #授权. 这里的user基于admin数据库授权
            conn.admin.authenticate(username, password)
    return conn