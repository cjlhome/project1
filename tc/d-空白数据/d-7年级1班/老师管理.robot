*** Settings ***
Library  pylib.TeacherLib
Variables   cfg.py

*** Test Cases ***
添加老师1 - tc001001
#    sleep  1d
  ${addRet}=  add teacher   zhang  张丽
     ...  ${g_subject_math_id}
     ...  ${suite_g7c1_classid}
     ...  13210252552    13210252552@qq.com    1313210252552
    should be true  $addRet['retcode']==0

  ${listRet}=   list teacher
   teacherlist should contain   ${listRet}[retlist]
      ...  zhang   ${suite_g7c1_classid}   张丽
      ...  &{addRet}[id]
      ...  13210252552   13210252552@qq.com    1313210252552


    [Teardown]  delete teacher   &{addRet}[id]



