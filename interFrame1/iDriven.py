# -*- coding: utf-8 -*-

import requests,json, jsonpath
import os,xlrd,xlwt
import requests,inspect
import smtplib,email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes ,base64
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
from xlutils.copy import copy
from xlrd import open_workbook


class HTTP:
    # 创建一个http接口请求的关键字类
    # 构造函数，  实例化实例变量

    def __init__(self):

        global scheme, baseurl,port
        scheme = localReadConfig.get_http("scheme")
        baseurl = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")

        # 创建session对象，模拟浏览器的cookie管理
        self.session = requests.session()
        # 存放json解析后的结果
        self.jsonres = {}
        # 用来保存所需要的数据，实现关联
        self.params = {}
        # 全局的url
        self.url = ''
        # 添加默认UA，模拟chrome浏览器
        # self.session.headers['User Agent'] = 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/64.0'
        # 添加默认的请求Content-type
        # self.session.headers['Content-type'] = 'application/x-www-form-urlencoded'

    # 设置地址
    def seturl(self,url):
        if url.startswith('http'):
            self.url = url
            return True
        else:
            print('error:url地址不合法')
            return False

    # 定义post实例方法，用来发送post请求
    def post(self, interName, param, jsonpath, expected):

        '''
        :param interName: /inter/HTTP/login
        :param param: will,1234561212
        :param jsonpath: $.status
        :param expected: 200
        :return:
        '''

        # if not path.startswith('http'):
        #     path = self.url + '/' + path
        path = scheme + "://" + baseurl + ":" + port + interName

        # 获取param参数
        if param == 'None':
            result = self.session.post(path,data=None)
            print(result.text) # {"status":200,"msg":"success","token":"dbc1b5992a984670b12610fce3614246"}
            self.jsonres = json.loads(result.text)
            self.session.headers['token'] = self.jsonres['token']
        elif param == '':
            result = self.session.post(path, data=None)
            print(result.text)
        else:
            # 替换参数
            # param = self.__getparams(param)
            # print(param)  # username=will&password=123456
            # 参数 转 字典
            param = self.__strTodict(param)
            # 发送请求
            result = self.session.post(path,data=param)
            print(param) # {'username': 'will', 'password': '1234561212'}
            print(result.text) # {"status":401,"msg":"用户名密码错误"}

        res = result.text

        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)

        return res

    # 定义断言相等的关键字，用来判断json的key对应的值和期望相等。
    def assertequals(self,jsonpaths,value):
        res = 'None'
        try:
            res = str(jsonpath.jsonpath(self.jsonres, jsonpaths)[0])
        except Exception as e:
            print(e.__traceback__)

        value = self.__getparams(value)

        if res == str(value):
            return True
        else:
            return False

    # 给头添加一个键值对的关键字
    def addheader(self,key,value):
        value = self.__getparams(value)
        self.session.headers[key] = value
        return True
    # 88-93
    #
    #     return True

    # 定义保存一个json值为参数的关键字
    def savejson(self,key,p):
        res = ''
        try:
            res = self.jsonres[key]
        except Exception as e:
            print(e.__traceback__)
        self.params[p] = res
        return True

    # 获取参数里面的值
    def __getparams(self,s):
        for key in self.params:
            s = s.replace('{' + key +'}',self.params[key])
        return s

    def __strTodict(self,s):

        '''
        字符型键值队格式 转 字典类型
        :param s: username=will&password=123456
        :return: {'username':'will','password':'123456’}
        '''

        httpparam = {}
        param = s.split('&')
        for ss in param:
            p = ss.split('=')
            if len(p)>1:
                httpparam[p[0]] = p[1]
            else:
                httpparam[p[0]] = ''
        return httpparam


    def getJointParam(self, keys, values):

        """
            将两个字符串组合成一组接口参数
            如：xls.keyValue('username,password', 'will,123456')
            返回：'username=will&password=123456'
        """

        interKey = len(str(keys).split(','))
        exlValue = len(str(values).split(','))
        varJoint = ''

        try:
            if interKey == exlValue:
                for i in range(interKey):
                    varJoint = varJoint + str(keys).split(',')[i] + '=' + str(values).split(',')[i] + '&'
            else:
                assert (interKey == exlValue)
        except Exception as e:
            # print(e.__traceback__)
            print("error, 接口的参数与值数量不一致！")

        return varJoint[:-1]

    # 3个关于Email函数
    def getAttachment(self, attachmentFilePath):
        contentType, encoding = mimetypes.guess_type(attachmentFilePath)
        if contentType is None or encoding is not None:
            contentType = 'application/octet-stream'
        mainType, subType = contentType.split('/', 1)
        file = open(attachmentFilePath, 'rb')
        if mainType == 'text':
            attachment = MIMEText(file.read())
        elif mainType == 'message':
            attachment = email.message_from_file(file)
        elif mainType == 'image':
            attachment = MIMEImage(file.read(), subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(file.read(), subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
        attachment.set_payload(file.read())
        # encode_base64(attachment)
        base64.b64encode(attachment.encode('utf-8'))

        file.close()
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachmentFilePath))
        return attachment
    def sendemail(self, subject, text, *attachmentFilePaths):
        gmailUser = 'skducn@163.com'
        gmailPassword = 'jinhao123'
        recipient = 'skducn@163.com'
        # recipient = "'jinhao@mo-win.com.cn', 'guoweiliang@mo-win.com.cn'"
        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        # 附件是可选项
        for attachmentFilePath in attachmentFilePaths:
            if attachmentFilePath != '':
                msg.attach(self.getAttachment(attachmentFilePath))
        mailServer = smtplib.SMTP('smtp.exmail.qq.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        print('Sent email to %s' % recipient)
    def send1(self):

        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header

        mail_host = "smtp.163.com"
        mail_user = "skducn@163.com"
        mail_pass = "jinhao80"
        sender = 'skducn@163.com'
        # receivers = ['skducn@163.com', '******@163.com']
        receivers = ['skducn@163.com']
        body_content = """ 测试文本  """

        message = MIMEText(body_content, 'plain', 'utf-8')
        message['From'] = "skducn@163.com"
        message['To'] = "skducn@163.com"
        subject = """
        项目异常测试邮件
        """
        message['Subject'] = Header(subject, 'utf-8')
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.set_debuglevel(1)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")

