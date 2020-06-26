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
    def save_leaderboard(login: str, score: int, level: int, server_link: str = Api.LOCAL_SERVER_LINK):
        data = {"login": login, "score": score, "level": level}
        r: requests.Response = requests.post(server_link + Api.SAVE_LEADERBOARDS, params=data)
        result_msg = "status: " + str(r.status_code.real) + " response:" + r.text
        print(result_msg)
        return result_msg
