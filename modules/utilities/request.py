import requests
import json
from urllib.parse import urlencode


class UtilitiesRequest:
    API_RETRY = 3
    VALID_HTTP_RESPONSE_CODES = [200, 302, 304]


    def get(self, url, params = None, headers = None, allow_redirects = True):
        if params is not None and type(params) is dict:
            url += "?" + urlencode(params)
        return self.makeCall("GET", url, headers = headers, allow_redirects = allow_redirects)


    def post(self, url, params = None, headers = None, allow_redirects = True):
        return self.makeCall("POST", url, params = params, headers = headers, allow_redirects = allow_redirects)

    def postJson(self, url, params = None, headers = None, allow_redirects = True):
        return self.makeCall("POST_JSON", url, params = params, headers = headers, allow_redirects = allow_redirects)


    def makeCall(self, method, url, params = None, headers = None, allow_redirects = True):
        method = method.upper()
        attempt = 0
        while attempt < self.API_RETRY:
            try:
                response = None
                if method == "POST":
                    response = requests.post(url, data = params, headers = headers, allow_redirects = allow_redirects)
                if method == "POST_JSON":
                    response = requests.post(url, json = params, headers = headers, allow_redirects = allow_redirects)
                if method == "GET":
                    response = requests.get(url, headers = headers, allow_redirects = allow_redirects)

                if response is None:
                    raise InvalidActionException(method)

                status_code = ""
                if hasattr(response, "status_code"):
                    status_code = response.status_code

                if status_code not in self.VALID_HTTP_RESPONSE_CODES:
                    raise InvalidResponseException(status_code, response)

                return_obj = {}
                return_obj["status"] = status_code
                return_obj["response"] = self.parseResponse(response)
                return_obj["request"] = self.parseRequest(response)
                return return_obj
            except InvalidResponseException as e:
                raise Exception(e.message)
            except InvalidActionException as e:
                raise Exception(e.message)
            except Exception as e:
                attempt += 1

        raise Exception("Max number of retries exceeded")


    def parseRequest(self, response):
        request_obj = {}
        request_obj["method"] = ""
        request_obj["url"] = ""
        request_obj["headers"] = {}
        request_obj["body"] = ""
    
        if hasattr(response, "request"):
            if hasattr(response.request, "headers"):
                request_obj["headers"] = response.request.headers
            if hasattr(response.request, "body"):
                request_obj["body"] = response.request.body
            if hasattr(response.request, "method"):
                request_obj["method"] = response.request.method
            if hasattr(response.request, "url"):
                request_obj["url"] = response.request.url
        return request_obj

    def parseResponse(self, response):
        response_obj = {}
        response_obj["headers"] = {}
        response_obj["text"] = ""
        if hasattr(response, "headers"):
            response_obj["headers"] = response.headers
        if hasattr(response, "text"):
            response_obj["text"] = response.text
        return response_obj

class InvalidResponseException(Exception):
    def __init__(self, status_code, response):
        self.message = str(status_code)
        if hasattr(response, "text"):
            self.message += ": " + response.text
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"

class InvalidActionException(Exception):
    def __init__(self, method):
        self.message = method + " is not a supported action"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
