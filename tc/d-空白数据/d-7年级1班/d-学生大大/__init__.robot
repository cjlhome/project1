*** Settings ***
Library    pylib.StudentLib
Variables  cfg.py
Suite Setup    add student   dada   大大   ${g_grade_7_id}
               ...   ${suite_g7c1_classid}    1566565545
               ...  suite_student_id  #全局变量来存放数学老师id


Suite Teardown   delete student       ${suite_student_id}


