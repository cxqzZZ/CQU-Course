import re
import os
import time
import json

if __name__ == '__main__':
    user = json.load(open('../info/user.json', 'r', encoding='utf-8'))
    url = json.load(open('../info/serverurl.json', 'r', encoding='utf-8'))
    url["id"] = 0
    json.dump(url, open('../info/serverurl.json', 'w+', encoding='utf-8'))
    url = json.load(open('../info/serverurl.json', 'r', encoding='utf-8'))
    print(url["id"])
    print(user)


class login(object):
    def wait_time(self):
        import random
        time.sleep(1 + random.randint(0, 10) / 10)

    def ecrpyt_passwd(self):
        import hashlib
        m = hashlib.md5()
        m.update(self.password.encode('utf-8'))
        password = m.hexdigest()
        string = self.username + password.upper()[:30] + '10611'
        n = hashlib.md5()
        n.update(string.encode('utf-8'))
        res = n.hexdigest().upper()[:30]
        return res

    def changeServer(self, server=None):
        import random
        # x<=randint(x,y)<=y
        if(server is None):
            print("改变目标服务器...")
            self.server = random.randint(0, 3)
        else:
            self.server = server
        self.url = self.serverurl["{}".format(self.server)]['host']
        self.vs = self.serverurl["{}".format(self.server)]['vs']
        self.serverurl["id"] = "{}".format(self.server)
        print("目前请求链接:{}".format(self.url))

    def login(self):
        form = {
                'Sel_Type': 'STU',
                '__VIEWSTATE': self.vs,
                '__VIEWSTATEGENERATOR': self.vsg,
                'aerererdsdxcxdfgfg': '',
                'efdfdfuuyyuuckjg': self.ecrpyt_passwd(),
                'pcInfo': '',
                'txt_dsdfdfgfouyy': '',
                'txt_dsdsdsdjkjkjc': self.username,
                'txt_ysdsdsdskgf': '',
                'typeName': ''
            }
        print("正在登录……")
        res = self.session.post(self.url+'/_data/index_login.aspx', data=form, headers=self.headers)
        # 失败重试
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")
        x = soup.find_all(text=re.compile(r".*登录失败.*"), limit=1)
        if res.status_code != 200 or len(x) > 0:
            print("登陆失败，正在重试，请检查账户密码及服务器可用性")
            print(x)
            self.wait_time()
            self.changeServer()
            self.login()
        else:
            print("登陆成功")
            return True

    def getSelspecail(self):
        # now to do 完成专业代号以后的设定 22:40 2019/7/24
        res = self.session.get(self.url+self.path["btx"])
        if "&xn=" in res.text:
            s = re.findall(re.compile(r"'&xn=(\d+)&xq=(\d+)'"), res.text)
            # print(s)
            # print(len(s))
            if (len(s) == 1):
                xn = s[0][0]
                xq = s[0][1]
                self.path["selspecail"] += "&xn={}&xq={}".format(xn, xq)
                print("现在是{}学年，第{}学期".format(xn, xq))
            else:
                print("学年格式错误，重试...")
                self.changeServer()
                self.wait_time()
                return False
        else:
            print("未找到学年信息，重试...")
            self.changeServer()
            self.wait_time()
            return False
        res = self.session.get(self.url+self.path["selspecail"])
        if res.text.find("setTimeout(\"load_url()\",680);") == -1:
            self.selspecial = re.findall('<option value=(.*?) selected>', res.text)
            if len(self.selspecial) != 0:
                self.selspecial = self.selspecial[0]
            print("专业代号{}".format(self.selspecial))
            return True
        else:
            print("重新获取专业代号中...")
            self.changeServer()
            self.wait_time()
            return False

    def getInfo(self):
        while self.login():
            if (self.getSelspecail()):
                break
        print("获取信息成功")
        return True

    def __init__(self, session, path=".", *args, **kwargs):
        self.user = json.load(open(path+'/info/user.json', 'r', encoding='utf-8'))
        self.serverurl = json.load(open(path+'/info/serverurl.json', 'r', encoding='utf-8'))
        self.path = json.load(open(path+'/info/path.json', 'r', encoding='utf-8'))
        self.username = self.user["name"]
        self.password = self.user["password"]
        self.vsg = self.serverurl["vsg"]
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
        }
        self.session = session
        self.changeServer()
        self.getInfo()
        json.dump(self.serverurl, open(path+'/info/serverurl.json', 'w+', encoding='utf-8'))
