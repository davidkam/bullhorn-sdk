import requests
import json
import os
import time
from urllib.parse import urlparse, parse_qs
from modules.utilities.request import *
from modules.bullhorn.access_token import BullhornAccessToken

class BullhornSession:
    LOGIN_INFO_URL = "https://rest.bullhornstaffing.com/rest-services/loginInfo"
    AUTH_CODE_ACTION = "Login"
    AUTH_CODE_RESPONSE_TYPE = "code"
    ACCESS_TOKEN_GRANT_TYPE = "authorization_code"
    REFRESH_TOKEN_GRANT_TYPE = "refresh_token"
    BH_REST_TOKEN_KEY = "BhRestToken"
    BH_REST_URL_KEY = "restUrl"
    USERNAME = os.getenv("BH_USERNAME")
    PASSWORD = os.getenv("BH_PASSWORD")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    def __init__(self):
        self.__request = UtilitiesRequest()
        self.__login_info = None
        self.__access_token = None
        self.__rest_token = None
        self.__rests_url = None
        self.__expiration = None

    def createSession(self):
        self.__expiration = int(time.time()) + (60 * 10)
        self.getToken(self.getAuthCode())
        self.login()

    def getAuthCode(self):
        url = self.getAuthorizeUrl()
        params = {
            "client_id": self.CLIENT_ID,
            "response_type": self.AUTH_CODE_RESPONSE_TYPE,
            "action": self.AUTH_CODE_ACTION,
            "username": self.USERNAME,
            "password": self.PASSWORD,
        }
        request = self.__request.post(url, params = params, allow_redirects = False)
        if request["status"] == 302:
            if "Location" in request["response"]["headers"]:
                url = request["response"]["headers"]["Location"]
                parsed_url = urlparse(url)
                params = parse_qs(parsed_url.query)
                if "code" in params:
                    return params["code"]

        return None
            
    def getToken(self, code):
        url = self.getTokenUrl()
        params = {
            "grant_type": self.ACCESS_TOKEN_GRANT_TYPE,
            "code": code,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
        }
        request = self.__request.post(url, params = params, allow_redirects = False)
        self.__access_token = BullhornAccessToken(json.loads(request["response"]["text"]))

    def login(self):
        url = self.getLoginUrl()
        params = {
            "version": "*",
            "access_token": self.__access_token.getAccessToken(),
        }
        request = self.__request.get(url, params = params, allow_redirects = False)
        data = json.loads(request["response"]["text"])
        self.__rest_token = data[self.BH_REST_TOKEN_KEY]
        self.__rest_url = data[self.BH_REST_URL_KEY]

    def getAuthorizeUrl(self):
        return self.getBaseOauthUrl() + "/authorize"

    def getTokenUrl(self):
        return self.getBaseOauthUrl() + "/token"

    def getLoginUrl(self):
        return self.getBaseRestUrl() + "/login"

    def getBaseOauthUrl(self):
        if self.__login_info is None:
            self.__login_info = self.getLoginInfo()
        return self.__login_info["oauthUrl"]

    def getBaseRestUrl(self):
        if self.__login_info is None:
            self.__login_info = self.getLoginInfo()
        return self.__login_info["restUrl"]

    def getLoginInfo(self):
        params = {
            "username": self.USERNAME
        }
        request = self.__request.get(self.LOGIN_INFO_URL, params = params)
        data = json.loads(request["response"]["text"])
        return data

    def getRestUrl(self):
        return self.__rest_url

    def getRestToken(self):
        now = int(time.time())
        if now > self.__expiration:
            print("refreshing token")
            self.createSession()
        return self.__rest_token
