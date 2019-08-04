import json
import threading
from httpFunc.loginAndGetInfo import login as LG
from httpFunc.submitOneCourse import submitOne as SO
from httpFunc.allCourse import allCourse as AC


class multiThread(object):
    def mainThread(self):
        for x in self.tasks:
            m = threading.Thread(target=self.multiThread, args=(x,))
            m.start()

    def multiThread(self, classes="btx"):
        course = self.preference[classes]
        allCourse = AC(self.session, self.login.selspecial, classes=classes, path=self.path)
        courseList = allCourse.courseList
        for x in course:
            print("课程:{} 教师:{}".format(x, course[x]))
            multi = threading.Thread(target=SO, args=(self.session, courseList, x, course[x]))
            multi.start()
            self.threadID.append(multi)

    def __init__(self, session, path="."):
        self.path = path
        self.session = session
        self.threadID = []
        self.preference = json.load(open(path + '/info/preference.json', 'r', encoding='utf-8'))
        self.tasks = json.load(open(path + '/info/user.json', 'r', encoding='utf-8'))["tasks"]
        self.login = LG(self.session, self.path)
        self.mainThread()
