import os

import requests
from tabulate import tabulate

from main.server_connector.api import Api


class ServerConnector:


    @staticmethod
    def get_leaderboards_formatted(level: int, server_link: str = Api.LOCAL_SERVER_LINK):
        leaderboards = ServerConnector.get_leaderboards(level, server_link)
        if len(leaderboards) == 0:
            leaderboards.append(["No records", "at the", "moment"])
        formatted_leaderboard = tabulate(leaderboards,
                                         ["NAME", "LEVEL", "SCORE"],
                                         tablefmt="simple")
        return formatted_leaderboard

    @staticmethod
    def get_leaderboards(level: int, server_link: str = Api.LOCAL_SERVER_LINK):
        leaderboards_records = Api.get_leaderboards(level, server_link)
        result = []
        for record in leaderboards_records:
            result.append([record["playerName"], record["levelId"], record["score"]])
        return result

    @staticmethod
    def save_leaderboard(login: str, score: int, level: int, cookie:str, server_link: str = Api.LOCAL_SERVER_LINK):
        data = {"login": login, "score": score, "level": level}
        cookies = dict(session=cookie)
        r: requests.Response = requests.post(server_link + Api.SAVE_LEADERBOARDS,params=data,cookies = cookies)
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        return result_msg

    @staticmethod
    def register(login: str, password: str, server_link: str = Api.LOCAL_SERVER_LINK):
        data = {"login": login}
        r: requests.Response = requests.post(server_link + Api.REGISTER_USER, params=data, data={"password":password})
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        return result_msg

    @staticmethod
    def login(login: str, password: str, server_link: str = Api.LOCAL_SERVER_LINK):
        data = {"login": login}
        r: requests.Response = requests.post(server_link + Api.LOGIN_USER, params=data, data={"password":password})
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        if r.status_code.real==200 and r.text=="Logged in successfully as " + login:
            ServerConnector.save_cookie(r.cookies[Api.SESSION_COOKIE])
        return result_msg

    @staticmethod
    def is_logged_in(server_link: str = Api.LOCAL_SERVER_LINK):
        cookies = dict(session=ServerConnector.get_cookie())
        r: requests.Response = requests.post(server_link + Api.LOGIN_USER, cookies=cookies)
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        if r.status_code.real ==200:
            return True
        return False

    @staticmethod
    def save_cookie(cookie:str):
        f = open(os.path.join(Api.COOKIES_LOCATION, Api.COOKIES_FILE), 'w')
        print(cookie)
        f.write(cookie)
        f.close()

    @staticmethod
    def get_cookie():
        path_to_file = os.path.join(Api.COOKIES_LOCATION, Api.COOKIES_FILE)
        if not os.path.isfile(path_to_file):
            f = open(path_to_file, 'w')
            f.write("")
            f.close()
        f = open(path_to_file, 'r')
        cookie = f.readline()
        f.close()
        print(cookie)
        return cookie

