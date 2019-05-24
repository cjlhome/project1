*** Settings ***
Library    pylib.SchoolClassLib
Library   pylib.TeacherLib
Library   pylib.StudentLib
Suite Setup     Run Keywords     delete all students  AND
                               ...  delete all teachers   AND
                               ...  delete all school classes        #要先删掉老师，在删掉班级，老师依赖班级，  班级是基础