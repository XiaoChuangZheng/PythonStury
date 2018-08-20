#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import os
import time, json
import urllib2, urllib
import ConfigParser

# 每n秒执行一次
def timer(n, file_path):
    while True:
        current_time = time.time()
        log_time = get_file_update_time(file_path)
        if current_time - log_time > 60 * 5:
            # sendSmsNotice()
            print("告警任务日志超过5分钟未更新,") + "当前时间：" + time.strftime("%y年%m月%d日 %H:%M:%S") + "日志更新时间：" + time.strftime(
                "%y年%m月%d日 %H:%M:%S", time.localtime(log_time))
        else:
            print "告警任务日志更新了" + time.strftime("%y年%m月%d日 %H:%M:%S", time.localtime(log_time))
        time.sleep(n)


def getUserToken():
    url = "https://antfact.com/auth2_test/authc/login"
    postdata = {'client_id': '3E6570bKX4okbBT10TANVohs', 'client_secret': '349lUwapX54MbjA0wM5q0ZiS',
                "grant_type": "client_credentials"}
    # postdata = json.dumps(postdata)
    postdata = urllib.urlencode(postdata)
    request = urllib2.Request(url, postdata)
    # request.add_header('Content-Type', 'application/json')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header("Accept", "application/json")
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError as ex:
        print "获取token错误"
        print ex
    else:
        result = json.loads(response.read())
        dict_token = dict(result.get("token"))
        token = dict_token.get("access_token")
        print token
        return str(token)


def sendSmsNotice():
    url = "http://172.19.105.84:8056/message/sms"
    postdata = {'toMobile': '15580058416', 'realmName': 'eageye', "text": "告警任务停止了"}
    # postdata = json.dumps(postdata)
    postdata = urllib.urlencode(postdata)
    request = urllib2.Request(url, postdata)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    token = 'oauth2 ' + getUserToken()
    request.add_header("Authorization", token)
    request.add_header("Accept", "application/json")
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError as ex:
        print "发送短信发生错误"
        print ex
    else:
        result = response.read()
        print result


def get_file_update_time(file_path):
    mtime = os.path.getmtime(file_path)
    return mtime

    # timer(10, "/home/zcx/Desktop/alarm.task.schedule.log")
    # sendSmsNotice()
    # getUserToken()



c_time = get_file_update_time("/home/zcx/Desktop/alarm.task.schedule.log")
timer(10, "/home/zcx/Desktop/alarm.task.schedule.log")
