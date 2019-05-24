import requests
from cfg import g_vcode
from pprint import pprint
# from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import json

class  TeacherLib:
    URL = "http://ci.ytesting.com/api/3school/teachers"

    def __init__(self):
        self.vcode = g_vcode

    def set_vcode(self,vcode):
        self.vcode = vcode

    def delete_teacher(self, teacherid):
        payload = {
            'vcode': self.vcode,
        }

        url = '{}/{}'.format(self.URL, teacherid)
        response = requests.delete(url, data=payload)

        bodyDict = response.json()
        pprint(bodyDict, indent=2)
        return bodyDict

    def list_teacher(self, subjectid=None):
        if subjectid != None:
            params = {
                'vcode': self.vcode,
                'action': 'search_with_pagenation',
                'subjectid': int(subjectid)
            }
        else:
            params = {
                'vcode': self.vcode,
                'action': 'search_with_pagenation'
            }

        response = requests.get(self.URL, params=params)

        bodyDict = response.json()
        pprint(bodyDict, indent=2)
        return bodyDict

    def add_teacher(self, username, realname, subjectid,classlist,phonenumber,email, idcardnumber,                     idsavedname=None):
        classlist=str(classlist)
        newclasslist=[{'id':oneid} for oneid in classlist.split(',') if oneid]
        payload = {
            'vcode': self.vcode,
            'action': 'add',
            'username': username,
            'realname':realname,
            'subjectid': int(subjectid),
            'classlist':json.dumps(newclasslist),
            'phonenumber':phonenumber,
            'email':email,
            'idcardnumber':idcardnumber
        }
        response = requests.post(self.URL, data=payload)

        bodyDict = response.json()
        # logger.debug('ret:\n{}'.format(bodyDict))
        pprint(bodyDict, indent=2)
        if idsavedname:
            BuiltIn().set_global_variable('${%s}' % idsavedname, bodyDict['id'])
        return bodyDict

    def delete_all_teachers(self):
        # 先列出所有老师
        rd = self.list_teacher()
        if rd['retcode'] != 0:
            raise Exception('cannot list all teachers!')
        pprint(rd, indent=2)

        # 删除列出的所有老师
        for one in rd['retlist']:
            self.delete_teacher(one['id'])

        # 再列出所有的老师
        rd = self.list_teacher(1)
        pprint(rd, indent=2)

        # 如果没有删除干净，通过异常报错给RF
        # 参考http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#reporting-keyword-status
        if rd['retlist'] != []:
            raise Exception("cannot delete all teacher!!")

    def teacherlist_should_contain(self,
                                   teacherlist,
                                   username,
                                   teachclasslist,
                                   realname,
                                   teacherid,
                                   phonenumber,
                                   email,
                                   idcardnumber,
                                   expectedtimes=1):

        teachclasslist=str(teachclasslist)

        item = {
            "username": username,
            "teachclasslist": [int(one) for one in teachclasslist.split(',')],
            "realname": realname,
            "phonenumber": phonenumber,
            "id": int(teacherid),
            "email": email,
          "idcardnumber": idcardnumber
        }
        occurtimes = teacherlist.count(item)
        if occurtimes != int(expectedtimes):
            raise Exception(f'老师列表包含了{occurtimes}次指定信息，期望包含{expectedtimes}！！')

    def modify_teacher(self, teacherid, realname=None, subjectid=None,classlist=None,                                       phonenumber=None,email=None,idcardnumber=None):

        payload = {
            'vcode': self.vcode,
            'action': 'modify'
        }
        if realname != None:
            payload['realname'] = realname
        if subjectid != None:
            payload['subjectid'] = int(subjectid)
        if classlist != None:
            classlist = str(classlist)
            newclasslist = [{'id': oneid} for oneid in classlist.split(',') if oneid]
            payload['classlist'] = json.dumps(newclasslist)
        if phonenumber != None:
            payload['phonenumber'] = phonenumber
        if email != None:
            payload['email'] = email
        if idcardnumber != None:
            payload['idcardnumber'] = idcardnumber

        url = '{}/{}'.format(self.URL, teacherid)  # 也可以用url =f'{self.URL}/{classid}'
        response = requests.put(url, data=payload)
        bodyDict = response.json()
        pprint(bodyDict, indent=2)
        return bodyDict
