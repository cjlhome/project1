*** Settings ***
Library  pylib.StudentLib
Variables  cfg.py


*** Test Cases ***
添加学生2 - tc002002
#      sleep   1d
    ${AddRet}=  add student   dada3   大大3   ${g_grade_7_id}
               ...   ${suite_g7c1_classid}    1566565546


     should be true     $AddRet['retcode']==0  #python表达式的写法
     ${listRet}   list student
     studentlist_should_contain   &{listRet}[retlist]  #robot的写法
                                  ...  dada3   大大3   &{AddRet}[id]
                                  ...  ${suite_g7c1_classid}     1566565546

    [Teardown]  delete student   &{AddRet}[id]


删除学生1 - tc002081
    ${Retlist1}=  list student
    ${AddRet}=  add student   dadada   大大大   ${g_grade_7_id}
               ...   ${suite_g7c1_classid}    1566565546
     should be true     $AddRet['retcode']==0

     ${delRet}=  delete student  &{AddRet}[id]
     should be true     $delRet['retcode']==0
     ${Retlist2}=  list student
     should be equal   ${Retlist1}   ${Retlist2}