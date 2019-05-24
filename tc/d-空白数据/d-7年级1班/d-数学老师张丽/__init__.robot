*** Settings ***
Library    pylib.TeacherLib
Variables  cfg.py
Suite Setup    add teacher   zhang  张丽
     ...  ${g_subject_math_id}
     ...  ${suite_g7c1_classid}
     ...  13210252552    13210252552@qq.com    1313210252552
     ...  suite_math_teacherid  #全局变量来存放数学老师id


Suite Teardown   delete teacher       ${suite_math_teacherid}


