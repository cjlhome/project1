import requests
from cfg import g_vcode
from pprint import pprint
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import json

class  StudentLib:
    URL = "http://ci.ytesting.com/api/3school/students"

    def __init__(self):
        self.vcode = g_vcode

    def set_vcode(self,vcode):
        self.vcode = vcode

    def delete_student(self, studentid):
        payload = {
            'vcode': self.vcode,
        }

        url = '{}/{}'.format(self.URL, studentid)
        response = requests.delete(url, data=payload)

        bodyDict = response.json()
        pprint(bodyDict, indent=2)
        return bodyDict

    def list_student(self):
        params = {
                'vcode': self.vcode,
                'action': 'search_with_pagenation'
            }
        response = requests.get(self.URL, params=params)

        bodyDict = response.json()
        pprint(bodyDict, indent=2)
        return bodyDict

    def add_student(self, username, realname, gradeid,classid,phonenumber,idsavedname=None):
        payload = {
            'vcode': self.vcode,
            'action': 'add',
            'username': username,
            'realname':realname,
            'gradeid': int(gradeid),
            'classid':int(classid),
            'phonenumber':phonenumber,
        }
        response = requests.post(self.URL, data=payload)

        bodyDict = response.json()
        # logger.debug('ret:\n{}'.format(bodyDict))
        pprint(bodyDict, indent=2)
        if idsavedname:
            BuiltIn().set_global_variable('${%s}' % idsavedname, bodyDict['id'])
        return bodyDict

    def delete_all_students(self):
        # 先列出所有学生
        rd = self.list_student()
        if rd['retcode'] != 0:
            raise Exception('cannot list all students!')
        pprint(rd, indent=2)

        # 删除列出的所有学生
        for one in rd['retlist']:
            self.delete_student(one['id'])

        # 再列出所有的学生
        rd = self.list_student()
        pprint(rd, indent=2)

        # 如果没有删除干净，通过异常报错给RF
        # 参考http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#reporting-keyword-status
        if rd['retlist'] != []:
            raise Exception("cannot delete all students!!")

    def studentlist_should_contain(self,
                                   studentlist,
                                   username,
                                   realname,
                                   studentid,
                                   classid,
                                   phonenumber,
                                  expectedtimes=1):


        item = {
            "classid": int(classid),
            "username": username,
            "realname": realname,
            "phonenumber": phonenumber,
            "id": int(studentid),
        }

        occurtimes = studentlist.count(item)
        logger.info('occur {} times'.format(occurtimes))
        if occurtimes != int(expectedtimes):
            raise Exception(f'学生列表包含了{occurtimes}次指定信息，期望包含{expectedtimes}！！')

    def modify_student(self, studentid, realname=None, phonenumber=None):

        payload = {
            'vcode': self.vcode,
            'action': 'modify'
        }
        if realname != None:#最好不要写成if realname:不严谨，有0的情况
            payload['realname'] = realname
        if phonenumber != None:
            payload['phonenumber'] = phonenumber

        url = '{}/{}'.format(self.URL, studentid)  # 也可以用url =f'{self.URL}/{classid}'
        response = requests.put(url, data=payload)
        bodyDict = response.json()
        pprint(bodyDict, indent=2)
        return bodyDict



# if _name_=='_main_':
#     scm = StudentLib()
#     ret =scm.list_student()



