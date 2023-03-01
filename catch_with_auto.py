import newClass
import time
import schedule
if __name__ == '__main__':
    log_id = '202200101001'  # 统一认证平台登陆账号(学号)
    passwd = 'sztu6666666999'  # 统一认证平台密码
    lessonType = 'plan'  # 填plan或者public，plan是计划选课，public是公选课
    teachers_names = ['大大怪', '小小怪'] # 填入你想抢的课的老师名字，多个名字以逗号分隔
    lesson_select_set = [1]  # 1:第一节 2:第二节 4:第三节, 那么填5就是抢第一和第二，填6就是第二和第三
    mainThreat = newClass.CatchProcession(log_id, passwd, lessonType, teachers_names, lesson_select_set)
    mainThreat.auto_doit()
    # 以下代码实现定时启动
    # schedule.every().day.at("13:20").do(mainThreat.auto_doit)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
