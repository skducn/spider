# coding:utf-8
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-7-26
# Description: 党建接口1.5
# https://www.macappstore.net/wallpaper/index_2.html  高清壁纸
# *******************************************************************************************************************************


import urllib
import urllib2,cookielib,lxml
from lxml import etree
from time import sleep

# 伪装头信息
header = {
    "Referer":"https://www.macappstore.net/wallpaper/index_2.html",
    "User-Agent":"Mozilla/5.0 "
}

# 遍历多少页
for i in range(2, 3):

    print "\n"
    # url = "http://jandan.net/ooxx/page-" + str(i)
    # url = "https://www.macappstore.net/wallpaper/index_" + str(i) + ".html"
    url = "https://www.macappstore.net/wallpaper/index_8.html"
    # url ="https://www.macappstore.net/wallpaper/12/777/"
    print url + "\n"

    # 构建请求
    request = urllib2.Request(url, data=None, headers=header)
    #发起请求并接收回应
    response = urllib2.urlopen(request)
    #查看内容
    content = response.read()
    # 内容筛选 , 将获取内容转化为html结构
    html = etree.HTML(content)
    # 按照结构匹配
    xpath_list = html.xpath("//a")   # 匹配所有的图片对象
    print len(xpath_list)
    # 对匹配到的内容进行解析
    # tag标签，text文本内容，attrib属性
    for obj in xpath_list:
        src = obj.attrib['href']
        print src
        # img_url = src.rsplit("?")[0]
        # print img_url
        # # print img_url
        # name = img_url.rsplit("/",1)[1]
        # print name
        # path = "/Users/linghuchong/Downloads/51/testpic/" + name
        # if "http" not in img_url:
        #     print "ignore:" + img_url
        # else:
        #     urllib.urlretrieve(img_url, path)
        sleep(1)





