import os
import requests
import threading
from httpFunc.multiThread import multiThread as MT


class CQUCourse(object):
    def all(self):
        for x in self.tasks:
            m = threading.Thread(target=MT, args=(self.session, x, self.path))
            m.start()

    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.session = requests.session()
        self.tasks = ["btx", "ts", "eng"]
        self.all()


CQUCourse()
