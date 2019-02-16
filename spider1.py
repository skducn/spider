# coding:utf-8
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-7-26
# Description: http://jandan.net/ooxx/ 煎蛋网
# *******************************************************************************************************************************


import urllib
import urllib2,cookielib,lxml
from lxml import etree
from time import sleep

# Referer ,标注我们请求的来源
# User-Agent,请求者身份
# 伪装头信息
header = {"Referer":"http://jandan.net/ooxx/","User-Agent":"Mozilla/5.0 "}

# 遍历
for i in range(9, 10):

    print "\n"
    url = "http://jandan.net/ooxx/page-" + str(i)
    print url + "\n"

    request = urllib2.Request(url, data=None, headers=header)      # 构建请求

    response = urllib2.urlopen(request)      # 发起请求并接收回应

    content = response.read()      # 查看内容

    html = etree.HTML(content)      # 内容筛选 , 将获取内容转化为html结构

    xpath_list = html.xpath("//img")   # 匹配所有的图片对象

    # 对匹配到的内容进行解析
    for obj in xpath_list:
        src = obj.attrib['src']
        # print src
        if 'http' not in src:
            img_url = "http:" + src
            print img_url
            path = "/Users/linghuchong/Downloads/51/spider1/" + img_url.rsplit("/",1)[1]
        else:
            path = "/Users/linghuchong/Downloads/51/spider1/" + src.rsplit("/", 1)[1]
        urllib.urlretrieve(img_url, path)
        sleep(1)




