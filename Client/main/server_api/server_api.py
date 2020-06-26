
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
import requests
class ServerApi:
    LOCAL_SERVER_LINK = "http://127.0.0.1:5000/"
    GET_LEADERBOARDS = "leaderboard"
    SAVE_LEADERBOARDS = "leaderboard/post"

    @staticmethod
    def get_leaderboards(level:int, server_link:str=LOCAL_SERVER_LINK):
        data = {"level": level}
        r = requests.get(server_link+ServerApi.GET_LEADERBOARDS, params=data)
        print(r.json())
        return r.json()

    @staticmethod
    def save_leaderboard(login:str,score:int,level:int, server_link: str = LOCAL_SERVER_LINK):
        data = {"login":login,"score":score,"level":level}
        r: requests.Response = requests.post(server_link + ServerApi.SAVE_LEADERBOARDS, params = data)
        result_msg = "status: "+str(r.status_code.real)+" response:"+r.text
        print(result_msg)
        return result_msg