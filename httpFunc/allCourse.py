import json
from PIL import Image
from bs4 import BeautifulSoup

if __name__ == "__main__":
    from CquRequest import CquRequest as CR
else:
    from httpFunc.CquRequest import CquRequest as CR


class allCourse(object):
    def getCaptcha(self):
        res = self.http.get(self.path["tsCaptcha"])
        with open("./img.gif", "wb+") as fp:
            fp.write(res.content)
        img = Image.open('./img.gif')
        img.show()
        self.captcha = input("请输入验证码\n")
        print(self.captcha)

    def search(self):
        # 检索老师
        search_data = {
            "btx": {
                'sel_lx': '0',
                'SelSpeciality': self.selspecial,
                'Submit': '%BC%EC%CB%F7',
                # mean url decode gb2312 to 检索
                # 'kclbmc': 'Nothing'
            },
            "eng": {
                'sel_lx': '0',
                'SelSpeciality': self.selspecial,
                'Submit': '%BC%EC%CB%F7',
                'kclb3': "60",
            },
            "ts": {
                'SelSpeciality': self.selspecial,
                'sel_xq': '4',
                'chk_kyme': '1',
                'txt_yzm': self.captcha,
                'sel_lx': '4',
                'kclb3': '',
                'Submit': '%BC%EC%CB%F7',
            }
        }
        if self.classes == "ts":
            self.getCaptcha()
        while True:
            res = self.http.post(self.path['check{}'.format(self.classes)], search_data[self.classes])
            if (res.status_code != 200):
                print("请求响应状态码:{}".format(res))
                print("重新尝试提交表单中")
                self.wait_time()
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            print("Respons search:<{}>".format(res.status_code))
            forms = soup.find_all("form")
            for form in forms:
                if "%b7%c7%d1%a1%bf%ce%ca%b1%bc%e4%a3%a1" in form.get("action"):
                    print("不在选课时间内")
                    import sys
                    sys.exit()
            self.courseList = soup

    def __init__(self, session, selspecial, classes="btx", path="."):
        # ->self.coursesList
        self.selspecial = selspecial
        self.session = session
        self.classes = classes
        self.http = CR(self.session)
        self.path = json.load(open(path+'/info/path.json', 'r', encoding='utf-8'))
        self.search()
