# coding: utf-8

import time
import urllib
import urllib.request
from random import uniform

import xlrd

from Config.config import *
from lxml import etree
import pymongo
from bs4 import BeautifulSoup
import requests
import random
import telnetlib

def savedProxy():
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['ProxysLog']
    collection = db['proxys']
    cursor = collection.find().sort('getTime', pymongo.DESCENDING).limit(1)
    proxy_list = list(cursor)[0]['proxyList']

    cursor.close()
    conn.close()
    return proxy_list

def insertLog(oneDic):
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['ProxysLog']
    collection = db['proxys']
    collection.insert(oneDic)

def getProxyIp(current_time):
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['ProxysLog']
    collection = db['proxys']
    cursor = collection.find().sort('getTime', pymongo.DESCENDING).limit(1)
    res = list(cursor)
    if len(res) != 0:
        last_time = res[0]['getTime']
        cursor.close()
        conn.close()
    else:
        proxy = []
        for i in range(1, 3):
            print(i)
            header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Ubuntu Chromium/44.0.2403.89 '
                                    'Chrome/44.0.2403.89 '
                                    'Safari/537.36'}
            req = urllib.request.Request(url='http://www.xicidaili.com/nt/{0}'.format(i), headers=header)
            r = urllib.request.urlopen(req)
            soup = BeautifulSoup(r, 'html.parser', from_encoding='utf-8')
            table = soup.find('table', attrs={'id': 'ip_list'})
            tr = table.find_all('tr')[1:]

            for item in tr:
                tds = item.find_all('td')
                temp_dict = {}
                kind = "{0}:{1}".format(tds[1].get_text().lower(), tds[2].get_text())
                proxy.append(kind)
        oneDic = {}
        oneDic['getTime'] = time.time()
        oneDic['proxyList'] = proxy
        insertLog(oneDic)
        return proxy

    time_span = current_time - last_time
    if time_span >= 1800:

        proxy = []
        for i in range(1, 3):
            print(i)
            header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                   'Ubuntu Chromium/44.0.2403.89 '
                                                   'Chrome/44.0.2403.89 '
                                                   'Safari/537.36'}
            req = urllib.request.Request(url='http://www.xicidaili.com/nt/{0}'.format(i), headers=header)
            r = urllib.request.urlopen(req)
            soup = BeautifulSoup(r, 'html.parser', from_encoding='utf-8')
            table = soup.find('table', attrs={'id': 'ip_list'})
            tr = table.find_all('tr')[1:]


            for item in tr:
                tds =  item.find_all('td')
                temp_dict = {}
                kind = "{0}:{1}".format(tds[1].get_text().lower(), tds[2].get_text())
                proxy.append(kind)
        oneDic = {}
        oneDic['getTime'] = time.time()
        oneDic['proxyList'] = proxy
        insertLog(oneDic)
        return proxy
    else:
        return savedProxy()

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append(ip)
    proxy_ip = random.choice(proxy_list)

    proxies = {'http': proxy_ip}
    try:
        requests.get('https://www.jd.com/', headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}, proxies=proxies)
    except Exception as e:
        print(e.args)
        print(e)
        return get_random_ip(ip_list)
    else:
        proxies = {'http': proxy_ip}
        return proxy_ip





#获取页面html
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                                           'Ubuntu Chromium/44.0.2403.89 '
                                           'Chrome/44.0.2403.89 '
                                           'Safari/537.36'}
def brash(proxy_dict):

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                                           'Ubuntu Chromium/44.0.2403.89 '
                                           'Chrome/44.0.2403.89 '
                                           'Safari/537.36'}
    proxy_handler = urllib.request.ProxyHandler({'http': proxy_dict})
    opener = urllib.request.build_opener(proxy_handler)
    # urllib.request.install_opener(opener)

    return opener


def main(current_time):
    ip_list = getProxyIp(current_time)
    proxy_ip = get_random_ip(ip_list)
    print(proxy_ip)
    return proxy_ip
