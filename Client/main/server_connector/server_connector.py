import json
import os

import requests
from tabulate import tabulate

from main.gui.DTO_models import map_obj_from_json, monster_obj_from_json, level_from_json


class ServerConnector:
    LOCAL_SERVER_LINK = "http://127.0.0.1:5000/"
    GET_LEADERBOARDS = "leaderboard"
    GET_USER = "user"
    GET_LEVEL = "level/"
    SAVE_LEADERBOARDS = "leaderboard/post"
    REGISTER_USER = "register"
    LOGIN_USER = "login"
    SESSION_COOKIE = "session"
    DATA_FILE = "data.txt"
    DATA_FILE_LOCATION = "data"

    @staticmethod
    def get_level(level:int, server_link: str = LOCAL_SERVER_LINK):
        level_response = requests.get(server_link+ServerConnector.GET_LEVEL+str(level))
        level_dict = json.loads(level_response.text)
        backgrounds = [map_obj_from_json(o['x'], o['y'], o['name']) for o in level_dict['backgrounds']]
        terrains = [map_obj_from_json(o['x'], o['y'], o['name']) for o in level_dict['terrains']]
        monsters = [monster_obj_from_json(o['x'], o['y'], o['name'], o['hp'], o['attack'], o['defense'])
                    for o in level_dict['monsters']]
        level = level_from_json(backgrounds, monsters, terrains)
        return level

    @staticmethod
    def get_leaderboards_formatted(level: int, server_link: str = LOCAL_SERVER_LINK):
        leaderboards = ServerConnector.get_leaderboards(level, server_link)
        if len(leaderboards) == 0:
            leaderboards.append(["No records", "at the", "moment"])

        formatted_leaderboard = tabulate(leaderboards,
                                         ["NAME", "LEVEL", "SCORE"],
                                         stralign='left',
                                         numalign="left"
                                         )
        print(formatted_leaderboard)
        return formatted_leaderboard

    @staticmethod
    def get_leaderboards(level: int, server_link: str = LOCAL_SERVER_LINK):
        data = {"level": level}
        r = requests.get(server_link + ServerConnector.GET_LEADERBOARDS, params=data)
        leaderboards_records = r.json()
        result = []
        for record in leaderboards_records:
            result.append([record["playerName"], record["levelId"], record["score"]])
        return result

    @staticmethod
    def get_user(server_link: str = LOCAL_SERVER_LINK):
        cookies = dict(session=ServerConnector.get_cookie())
        r: requests.Response = requests.get(server_link + ServerConnector.GET_USER, cookies=cookies)
        print(r.text)
        return r.json()[0]

    @staticmethod
    def save_leaderboard(score: int, level: int, server_link: str = LOCAL_SERVER_LINK):
        data = {"score": score, "level": level}
        cookies = dict(session=ServerConnector.get_cookie())
        r: requests.Response = requests.post(server_link + ServerConnector.SAVE_LEADERBOARDS, params=data,
                                             cookies=cookies)
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        return result_msg

    @staticmethod
    def register(login: str, password: str, server_link: str = LOCAL_SERVER_LINK):
        if login == "":
            return 400, "Enter username"
        if password == "":
            return 400, "Enter password"

        data = {"login": login}
        r: requests.Response = requests.post(server_link + ServerConnector.REGISTER_USER, params=data,
                                             data={"password": password})
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        return r.status_code.real, r.text

    @staticmethod
    def login(login: str, password: str, server_link: str = LOCAL_SERVER_LINK):
        if login == "":
            return 400, "Enter username"
        if password == "":
            return 400, "Enter password"
        data = {"login": login}
        r: requests.Response = requests.post(server_link + ServerConnector.LOGIN_USER, params=data,
                                             data={"password": password})
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        if r.status_code.real == 200 and r.text == "Logged in successfully as " + login:
            ServerConnector.save_data(r.cookies[ServerConnector.SESSION_COOKIE], login)
        return r.status_code.real, r.text

    @staticmethod
    def is_logged_in(server_link: str = LOCAL_SERVER_LINK):
        cookies = dict(session=ServerConnector.get_cookie())
        r: requests.Response = requests.post(server_link + ServerConnector.LOGIN_USER, cookies=cookies)
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        if r.status_code.real == 200:
            return True
        return False

    @staticmethod
    def save_data(cookie: str, login: str=""):
        f = open(os.path.join(ServerConnector.DATA_FILE_LOCATION, ServerConnector.DATA_FILE), 'w')
        print(cookie + " " + login)
        f.write(cookie)
        f.write("\n" + login)

        f.close()

    @staticmethod
    def get_cookie():
        path_to_file = os.path.join(ServerConnector.DATA_FILE_LOCATION, ServerConnector.DATA_FILE)
        if not os.path.isfile(path_to_file):
            f = open(path_to_file, 'w+')
            f.write("\n")
            f.close()

        f = open(path_to_file, 'r')
        lines = f.read().splitlines()
        f.close()
        if len(lines) != 2:
            f = open(path_to_file, 'w+')
            while len(lines) < 2:
                lines.append("")
                f.write("\n")
            f.close()
        return lines[0]
