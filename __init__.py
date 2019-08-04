import os
import requests
from httpFunc.multiThread import multiThread as MT


class CQUCourse(object):
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.session = requests.session()
        MT(self.session, self.path)


CQUCourse()
