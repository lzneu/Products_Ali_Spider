#coding=UTF-8
from datetime import datetime, tzinfo, timedelta
import time
import numpy as np

import pytz

class UTC(tzinfo):
    """UTC"""
    def __init__(self,offset = 0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)

''''时间字符串转换为mongodb时间
'''''
def convertTimeStringToDateTime(timeStr):
    structed_time = time.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
    type_datetime = datetime(*structed_time[:6], tzinfo = UTC(8))  #datetime.datetime(* t[:6])
    return type_datetime


''''mongo时间转换为年月日 时分秒
'''''
def datetime64ToTimeString(time64):
    # print(time64)
    timeStamp = (time64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    # print('timeStamp =', timeStamp)
    timeArray = time.localtime(timeStamp)
    timeString = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print('timeString =', timeString)
    return timeString

''''mongo时间转换为年月
'''''
def datetime64ToDateYM(time64):
    # print(time64)
    timeStamp = (time64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    # print('timeStamp =', timeStamp)
    timeArray = time.localtime(timeStamp)
    timeString = time.strftime("%Y-%m", timeArray)

    return timeString

def interval_month(date1,date2):

    time_arr = date1.split('-')
    tyears1 = int(time_arr[0])
    tmonth1 = int(time_arr[1])-1

    time_arr = date2.split('-')
    tyears2 = int(time_arr[0])
    tmonth2 = int(time_arr[1])-1
    if tyears1 == tyears2:
        interval_month =tmonth1 -tmonth2
    elif tyears1>tyears2:
        iterval_year =tyears1-tyears2




def timeStrToISODate(timeStr):
    # timeStr = "2016-04-26 01:00:00"
    #将其转换为时间数组
    timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳:
    timeStamp = int(time.mktime(timeArray))
    isodate = datetime.fromtimestamp(timeStamp, tz=pytz.timezone('Asia/Chongqing'))
    # print('时间数组=', isodate)
    return isodate



def minus_moths(_time):
    _time_arr = _time.split('-')
    _tyears = int(_time_arr[0])
    _tmonth = int(_time_arr[1])-1
    if _tmonth==0:
        _tmonth = _tmonth + 12
        _tyears = _tyears - 1
    return str(_tyears)+'-'+str(_tmonth)+'-'+_time_arr[2]
    #Coding by Seay

    print(_minus_moths('2013-01-20'))