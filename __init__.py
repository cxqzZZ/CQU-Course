import os
import requests
from httpFunc.multiThread import multiThread as MT


class CQUCourse(object):
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.session = requests.session()
        # self.login = LG(self.session, self.path)
        # self.allCourse = AC(self.session, self.login.selspecial)
        # self.courseList = self.allCourse.courseList
        self.mt = MT(self.session, path=self.path)


CQUCourse()
