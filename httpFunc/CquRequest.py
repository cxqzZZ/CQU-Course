import json


class CquRequest(object):
    # 封装get和post请求
    def get(self, url, params=None, headers=None):
        if headers is None:
            headers = self.__session.headers
        headers.update({'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"})
        res = self.__session.get(self.serverUrl+url, params=params, headers=headers)
        while res.status_code != 200:
            self.wait_time()
            res = self.__session.get(self.serverUrl + url, params=params, headers=headers)
        return res

    def post(self, url, data=None, headers=None):
        if headers is None:
            headers = self.__session.headers
        headers.update({'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"})
        res = self.__session.post(self.serverUrl + url, data=data, headers=headers)
        while res.status_code != 200:
            self.wait_time()
            res = self.__session.post(self.serverUrl+url, data=data, headers=headers)
        return res

    def __init__(self, session, path="."):
        self.__session = session
        self.url = json.load(open(path+'/info/serverurl.json', 'r', encoding='utf-8'))
        self.serverUrl = self.url[self.url["id"]]["host"]
