from selenium import webdriver
from cfg import *
import time

class WebOpLib:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        pass

    def open_browser(self):
        self.wd = webdriver.Chrome()
        self.wd.implicitly_wait(10)

    def close_browser(self):
        self.wd.quit()

    def teacher_login(self,username,password):
        self.wd.get(g_teacher_login_url)
        self.wd.find_element_by_id('username').send_keys(username)
        self.wd.find_element_by_id('password').send_keys(password)
        self.wd.find_element_by_id('submit').click()

        self.wd.find_element_by_id('topbar')


    def get_teacher_homepage_info(self):
        self.wd.find_element_by_css_selector('a[href="#/home"] > li').click()

        self.wd.find_element_by_id('home_div')

        time.sleep(2)

        eles = self.wd.find_elements_by_css_selector('#home_div .ng-binding')
        return [ele.text for ele in eles]





    def get_teacher_class_students_info(self):
        self.wd.find_element_by_css_selector('.main-menu >ul> li:nth-of-type(4)').click()

        self.wd.find_element_by_css_selector('a[href="#/student_group"] span').click()

        time.sleep(2)

        classes = self.wd.find_elements_by_css_selector('div.panel')

        if not classes:
            return {}

        classStudentTab = {}

        for cla in classes:
            gradeclass = cla.find_element_by_class_name('panel-heading').text.replace(' ','')

            cla.click()

            time.sleep(2)

            self.wd.implicitly_wait(1)
            nameEles = cla.find_elements_by_css_selector('tr > td:nth-child(2)')
            self.wd.implicitly_wait(10)

            names = [nameEle.text for nameEle in nameEles]

            classStudentTab[gradeclass]=names

        return classStudentTab



    def student_login(self,username,password):
        self.wd.get(g_student_login_url)
        self.wd.find_element_by_id('username').send_keys(username)
        self.wd.find_element_by_id('password').send_keys(password)
        self.wd.find_element_by_id('submit').click()
        self.wd.find_element_by_id('div-home')

    def get_student_homepage_info(self):
        # 查看 a 元素发现其位置不是主页按钮位置
        self.wd.find_element_by_css_selector("a[href='#/home']>li").click()
        # 确保首页打开
        self.wd.find_element_by_id('div-home')

        # 由于数据是异步获取，需要sleep一段时间，假设需求是2秒必须获取数据
        time.sleep(2)

        eles = self.wd.find_elements_by_css_selector('#div-home .ng-binding')

        ret = [ele.text for ele in eles]
        ret.pop(2)
        return ret



    def get_student_homepage_info(self):
        # 查看 a 元素发现其位置不是主页按钮位置
        self.wd.find_element_by_css_selector("a[href='#/home']>li").click()
        # 确保首页打开
        self.wd.find_element_by_id('div-home')

        # 由于数据是异步获取，需要sleep一段时间，假设需求是2秒必须获取数据
        time.sleep(2)

        eles = self.wd.find_elements_by_css_selector('#div-home .ng-binding')

        ret = [ele.text for ele in eles]
        ret.pop(2)
        return ret

    def get_student_wrongquestions(self):
        self.wd.find_element_by_css_selector("div.main-menu>ul>a:nth-of-type(4)>li").click()

        # 由于数据是异步获取，需要sleep一段时间，假设需求是2秒必须获取数据
        time.sleep(2)

        return self.wd.find_element_by_id('page-wrapper').text

    def teacher_deliver_task(self,examname):
        self.wd.find_element_by_css_selector('.main-menu >ul> li:nth-of-type(2)').click()

        self.wd.find_element_by_css_selector('a[ng-click^="show_page_addexam"] span').click()

        time.sleep(2)

        self.wd.find_element_by_id('exam_name_text').send_keys(examname)

        self.wd.find_element_by_id('btn_pick_question').click()

        # 点击后界面重新渲染，等待一下
        time.sleep(2)

        # 题目在新的frame中
        self.wd.switch_to.frame('pick_questions_frame')

        # 只需要选前3个

        # 每次选择一题，界面会重新渲染，所以只能循环获取

        for counter in range(3):
            selectButtons = self.wd.find_elements_by_class_name('btn_pick_question')
            selectButtons[counter].click()
            # 点击后界面重新渲染，等待一下
            time.sleep(1)

        # 点击 oK button
        self.wd.maximize_window()
        time.sleep(1)
        self.wd.find_element_by_css_selector('div.btn-blue[onclick*="pickQuestionOK"').click()

        # 切换回 主 html
        self.wd.switch_to.default_content()

        # 选完题目回到主界面，界面会发生变动，sleep 一下
        time.sleep(1)

        # 点击确定添加
        self.wd.find_element_by_id('btn_submit').click()

        # 选择发布给学生
        self.wd.find_element_by_css_selector(
            'div.bootstrap-dialog  .bootstrap-dialog-footer-buttons  button:nth-child(2)'
        ).click()

        # sleep 一下
        time.sleep(1)

        # 切换到 下发学习任务窗口

        # 保存主窗口handle
        mainWindow = self.wd.current_window_handle

        for handle in self.wd.window_handles:
            # 切换到新窗口
            self.wd.switch_to.window(handle)
            # 检查是否是我们要进入的window
            if '下发学习任务' in self.wd.title:
                print('进入到下发任务窗口')
                break

        # sleep 一下
        time.sleep(1)

        # 只有唯一的一位学生，直接勾选即可
        # 注意要选  label.myCheckbox  而不是  input[type=checkbox]
        # 因为后者不可见，调试就会发现问题
        self.wd.find_element_by_css_selector('label.myCheckbox').click()

        # 点击确定下发
        self.wd.find_element_by_css_selector('button[ng-click*=openDispatchDlg]').click()

        # sleep 一下
        time.sleep(1)

        # 点击确定
        self.wd.find_element_by_css_selector('button[ng-click*=dispatchIt]').click()

        # 下一个确定
        self.wd.find_element_by_css_selector(
            'div.bootstrap-dialog-footer-buttons > button').click()

        # 切回主窗口
        self.wd.switch_to.window(mainWindow)

    def studentDoExam(self):
        self.wd.find_element_by_css_selector('a[href="#/task_manage"] >li').click()

        # 由于数据是异步获取，需要sleep一段时间，假设需求是2秒必须获取数据
        time.sleep(2)

        # 点击打开第一个任务
        self.wd.find_element_by_css_selector('button[ng-click*=viewTask]').click()

        # 全部选A
        firstAnwsers = self.wd.find_elements_by_css_selector(
            '.btn-group button:nth-child(1)'
        )

        for one in firstAnwsers:
            one.click()

        self.wd.find_element_by_css_selector('button[ng-click*=saveMyResult]').click()

        # 点击确定
        self.wd.find_element_by_css_selector('div.bootstrap-dialog .bootstrap-dialog-footer-buttons button:nth-child(2)').click()

        time.sleep(2)

    def teacher_get_latest_student_task(self):
        self.wd.get('http://ci.ytesting.com/teacher/index.html#/task_manage?tt=1')

        time.sleep(2)

        # 点击第一个任务查看
        self.wd.find_element_by_css_selector("a[ng-click*=trackTask]").click()

        time.sleep(1)

        # 点击 第一个学生 查看
        self.wd.find_element_by_css_selector('button[ng-click*="viewTaskTrack"]').click()

        # 切换到 查看作业窗口

        # 保存主窗口handle
        mainWindow = self.wd.current_window_handle

        for handle in self.wd.window_handles:
            # 切换到新窗口
            self.wd.switch_to.window(handle)
            # 检查是否是我们要进入的window
            if '查看作业' in self.wd.title:
                break

        # 勾选的选项会有 .myCheckbox input:checked  风格修饰，
        # 但是这个不出现在 元素html里面
        eles = self.wd.find_elements_by_css_selector('.myCheckbox input:checked')

        selectedchoices = [ele.find_element_by_xpath('./..').text.strip() for ele in eles]

        print(selectedchoices)

        # 切回主窗口
        self.wd.switch_to.window(mainWindow)

        return selectedchoices

if __name__ == '__main__':
    wo = WebOpLib()
    wo.open_browser()

    wo.teacher_login('zhang', '888888')
    wo.teacher_deliver_task('20190322数学作业')

    wo.student_login('dada', '888888')
    wo.studentDoExam()

    wo.teacher_login('zhang', '888888')
    wo.teacher_get_latest_student_task()




if __name__ == '__main__':
    op = WebOpLib()
    op.open_browser()
    op.student_login()
    ret = op.get_student_homepage_info()
    print(ret)
    ret = op.get_student_wrongquestions()
    print(ret)




    # op.teacher_login()
    # ret = op.get_teacher_homepage_info()
    # print ret

    # ret = op.get_teacher_class_students_info()
    # print ret


