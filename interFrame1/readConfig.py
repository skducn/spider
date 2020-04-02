# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : 读取 config.ini , configparser
# ConfigParser 是用来读取config.ini配置文件的包
# *****************************************************************

import os,codecs,configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
# configPath = os.path.join(proDir + "\config\\" , "config.ini")
configPath = os.path.join(proDir + "/config/" , "config.ini")


class ReadConfig:
    def __init__(self):
        fd = open(configPath,"r")
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_system(self, name):
        value = self.cf.get("SYSTEM", name)
        return value

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value


