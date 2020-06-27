import requests


class Api:
    LOCAL_SERVER_LINK = "http://127.0.0.1:5000/"
    GET_LEADERBOARDS = "leaderboard"
    SAVE_LEADERBOARDS = "leaderboard/post"
    REGISTER_USER = "register"
    LOGIN_USER = "login"
    SESSION_COOKIE = "session"
    DATA_FILE = "data.txt"
    DATA_FILE_LOCATION = "data"
    @staticmethod
    def get_leaderboards(level: int, server_link: str = LOCAL_SERVER_LINK):
        data = {"level": level}
        r = requests.get(server_link + Api.GET_LEADERBOARDS, params=data)
        # print(r.json())
        return r.json()

    @staticmethod
    def save_leaderboard(login: str, score: int, level: int, server_link: str = LOCAL_SERVER_LINK):
        data = {"login": login, "score": score, "level": level}
        r: requests.Response = requests.post(server_link + Api.SAVE_LEADERBOARDS, params=data)
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        # print(result_msg)
        return result_msg
