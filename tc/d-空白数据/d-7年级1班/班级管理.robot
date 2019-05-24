*** Settings ***
Library    pylib.SchoolClassLib
Variables  cfg.py

*** Test Cases ***
添加班级2 - tc000002
     ${ret1}=    add_school_class    ${g_grade_7_id}     2班     60
     should be true     $ret1['retcode']==0
     ${ret2}=    list school class    ${g_grade_7_id}
     ${retlist}=   evaluate   $ret2['retlist']
     #下面这种方法比较麻烦，容易出错。可以自己封装一个函数来写。
#     should be true    {"name":"2班","grade__name":"七年级","invitecode":$ret1["invitecode"],"studentlimit":60,"studentnumber":0,"id":$ret1["id"],"teacherlist":[]} in $retlist
     classlist should contain    ${retlist}
     ...  2班  七年级   &{ret1}[invitecode]  60  0  &{ret1}[id]
     [Teardown]    delete_school_class   &{ret1}[id]

添加班级3 - tc000003
    ${ret1}=    list school class    ${g_grade_7_id}
    ${addret1}=    add_school_class    1     1班     60
    should be true     $addret1['retcode']==1
    should be true      $addret1['reason']=="duplicated class name"

#列出班级，检验一下
    ${ret2}=    list school class    ${g_grade_7_id}
    should be true  $ret1 == $ret2


#    [Teardown]    delete_school_class   &{ret1}[id]   没有添加数据，不用teardown

修改班级1 - tc000051
    ${ret1}=    add_school_class    ${g_grade_7_id}     2班     60
    should be true     $ret1['retcode']==0
    ${classid}=   evaluate   $ret1['id']
    ${modifyret}=  modify_sclool_class  ${classid}  22班  60
    should be true   $modifyret['retcode'] == 0
     ${ret2}=  list school class  ${g_grade_7_id}
     ${retlist}=  evaluate   $ret2['retlist']
     classlist should contain       ${retlist}
     ...  22班  七年级   &{ret1}[invitecode]  60  0  ${classid}  #也可以写成存下来的${classid}
     [Teardown]  delete_school_class   ${classid}


修改班级2 - tc000052
    ${ret1}=    add_school_class    ${g_grade_7_id}      2班     60
    should be true     $ret1['retcode']==0
     ${classid}=   evaluate   $ret1['id']
     ${retlist1}=  list school class  ${g_grade_7_id}
     ${modifyret}=  modify_sclool_class  $classid  1班  60
     should be true         $modifyret['retcode'] ==1
     should be true      $modifyret['reason']=="duplicated class name"
     ${retlist2}=  list school class  ${g_grade_7_id}
     should be equal   ${retlist1}     ${retlist2}

#列出班级，检验一下
    ${ret2}=    list school class   ${g_grade_7_id}
    should be equal  $ret1   $ret2
    [Teardown]   delete_school_class   $classid

修改班级3 - tc000053
    ${modifyret}=  modify_sclool_class   99999  1班  60
    should be true      $modifyret['retcode'] ==404
    should be true      $modifyret['reason']=="id 为`99999`的班级不存在"


删除班级1 - tc000081
    ${retlist1}=  list school class  ${g_grade_7_id}
    ${delret}=  delete_school_class    99999
    should be true      $delret['retcode'] ==404
    should be true      $delret['reason']=="id 为`99999`的班级不存在"
    ${retlist2}=  list school class  ${g_grade_7_id}
    should be equal   ${retlist1}     ${retlist2}

删除班级2 - tc000082
    ${ret1}=    add_school_class    ${g_grade_7_id}      2班     60
    should be true     $ret1['retcode']==0
    ${classid}=   evaluate   $ret1['id']

    ${retlist1}=  list school class  1
    classlist should contain       &{retlist1}[retlist]
     ...  2班  七年级   &{ret1}[invitecode]  60  0  ${classid}


     ${delret}=  delete_school_class   ${classid}
     should be true     $delret['retcode']==0


     ${retlist2}=  list school class  ${g_grade_7_id}
     classlist should contain      &{retlist2}[retlist]
     ...  2班  七年级   &{ret1}[invitecode]  60
     ...  0  ${classid}  0  #期望包含0次




