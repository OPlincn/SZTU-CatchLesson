from selenium import webdriver
import time
import schedule


def login_to_system(log_id, passwd):
    driver.find_element("xpath", r'//*[@id="j_username"]').send_keys(log_id)
    driver.find_element("xpath", r'//*[@id="j_password"]').send_keys(passwd)
    driver.find_element("xpath", r'//*[@id="loginButton"]').click()  # 登录
    time.sleep(1)
    driver.find_element("xpath", r'/html/body/div[5]/div[1]/section/ul/li[5]/div').click()  # 点击培养管理
    time.sleep(1)
    driver.find_element("xpath", r"/html/body/div[5]/div[1]/section/ul/li[5]/ul/li[3]/div").click()  # 点击选课管理
    time.sleep(1)
    driver.find_element("xpath", r'/html/body/div[5]/div[1]/section/ul/li[5]/ul/li[3]/ul/li[1]').click()  # 点击学生选课中心
    # 切换至框架Frame1,才能点击内嵌的A标签
    driver.switch_to.frame("Frame1")
    driver.find_element('xpath', r'//*[@id="attend_class"]/tbody/tr[2]/td[4]/a').click()  # 进入选课 得到token
    driver.switch_to.default_content()  # 回去原来的框架
    driver.switch_to.frame("Frame1")  # 再变到标签所在框架，这个流程似乎使必须的
    time.sleep(1)
    driver.find_element('xpath', r'/html/body/form/div/div/input[2]').click()  # 进入选课

def catch_lesson(lessonType):
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    if lessonType == 'plan':
        driver.find_element('xpath', r'/html/body/div[1]/div[1]/ul/li[2]/a').click()
    if lessonType == 'public':
        driver.find_element('xpath', r'/html/body/div[1]/div[1]/ul/li[3]/a').click()
    time.sleep(1)



def rob_lesson(teachers_names):
    driver.switch_to.default_content()  # 回去原来的框架
    driver.switch_to.frame('mainFrame')
    time.sleep(1)
    no_lesson = True
    how_many_times = 1
    while no_lesson:
        for teacher in teachers_names:
            print(f"第{how_many_times}次，开始检索{teacher}老师的课!\n")
            how_many_times += 1
            time.sleep(2)
            input_teacher = driver.find_element('xpath', '//*[@id="skls"]')
            input_teacher.clear()
            input_teacher.send_keys(teacher)
            time.sleep(1)
            driver.find_element('xpath', '/html/body/div[8]/input[4]').click()
            time.sleep(3)
            print(f"开始检索{teacher}老师的第一场课!")
            lesson_left = driver.find_element('xpath', '/html/body/div[9]/div/table/tbody/tr[1]/td[12]')
            if int(lesson_left.text) > 0:
                driver.find_element('xpath', r'/html/body/div[9]/div/table/tbody/tr[1]/td[14]/div/a').click()
                time.sleep(1)
                print(f"抢到了老师的第一场课!")
                no_lesson = False
                break
            print(f"没货\n\n开始检索{teacher}老师的第二场课!")
            lesson_left = driver.find_element('xpath', '/html/body/div[9]/div/table/tbody/tr[2]/td[12]')
            if int(lesson_left.text) > 0:
                driver.find_element('xpath', r'/html/body/div[9]/div/table/tbody/tr[2]/td[14]/div/a').click()
                # print(f'{lesson_left.text}')
                time.sleep(1)
                print(f"抢到了老师的第一场课!")
                no_lesson = False
                break
            if no_lesson: print("也没货\n")
            time.sleep(10)


def mainThreat():
    driver.get(url)
    login_to_system(log_id, passwd)
    catch_lesson(lessonType)
    rob_lesson(teachers_names)


global driver, url, teachers_names, passwd, lessonType
driver = webdriver.Chrome(r'\chromedriver\chromedriver.exe')  # 启动浏览器模拟
url = 'https://auth.sztu.edu.cn/idp/authcenter/ActionAuthChain?entityId=jiaowu'
driver.set_window_size(900, 1100)  # 设置浏览器大小
# 打开网页
teachers_names = {'许晴', '支慧'} # 许晴-日语 支慧-	音乐赏析； 刘亚男 袁雅洁
log_id = '202200202033'
passwd = 'sztu1008611!!'
lessonType = 'plan'
schedule.every().day.at("14:02").do(mainThreat)
while True:
    schedule.run_pending()
    time.sleep(1)
print('结束力')
