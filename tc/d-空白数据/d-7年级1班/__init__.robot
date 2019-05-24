*** Settings ***
Library    pylib.SchoolClassLib
Variables  cfg.py
Suite Setup    add_school_class    ${g_grade_7_id}    1班    60   suite_g7c1_classid
Suite Teardown   delete_school_class       ${suite_g7c1_classid}  #七年级1班的id


