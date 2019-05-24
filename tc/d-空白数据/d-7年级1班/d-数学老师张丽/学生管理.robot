*** Settings ***
Library  pylib.StudentLib
Variables  cfg.py


*** Test Cases ***
添加学生1 - tc002001
    ${AddRet}=  add student   dadada   大大大   ${g_grade_7_id}
               ...   ${suite_g7c1_classid}    1566565546


     should be true     $AddRet['retcode']==0  #python表达式的写法
     ${listRet}   list student
     studentlist_should_contain   &{listRet}[retlist]  #robot的写法
                                  ...  dadada   大大大   &{AddRet}[id]
                                  ...  ${suite_g7c1_classid}     1566565546

    [Teardown]  delete student   &{AddRet}[id]



