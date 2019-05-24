*** Settings ***
Library  pylib.WebOpLib
Library  pylib.TeacherLib
Variables   cfg.py

Suite Setup   open browser
Suite Teardown   close browser

*** Test Cases ***
老师发布作业1 - tc005101
    teacher_login   zhang   888888
#    sleep  1d
    teacher deliver task   20190322数学作业

    student login  dada  888888
    studentDoExam

    teacher_login  zhang   888888

    ${answers}=  teacher_get_latest_student_task
    should be true   $answers==['A','A','A']



