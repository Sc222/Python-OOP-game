from main.server_connector.server_connector import ServerConnector


class ServerErrorsHandler:

    @staticmethod
    def try_get_user(server_link: str = ServerConnector.LOCAL_SERVER_LINK):
        try:
            user = ServerConnector.get_user(ServerConnector.get_saved_username(), server_link)
        except Exception:
            return False, None
        else:
            return True, user

    @staticmethod
    def try_get_leaderboards_formatted(level: int, server_link: str = ServerConnector.LOCAL_SERVER_LINK):
        try:
            leaderboards = ServerConnector.get_leaderboards_formatted(level, server_link)
        except Exception:
            return False, None
        else:
            return True, leaderboards

    @staticmethod
    def try_is_logged_in(server_link: str = ServerConnector.LOCAL_SERVER_LINK):
        try:
            is_logged_in = ServerConnector.is_logged_in(server_link)
        except Exception:
            return False, False
        else:
            if is_logged_in:
                return True, True
            else:
                return True, False
