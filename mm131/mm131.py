# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-24
# Description   : 爬取www.mm131.com上图片
# 参考 https://zhuanlan.zhihu.com/p/25428493 python 爬虫爬取妹子图
# *****************************************************************
# 功能：爬取 www.mm131.com 网站上板块中的图片
# 格式：mm131(参数1，参数2[，参数3])
# 参数1：板块名称
# 参数2：页数
# 参数3：相册数
# 场景1、爬取国产美女板块下所有相册，如：mm131('性感车模','all')
# 场景2、爬取国产美女板块下第2页的所有相册，如：mm131('性感车模','2','all')
# 场景3、爬取国产美女板块下第2页的第4相册，如：mm131('性感车模','2','4')
# 场景4、爬取国产美女板块下第2页的第4和第7相册（2个），如：mm131('性感车模','2','4,7')
# 场景5、爬取国产美女板块下第2页的第4到第6相册（3个），如：mm131('性感车模','2','4-6')

import os,requests,sys
from bs4 import BeautifulSoup
from time import sleep

baseURL = "http://www.mm131.com"

# 获取板块的URL
def getModuleURL(moduleName):

    '''
    获取板块的URL
    :param moduleName: 明星写真（可选：性感美女，清纯美眉，美女校花，性感车模，旗袍美女，明星写真）
    :return:  http://www.mm131.com/mingxing/
    '''

    html = requests.get(baseURL)
    html.encoding = 'gb2312'
    bsop = BeautifulSoup(html.text, 'html.parser')
    l_modulePages = bsop.find('div', {'class': 'nav'}).find('ul').findAll('li')
    for l in l_modulePages[1:]:
        if moduleName in str(l):
            moduleURL = str(l).split('href="')[1].split('"')[0]
            break
        else:
            moduleURL = None
    return moduleURL

# 遍历相册页数、每页相册数
def xiangce(moduleName, moduleURL, *param):

    '''
    相册页数、每页相册数
    :param moduleName: 性感车模
    :param moduleURL: http://www.mm131.com/chemo/
    :param param: all 、 2，all 、 2，4 、 2，'4，7' 、 2，‘4-6’
    :return:
    '''

    html = requests.get(moduleURL)
    html.encoding = 'gb2312'
    bsop = BeautifulSoup(html.text, 'html.parser')

    # 相册页数
    l_xiangcePages = bsop.find('dd', {'class': 'page'}).findAll('a')
    pages = str(l_xiangcePages[-1]).split('href="')[1].split('"')[0].split(".html")[0] # list_5_8
    tmp1 = pages.split("_")[0]
    tmp2 = pages.split("_")[1]
    pages = pages.split("_")[2]
    print(moduleName + "(" + moduleURL + ") 共" + str(pages) + "页")


    if len(param) == 1 :
        # 没有参数3时，mm131('性感车模','all')
        pageStart = 1  # 第一页
        pageEnd = int(pages)
    else:
        # 有参数3(param[1])，如 mm131('性感车模','2','4') or mm131('性感车模','2','all')
        try:
            page = int(param[0])
            try:
                if page < 0 :
                    print("error，参数2不能小于0")
            except Exception as e:
                print(e)
            xiangceNo = param[1]
            pageStart = int(page)
            pageEnd = int(page)
        except Exception as e:
            print(e)
            print("error,如果有参数2和参数3时，参数2表示具体的页数，此数字必须大于0")

        if xiangceNo != 'all':
            if ',' in xiangceNo:
                # mm131('性感车模', '2', '4,7')
                xiangceNo1 = str(xiangceNo).split(',')
                list1 = []
                for i in range(len(xiangceNo1)):
                    list1.append(xiangceNo1[i])
                # print(list1) # ['4', '7']
            elif '-' in xiangceNo:
                # mm131('性感车模', '2', '4-6')
                xiangceNo2 = str(xiangceNo).split("-")
                list2 = []
                for i in range(int(xiangceNo2[0]),int(xiangceNo2[1])+1):
                    list2.append(i)
                # print(list2)  # ['4', '7']


    # 遍历相册页数
    for i in range(pageStart, pageEnd + 1):
        if i == 1:
            print("第" + str(i) + "页(" + moduleURL + ")")
            xiangceURL = moduleURL  # http://www.mm131.com/xinggan/
        else:
            print("第" + str(i) + "页(" + moduleURL + tmp1 + "_" + tmp2 + "_" + str(i) + ".html)")
            xiangceURL = moduleURL + tmp1 + "_" + tmp2 + "_" + str(i) + ".html"  # http://www.mm131.com/xinggan/list_6_2.html

        html = requests.get(xiangceURL)
        html.encoding = 'gb2312'
        bsop = BeautifulSoup(html.text, 'html.parser')
        # 遍历当前页的相册URL
        l_xiangce = bsop.find('dl', {'class': 'list-left public-box'}).findAll('dd')
        x = 0
        for l in l_xiangce[:-1]:
            # print(l)
            x = x + 1
            if (len(param) == 1 and param[0] == 'all') or xiangceNo == 'all':
                # mm131('性感车模', 'all') or mm131('性感车模','2','all')
                xiangceURL= str(l).split('href="')[1].split('"')[0]
                print("相册" + str(x) + "：" + xiangceURL)
                downloadPIC(xiangceURL)
            elif ',' in xiangceNo:
                # mm131('性感车模', '2', '4,7')
                if str(x) in list1:
                    xiangceURL = str(l).split('href="')[1].split('"')[0]
                    print("相册" + str(x) + "：(" + xiangceURL + ")")  # http://www.mm131.com/xinggan/4725.html
                    downloadPIC(xiangceURL)
            elif '-' in xiangceNo:
                # mm131('性感车模', '2', '4-6')
                if x in list2:
                    xiangceURL = str(l).split('href="')[1].split('"')[0]
                    print("相册" + str(x) + "：(" + xiangceURL + ")")  # http://www.mm131.com/xinggan/4725.html
                    downloadPIC(xiangceURL)
            else:
                # mm131('性感车模','2','4')
                if int(xiangceNo) == x :
                    xiangceURL = str(l).split('href="')[1].split('"')[0]
                    print("相册" + str(x) + "：(" + xiangceURL + ")")  # http://www.mm131.com/xinggan/4725.html
                    downloadPIC(xiangceURL)
                    break
        print("\n")

