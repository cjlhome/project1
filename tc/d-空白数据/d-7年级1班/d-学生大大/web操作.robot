*** Settings ***
Library  pylib.WebOpLib
Library  pylib.TeacherLib
Variables   cfg.py

Suite Setup   open browser
Suite Teardown   close browser

*** Test Cases ***
老师登录2 - tc005002
    ${addRet}=  add teacher   zhangshan22  张山
     ...  ${g_subject_math_id}
     ...  ${suite_g7c1_classid}
     ...  13210252558    1321025258@qq.com    1313210252558
    should be true   $addRet['retcode']==0


#    sleep   1d

    teacher_login   zhangshan22   888888
    ${homepageinfo}=  get_teacher_homepage_info
    should be true  $homepageinfo==['松勤学院0357','张山','初中数学','0','0','0']

    ${csinfo}=  get_teacher_class_students_info
    should be true  $csinfo=={'七年级1班':['大大']}

    [Teardown]  delete teacher   &{addRet}[id]