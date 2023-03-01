import newClass
import time
import schedule
if __name__ == '__main__':
    log_id = '202200202032'
    passwd = 'sztu@250111'
    lessonType = 'plan'
    teachers_names = ['朱小琳'] # 许晴-日语 支慧-	音乐赏析； 刘亚男 袁雅洁
    lesson_select_set = [1]  # 1:第一节 2:第二节 4:第三节
    mainThreat = newClass.CatchProcession(log_id, passwd, lessonType, teachers_names, lesson_select_set)
    mainThreat.auto_doit()
    # schedule.every().day.at("13:20").do(mainThreat.auto_doit)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
