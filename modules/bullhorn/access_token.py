class BullhornAccessToken:
    def __init__(self, json_data):
        self.__access_token = ""
        self.__token_type = ""
        self.__expires_in = 0
        self.__refresh_token = ""
        if "access_token" in json_data:
            self.__access_token = json_data["access_token"]
        if "token_type" in json_data:
            self.__token_type = json_data["token_type"]
        if "expires_in" in json_data:
            self.__expires_in = json_data["expires_in"]
        if "refresh_token" in json_data:
            self.__refresh_token = json_data["refresh_token"]
    

    def getAccessToken(self):
        return self.__access_token

    def getTokenType(self):
        return self.__token_type

    def getExpiresIn(self):
        return self.__expires_in

    def getRefreshToken(self):
        return self.__refresh_token

