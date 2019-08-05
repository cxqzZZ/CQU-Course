import re
import json
from bs4 import BeautifulSoup

if __name__ == "__main__":
    from CquRequest import CquRequest as CR
else:
    from httpFunc.CquRequest import CquRequest as CR


class submitOne(object):
    def chose(self):
        count = 0
        # rg=re.compile(r"value+\"(.*)\"")
        nameOfSubject = re.compile(r"chkKC.*")
        nameOfWindows = re.compile(r"winSKBJ.*")
        nameOfKcxf = re.compile(r"kcxf.*")
        nameOfChkSKBJ = re.compile(r"chkSKBJ\d+")

        allWindows = self.courseList.find_all(id=nameOfWindows)
        allSubjects = self.courseList.find_all(id=nameOfSubject)
        allCredit = self.courseList.find_all(id=nameOfKcxf)
        allChkSKBJ = self.courseList.find_all(id=nameOfChkSKBJ)

        count = len(allSubjects)
        # 无法修改mcount变量-->赋值发生在修改前 已更正
        self.mcount = len(allSubjects)
        infos = []
        index = 0

        for i in range(0, count):
            # bs4的get方法用来取得标签对象中的属性值，tag.string是tag的内容
            # python中 一个变量可以看作是一个指针，而使用中间变量给list赋值其实是赋的中间变量的地址，
            # 而不是真正想要的变量，因此要直接将变量的地址传给list
            # 如temp=x->(temp->x),list.append(temp)->(list.append(&temp))
            # 因此, python中的= -> =& ?
            # 如a->2, b=a--->b->a,此时 a=3-->a->3, 则b->a->3
            # 所以python中是传地址
            infos.append({
                "valueSub": allSubjects[i].get("value"),
                "valueWin": allWindows[i].get("value"),
                "credit": allCredit[i].get("value"),
                "chkSKBJ": allChkSKBJ[i].get("value"),
                "id": i,
            })

        print('-'*20)

        # print("课程值:"+infos[i]["valueSub"])
        # print("网页值:" + infos[i]["valueWin"])
        # print("学分:" + infos[i]["credit"])
        # print("教师编码",infos[i]["chkSKBJ"])

        print("检索结果：")
        # 此处已经开始根据个人设置查询
        parttern = re.compile((".*" + self.course + ".*"))
        for info in infos:
            x = re.findall(parttern, info["valueSub"])
            if len(x) != 0:
                print(x)
                index = info["id"]

        print("Info len:{}".format(len(infos)))
        print("Index find:{}".format(index))
        # index是目标课程在列表中的位置 infos是所有课程的信息，在提交表单的时候需要用到
        self.index = index
        self.infos = infos

    def query(self):
        while True:
            openWindow_data = {
                "lx": "BX",
                "id": "",
                "skbjval": "",
                }
            # link[i]->{
            #     "id": subject id,
            #     "valueSub": "subject's code",
            #     "valueWin": "link",
            # }
            index = self.index
            link = self.infos
            data = []
            # 查询字符串（名称/值对）
            # 参数部分：从“？”开始到“#”为止之间的部分为参数部分，又称搜索部分、查询部分。
            url = ("?lx={}&id={}&skbjval={}".format(openWindow_data["lx"], link[index]["valueWin"], openWindow_data["skbjval"]))
            data.append({
                "response": self.http.get(self.path["skbj"] + url),
                "subID": link[index]["valueSub"],
                "credit": link[index]["credit"],
                "id": link[index]["id"]
                })
            # data->{
            # 课程response
            # 课程id
            # 课程学分
            # }

            # name=rad_0 name=rad_2 name不同的话都是必须要选一个的
            teacher = []
            rad = "rad_"
            # need subID
            for x in data:
                soup = BeautifulSoup(x["response"].text, "html.parser")
                cae = re.findall(r"(\[.*)\$", x["subID"])
                if len(cae) != 0:
                    print("课程：{}|学分：{}".format(cae[0], x["credit"]))
                    x["subject"] = cae[0]
                    for x in soup.find_all(id=re.compile(rad + ".*?")):
                        # print(x.get("value"))
                        va = x.get("value")
                        # 匹配的字符默认是最后一个遇到的
                        teacher.append({
                            "subject": cae[0],
                            "name": re.search(r"\@(.*)\@", va).group(1),
                            "teacher": re.search(r"\](.*)\@.*\@", va).group(1),
                            "code": re.search(r"\@.*\@(.*)", va).group(1),
                        })
                else:
                    print("解析教师id错误")
                    self.wait_time()
                    print("正在重试...")
                    continue
            self.data = data
            self.teacher = teacher
        # teacher[]->教授科目 (name)教师的组 教师的名字 教师的代码

    def transform(self, x, y):
        y.append({
                    "name": x["name"],
                    "subject": x["subject"],
                    "teacher": x["teacher"],
                    "code": x["code"]
                })

    def getAllCode(self):
        # self,codeList包含着页面中检索到的信息， 可以不用重新检索
        self.codeList = {
        }
        once = 1
        for index, x in enumerate(self.teacher):
            print("课程：{} 教师：{}".format(x["subject"], x["teacher"]))
            flag = self.teacher[0]
            if (index != 0):
                if (flag["name"] == x["name"]):
                    self.transform(x, self.codeList[flag["name"]])
                else:
                    if (once == -1):
                        self.codeList[x["name"]] = []
                        once = 0
                    self.transform(x, self.codeList[x["name"]])
            else:
                if (once == 1):
                    self.codeList[flag["name"]] = []
                    once = -1
                self.transform(x, self.codeList[flag["name"]])

    def getSubmitCode(self):
        # 从self.codeList中获取到需要提交的内容
        self.submitCode = []
        for key in self.codeList:
            matchCode = []
            count = 0
            for x in self.list:
                for value in self.codeList[key]:
                    if (x in value["teacher"]):
                        count += 1
                        self.transform(value, matchCode)
            if (count == 0):
                import random
                n = random.randint(0, len(self.codeList[key])-1)
                self.transform(self.codeList[key][n], matchCode)
                print("随机选择{}".format(self.codeList[key][n]["teacher"]))
            if (len(matchCode) == 0):
                print("匹配出错， 课程名称{}".format(self.course))
                import _thread
                _thread.exit()
            self.submitCode.append(matchCode[0])
        for x in self.submitCode:
            print("匹配结果：{}|{}".format(x["subject"], x["teacher"]))

    def delFailedTeacher(self, failedTeacher):
        self.codeList[failedTeacher["name"]].remove(failedTeacher)

    def submit(self):
        flags = True
        while flags:
            str_id = 'TTT'
            form_data = {}
            submit_data = {}
            teacherCode = self.submitCode

            for x in teacherCode:
                print("已选课程：{} 任课教师：{}".format(x["subject"], x["teacher"]))

            for x in range(0, self.mcount):
                form_data["chkSKBJ{}".format(x)] = self.info[x]["chkSKBJ"]
                form_data["kcxf{}".format(x)] = self.info[x]["credit"]

            for da in self.data:
                flag = True
                for index, x in enumerate(teacherCode):
                    if da["subject"] == x["subject"]:
                        if(flag):
                            form_data["chkSKBJ{}".format(da["id"])] = x["code"]
                            flag = False
                        else:
                            form_data["chkSKBJ{}".format(da["id"])] = form_data["chkSKBJ{}".format(da["id"])] + ";" + x["code"]
            for m in self.data:
                for i in teacherCode:
                    if m["subject"] == i["subject"]:
                        form_data["chkKC{}".format(m["id"])] = m["subID"]

            def takele(data):
                return data["id"]

            self.data.sort(key=takele)

            for inf in self.data:
                str_id += ',' + form_data["chkSKBJ{}".format(inf["id"])] + '#' + inf["subID"]
            for count in range(0, self.mcount):
                if ("chkKC{}".format(count) in form_data.keys()):
                    submit_data["kcxf{}".format(count)] = form_data["kcxf{}".format(count)]
                    submit_data["chkKC{}".format(count)] = form_data["chkKC{}".format(count)]
                    submit_data["chkSKBJ{}".format(count)] = form_data["chkSKBJ{}".format(count)]
                else:
                    submit_data["kcxf{}".format(count)] = form_data["kcxf{}".format(count)]
                    submit_data["chkSKBJ{}".format(count)] = form_data["chkSKBJ{}".format(count)]

            submit_data["mcount"] = self.mcount
            submit_data['sel_lx'] = '0'
            submit_data['sel_xq'] = '%'
            submit_data['SelSpeciality'] = self.selspecial
            submit_data['kclb3'] = '%'
            submit_data['chk_kyme'] = '0'
            submit_data['id'] = str_id
            submit_data['yxsjct'] = '0'
            submit_data['txt_yzm'] = ''
            import urllib
            upload = urllib.parse.urlencode(submit_data, encoding='gb2312')
            print("提交...")
            res = self.http.post(self.path["submit{}".format(self.classes)] + upload)

            if res.status_code != 200:
                continue

            resoup = BeautifulSoup(res.text, "html.parser")
            tips = resoup.find_all(text=re.compile(r"选课.*的课程"))
            for index, tip in enumerate(tips):
                if ("选课成功" in tip):
                    print(tip)
            for index, tip in enumerate(tips):
                if ("选课失败" in tip):
                    print(tip)
                    if ("突破人数上限" in tip):
                        # 选课失败的课程：[AEME21112]理论力学（Ⅲ ），原因：突破人数上限，逗号是全角符号
                        for x in self.submitCode:
                            self.delFailedTeacher(x)
                    else:
                        print("失败科目:{}".format(self.course))
                        import sys
                        sys.exit()
                    print("正在重试...")
                else:
                    flags = False
        for x in self.submitCode:
            print("成功:{}|{}".format(x["subjetc"], x["teacher"]))

    def __init__(self, session, courseList, oneCourse, teacherList, path=".", classes="btx"):
        self.courseList = courseList
        self.course = oneCourse
        self.list = teacherList
        self.session = session
        self.classes = classes
        self.failedList = []
        self.url = json.load(open(path+'/info/serverurl.json', 'r', encoding='utf-8'))
        self.path = json.load(open(path+'/info/path.json', 'r', encoding='utf-8'))
        self.http = CR(self.session, path)
        self.query()
        self.chose()
        self.getAllCode()
        self.getSubmitCode()
        self.submit()
