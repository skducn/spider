runAll , 
1������case��ȡ����
xls.py - XLS - getCaseParam([[2, 3, 5], [], 0],'/inter/HTTP/auth')
���أ�[['��ȡToken', 'post', '/inter/HTTP/auth', 'None', '$.status','200']]

2��ÿ���ӿ����ƶ�Ӧ�ĺ������� '/inter/HTTP/auth'
testAuth('��ȡToken', 'post', '/inter/HTTP/auth', 'None', '$.status','200')

	a��HTTP���亯��
	reflection.run(['��ȡToken', 'post', '/inter/HTTP/auth', 'None', '$.status','200'])
	����iDriven.py - HTTP - post(interName, param, jsonpath1, expected)
	��ͬ��post('/inter/HTTP/auth', 'None', '$.status','200')
	���أ� # {"status":401,"msg":"�û����������"}
	
	�ж� status = 401�����assert
	���� tokenֵ
	����excel��Ӧ�� saveparam��result,actual 


  jsonres = reflection.run([caseName, method, interName, param, jsonpathKey, expected])
        d_jsonres = json.loads(jsonres)
        jsonpathValue = jsonpath.jsonpath(d_jsonres, expr=jsonpathKey)
        jsonpathValue = str(jsonpathValue[0])
        # ����Ԥ�ڽ��
        if jsonpathValue != expected :
            xls.setCaseParam(excelNo, '', 'Fail', str(d_jsonres))
            assert jsonpathValue == expected, "Ԥ��ֵ��" + expected + "����ʵ��ֵ��" + jsonpathValue
        else:
            token = jsonpath.jsonpath(d_jsonres, expr='$.token')
            runAll.token = token[0]
            token = "token=" + str(runAll.token)
            xls.setCaseParam(excelNo,token,'pass',str(d_jsonres))


'''

        :return: userid
        '''

        # �Զ�ƥ�� param ����
        if '=' not in param:
            for k, v in xls.d_inter.items():
                if '/inter/HTTP/login' == k :
                    param = http.getJointParam(v, param)
                    break
        jsonres = reflection.run([caseName, method, interName, param, jsonpathKey, expected])
        d_jsonres = json.loads(jsonres)
        jsonpathValue = jsonpath.jsonpath(d_jsonres, expr=jsonpathKey)
        jsonpathValue = str(jsonpathValue[0])
        # ����Ԥ�ڽ��
        if str(jsonpathValue) != str(expected):
            xls.setCaseParam(excelNo, '', 'Fail', str(d_jsonres))
            assert str(jsonpathValue) == str(expected), "Ԥ��ֵ��" + str(expected) + "��ʵ��ֵ��" + str(jsonpathValue)
        else:
            # ��ȡ���ڵ��µ�userid�ڵ��ֵ�����ڹ����¸��ӿ�
            if "userid" in d_jsonres:
                userid = jsonpath.jsonpath(d_jsonres, expr='$.userid')
                runAll.userid = userid[0]
                userid = "userid=" + str(runAll.userid)
                xls.setCaseParam(excelNo, userid, 'pass', str(d_jsonres))
            else:
                xls.setCaseParam(excelNo, '', 'pass', str(d_jsonres))


 """ �ǳ� """

        # result('userid',runAll.userid,'token',runAll.token)

        if '=' not in param:
            for k, v in xls.d_inter.items():
                if '/inter/HTTP/logout' == k:
                    param = http.getJointParam(v, param)
                    break
        # ��������
        if "?" or "&" in param:
            param = param.replace("userid=?", "userid=" + runAll.userid)
            param = param.replace("token=?", "token=" + runAll.token)
            param = param.replace("userid=$userid", "userid=" + runAll.userid)
            param = param.replace("token=$token", "token=" + runAll.token)
        jsonres = reflection.run([caseName, method, interName, param, jsonpathKey, expected])
        d_jsonres = json.loads(jsonres)
        jsonpathValue = jsonpath.jsonpath(d_jsonres, expr=jsonpathKey)
        jsonpathValue = str(jsonpathValue[0])
        # ����Ԥ�ڽ��
        if str(jsonpathValue) != str(expected):
            xls.setCaseParam(excelNo, '', 'Fail', str(d_jsonres))
            assert str(jsonpathValue) == str(expected), "Ԥ��ֵ��" + str(expected) + "��ʵ��ֵ��" + str(jsonpathValue)
        else:
            xls.setCaseParam(excelNo, '', 'pass', str(d_jsonres))