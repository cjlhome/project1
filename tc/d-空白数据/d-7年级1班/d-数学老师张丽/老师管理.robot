*** Settings ***
Library  pylib.TeacherLib
Variables   cfg.py

*** Test Cases ***
添加老师2 - tc001002
#   sleep  1d
  ${addRet}=  add teacher   zhangshan  张三
     ...  ${g_subject_science_id}
     ...  ${suite_g7c1_classid}
     ...  13210252553    13210252553@qq.com    1313210252553
    should be true   $addRet['retcode']==0

  ${listRet}=   list teacher
   teacherlist should contain   ${listRet}[retlist]
      ...  zhangshan   ${suite_g7c1_classid}   张三
      ...  &{addRet}[id]
      ...  13210252553   13210252553@qq.com    1313210252553


    [Teardown]  delete teacher   &{addRet}[id]


添加老师3 - tc001003
  ${listRet1}=  list teacher
  ${addRet}=  add teacher   zhang  张老师
     ...  ${g_subject_science_id}
     ...  ${suite_g7c1_classid}
     ...  13210252554    13210252554@qq.com    1313210252554
    should be true   $addRet['retcode']==1
    should be true   $addRet['reason']=="登录名 zhang 已经存在"

  ${listRet2}=   list teacher
   should be equal   ${listRet1}   ${listRet2}

删除老师1 - tc001081
   ${listRet1}=  list teacher

   ${delRet}=  delete teacher  999999999
   should be true  $delRet['retcode']==404
   should be true  $delRet['reason']=="id 为`999999999`的老师不存在"

   ${listRet2}=   list teacher
   should be equal   ${listRet1}   ${listRet2}

删除老师2 - tc001082
   ${listRet1}=  list teacher
   ${addRet}=  add teacher   zhangshanshan  张三shan
     ...  ${g_subject_science_id}
     ...  ${suite_g7c1_classid}
     ...  13210252554    13210252554@qq.com    1313210252554
    should be true   $addRet['retcode']==0
    delete teacher  ${addRet}[id]

   ${listRet2}=   list teacher
   should be equal   ${listRet1}   ${listRet2}


