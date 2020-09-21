#!/usr/bin/env python
#-*- coding:utf-8 -*-
############################
#File Name: ipscaner.py
#Author: frank
#Mail: frank0903@aliyun.com
#Created Time:2017-06-05 16:06:37
############################


import platform
import sys
import os
import time
import _thread

def get_os():
    '''
    get os 类型
    '''
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()

    flag = False
    for line in list(output):
        if not line:
            continue
        if str(line).upper().find("TTL") >=0:
            flag = True
            break
    if flag:
        print("ip: %s is ok ***"%ip_str)


def find_ip(ip_prefix):
    for i in range(1, 255):
        ip = '%s.%s' % (ip_prefix, i)
        _thread.start_new_thread(ping_ip, (ip,))
        time.sleep(0.3)


if __name__ == "__main__":
    print("start time %s" % time.ctime())
    # commandargs = "61.142.33.1"
    commandargs = '172.16.1.1'
    args = "".join(commandargs)

    ip_prefix = '.'.join(args.split('.')[:-1])
    find_ip(ip_prefix)
    print("end time %s" % time.ctime())