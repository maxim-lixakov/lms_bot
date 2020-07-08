import requests
import re


class User:

    def __init__(self, login, password, chat_id):
        self.login = login
        self.password = password
        self.chat_id = chat_id

    def lms_auth(self):
        login = self.login
        password = self.password
        data = {"user_login": login,
                "user_password": password,
                "group1[userLogin]": "Войти",
                "_qf__login_form": " "}
        with requests.Session() as s:
            s.post("https://lms.hse.ru/",
                       data=data, )
            r = s.get("https://lms.hse.ru/index.php?page=gradebook")
        name = re.findall(r'<li><span style="color: #f98012;">(.*)</span>', r.text)
        return name[0]

