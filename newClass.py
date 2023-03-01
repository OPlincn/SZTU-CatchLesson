from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CatchProcession:
    def __init__(self, log_id, passwd, lessonType, teachers_names, lesson_select_set):
        self.log_id = log_id
        self.passwd = passwd
        self.lessonType = lessonType
        self.teachers_names = teachers_names
        self.lesson_select_set = lesson_select_set
        self.driver = webdriver.Chrome(r'\chromeself.driver\chromeself.driver.exe')
        url = 'https://auth.sztu.edu.cn/idp/authcenter/ActionAuthChain?entityId=jiaowu'
        self.driver.set_window_size(1200, 800)  # 设置浏览器大小
        self.driver.get(url)

    def login_to_system(self):
        self.driver.find_element("xpath", r'//*[@id="j_username"]').send_keys(self.log_id)
        self.driver.find_element("xpath", r'//*[@id="j_password"]').send_keys(self.passwd)
        self.driver.find_element("xpath", r'//*[@id="loginButton"]').click()  # 登录
        time.sleep(1)
        self.driver.find_element("xpath", r'/html/body/div[5]/div[1]/section/ul/li[5]/div').click()  # 点击培养管理
        time.sleep(1)
        self.driver.find_element("xpath", r"/html/body/div[5]/div[1]/section/ul/li[5]/ul/li[3]/div").click()  # 点击选课管理
        time.sleep(1)
        self.driver.find_element("xpath",
                                 r'/html/body/div[5]/div[1]/section/ul/li[5]/ul/li[3]/ul/li[1]').click()  # 点击学生选课中心
        # 切换至框架Frame1,才能点击内嵌的A标签
        self.driver.switch_to.frame("Frame1")
        self.driver.find_element('xpath', r'//*[@id="attend_class"]/tbody/tr[2]/td[4]/a').click()  # 进入选课 得到token
        self.driver.switch_to.default_content()  # 回去原来的框架
        self.driver.switch_to.frame("Frame1")  # 再变到标签所在框架，这个流程似乎使必须的
        time.sleep(1)
        self.driver.find_element('xpath', r'/html/body/form/div/div/input[2]').click()  # 进入选课

    def into_lesson_system(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(1)
        # 接下来的两个if， 分别进入到计划选课和公选课页面中
        if self.lessonType == 'public': self.driver.find_element('xpath',
                                                                 r'/html/body/div[1]/div[1]/ul/li[3]/a').click()
        if self.lessonType == 'plan': self.driver.find_element('xpath', r'/html/body/div[1]/div[1]/ul/li[2]/a').click()
        time.sleep(1)

    def catch_lesson(self):
        self.driver.switch_to.default_content()  # 回去原来的框架
        self.driver.switch_to.frame('mainFrame')
        time.sleep(1)
        no_lesson = True
        while no_lesson:
            # 以下两个if 用来适配 "计划选课" 和 "公选课" 在课程剩余人数和选课确认 xpath链接上的不同， 目前还未对同时检索三门课的情况进行调试
            if self.lessonType == 'plan':
                num_td_index = '12'
                confirm_td_index = '14'
            if self.lessonType == 'public':
                num_td_index = '10'
                confirm_td_index = '13'
            for teacher in self.teachers_names:
                lesson_select_index = self.teachers_names.index(teacher)  # 确定此时循环中的老师的选课 777
                what_time_is = time.ctime()
                print('\n----------------------------------------')
                print(f"时间: {what_time_is}\n开始检索{teacher}老师的课还缺不缺人!\n")
                input_teacher = self.driver.find_element('xpath', '//*[@id="skls"]')  # 键入名字
                input_teacher.clear()
                input_teacher.send_keys(teacher)
                time.sleep(1)
                try:
                    self.driver.find_element('xpath', '/html/body/div[8]/input[4]').click()
                    time.sleep(2)
                except:
                    continue
                # 第一节
                if self.lesson_select_set[lesson_select_index] in [1, 3, 5, 7]:
                    if self.lesson_select_set[lesson_select_index] == 1: tr_tail = ''
                    else: tr_tail = '[1]'
                    try:
                        lesson_left = self.driver.find_element('xpath',
                                                               f'/html/body/div[9]/div/table/tbody/tr{tr_tail}/td[{num_td_index}]')
                        print(f'{teacher}老师的第一场课现在有{lesson_left.text}个名额！')
                    except Exception as a:
                        print(f"获得{teacher}老师第一场课的剩余人数步骤Error {a}, 先跳过这次！")
                        continue
                    if int(lesson_left.text) > 0:
                        try_times = 1
                        while True:  # 抢都抢到了 报错也得循环下去
                            try:
                                self.driver.find_element('xpath',
                                                         f'/html/body/div[9]/div/table/tbody/tr{tr_tail}/td[{confirm_td_index}]/div/a').click()
                                if self.lessonType == 'public':
                                    # 等待弹窗出现
                                    alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                                    # 获取弹窗对象
                                    alert_obj = self.driver.switch_to.alert
                                    # 点击弹窗上的确认按钮
                                    alert_obj.accept()
                                break
                            except Exception as b:
                                try_times += 1
                                print(f"抢到课时An error occurred: {b}, But I will retry!")
                                time.sleep(1)  # 等待1秒钟，然后再尝试执行
                                if try_times == 9:
                                    print("啊哦，抢课失败，下面的\"抢到了老师的课\"是假消息!")
                                    break
                        print(f"恭喜恭喜！抢到了{teacher}老师的第一场课!")
                        if try_times != 9: no_lesson = False
                        break
                # 第二节
                if self.lesson_select_set[lesson_select_index] in [2, 3, 6, 7]:
                    try:
                        lesson_left = self.driver.find_element('xpath',
                                                               f'/html/body/div[9]/div/table/tbody/tr[2]/td[{num_td_index}]')
                        print(f'{teacher}老师的第二场课现在有{lesson_left.text}个名额！')
                    except Exception as c:
                        print(f"获得{teacher}老师第二场课的剩余人数步骤Error {c}, 先跳过这次！")
                        continue
                    if int(lesson_left.text) > 0:
                        try_times = 1
                        while True:
                            try:
                                self.driver.find_element('xpath',
                                                         f'/html/body/div[9]/div/table/tbody/tr[2]/td[{confirm_td_index}]/div/a').click()
                                if self.lessonType == 'public':
                                    # 等待弹窗出现
                                    alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                                    # 获取弹窗对象
                                    alert_obj = self.driver.switch_to.alert
                                    # 点击弹窗上的确认按钮
                                    alert_obj.accept()
                                break
                            except Exception as e:
                                try_times += 1
                                print(f"抢到课时An error occurred: {e}, But I will retry!")
                                time.sleep(1)  # 等待1秒钟，然后再尝试执行
                                if try_times == 9:
                                    print("啊哦，抢课失败，下面的\"抢到了老师的课\"是假消息!")
                                    break
                        print(f"抢到了{teacher}老师的第二场课!")
                        if try_times != 9: no_lesson = False
                        break
                # 第三节
                if self.lesson_select_set[lesson_select_index] in [4, 5, 6, 7]:
                    try:
                        lesson_left = self.driver.find_element('xpath',
                                                               f'/html/body/div[9]/div/table/tbody/tr[3]/td[{num_td_index}]')
                        print(f'{teacher}老师的第三场课现在有{lesson_left.text}个名额！')
                    except Exception as d:
                        print(f"获得{teacher}老师第三场课的剩余人数步骤Error {d}, 先跳过这次！")
                        continue
                    if int(lesson_left.text) > 0:
                        try_times = 1
                        while True:
                            try:
                                self.driver.find_element('xpath',
                                                         f'/html/body/div[9]/div/table/tbody/tr[3]/td[{confirm_td_index}]/div/a').click()
                                if self.lessonType == 'public':
                                    # 等待弹窗出现
                                    alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                                    # 获取弹窗对象
                                    alert_obj = self.driver.switch_to.alert
                                    # 点击弹窗上的确认按钮
                                    alert_obj.accept()
                                break
                            except Exception as e:
                                try_times += 1
                                print(f"要抢到课时An error occurred: {e}, But I will retry!")
                                time.sleep(1)  # 等待1秒钟，然后再尝试执行
                                if try_times == 9:
                                    print("啊哦，抢课失败，下面的\"抢到了老师的课\"是假消息!")
                                    break
                        print(f"抢到了{teacher}老师的第三场课!")
                        if try_times != 9: no_lesson = False
                        break

                if no_lesson:
                    print(f"oh no!{teacher}老师的课现在还没有多出来的名额！")
                    print('----------------------------------------')

    def auto_doit(self):
        self.login_to_system()
        self.into_lesson_system()
        self.catch_lesson()