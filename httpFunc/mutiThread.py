import json
import threading
if __name__ == "__main__":
    from loginAndGetInfo import login as LG
    from submitOneCourse import submitOne as SO
    from allCourse import allCourse as AC
else:
    from httpFunc.loginAndGetInfo import login as LG
    from httpFunc.submitOneCourse import submitOne as SO
    from httpFunc.allCourse import allCourse as AC


class mutiThread(object):
    def singleThread(self):
        self.login = LG(self.session, self.path)
        self.allCourse = AC(self.session, self.login.selspecial, path=self.path)
        self.courseList = self.allCourse.courseList

    def mutiThread(self):
        self.threadID = []
        for x in self.course:
            print("课程:{} 教师:{}".format(x, self.course[x]))
        muti = threading.Thread(target=SO, args=(self.session, self.courseList, x, self.course[x]))
        muti.start()
        self.threadID.append(muti)

    def __init__(self, session, classes="btx", path="."):
        self.path = path
        self.session = session
        self.classes = classes
        self.preference = json.load(open(path+'/info/preference.json', 'r', encoding='utf-8'))
        self.course = self.preference[self.classes]
        self.singleThread()
        self.mutiThread()
# now to do 完成多线程