# 下载图片
def downloadPIC(xiangceURL):

    '''
    下载图片
    :param xiangceURL: http://www.mm131.com/mingxing/1742.html
    :return:
    '''

    # 获取第一张图片
    html = requests.get(xiangceURL)
    html.encoding = 'gb2312'
    bsop = BeautifulSoup(html.text, 'html.parser')
    imgTotalPages = bsop.find('div', {'class': 'content-page'}).find('span')
    imgTotalPages = str(imgTotalPages).split('共')[1]
    imgTotalPages = imgTotalPages.split('页')[0]
    # print(str(imgTotalPages) + '张图：') # 获取图片总页数

    # 获取图片标题，可用于目录名
    imgFolder = bsop.find('div', {'class': 'content'}).find('h5')
    imgFolder = str(imgFolder).replace("<h5>", "")
    imgFolder = str(imgFolder).replace("</h5>", "")
    proDir = os.path.split(os.path.realpath(__file__))[0]
    resultPath = os.path.join(proDir, imgFolder)
    if not os.path.exists(resultPath):
         os.mkdir(resultPath)

    # 获取图片地址
    imgJPG = bsop.find('div', {'class': 'content-pic'}).find('a').findAll('img')[0].attrs['src']
    print("download 1 : " + imgJPG)
    imgName = imgJPG.split('/')[-1]  # 单个图片的名字，通过分割url得到
    headers = {"Referer": xiangceURL,
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36", }
    img_html = requests.get(imgJPG, headers=headers)
    with open(resultPath + '\\' + imgName, 'wb') as f:
        f.write(img_html.content)
        f.close()

    # 获取第二张到最后的图片
    for i in range(2,int(imgTotalPages)+1):
        url = str(xiangceURL).split(".html")[0] + "_" + str(i) + ".html"
        html = requests.get(url)
        bsop = BeautifulSoup(html.text, 'html.parser')
        # 获取图片地址
        imgJPG = bsop.find('div', {'class': 'content-pic'}).find('a').findAll('img')[0].attrs['src']
        print("download " + str(i) + " : " + imgJPG)
        imgName = imgJPG.split('/')[-1]  # 单个图片的名字，通过分割url得到
        img_html = requests.get(imgJPG, headers=headers)
        with open(resultPath + '\\' + imgName, 'wb') as f:
            f.write(img_html.content)
            f.close()

# 主程序
def mm131(moduleName, *param):

    '''
    :param moduleName: 版块名
    :param param: 动态参数
    # 参数1：板块名
    # 参数2：页码
    # 参数3：相册
    # mm131('性感车模','all') # 下载 性感车模 板块中所有的相册图片(谨慎)
    # mm131('性感美女','7','2') # 下载 性感美女 板块第7页相册2
    # mm131('性感美女','7','1,7,4') # 下载 性感美女 板块第7页相册1、4、7
    # mm131('性感美女','7','4-6') # 下载 性感美女 板块第7页相册4、5、6
    mm131('性感美女','7','all') # 下载 性感美女 板块第7页所有相册
    :return:
    '''

    moduleURL = getModuleURL(moduleName)
    xiangce(moduleName, moduleURL, *param)
    os.startfile(str('E:\\51\\Python\\09project\\common\\spider\\mm131'))


# mm131('性感美女','1','10')
# mm131('性感美女','7','1,7,4')
# mm131('性感美女','1','1-2')
# mm131('性感美女','1','all')


# 下载指定相册中的所有图片
downloadPIC("http://www.mm131.com/xinggan/4748.html")

# cmd 命令行方式使用参数 ,如: python3 mm131.py 1 2
# mm131('性感美女',sys.argv[1],sys.argv[2])





