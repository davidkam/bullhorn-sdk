import json
import time
import datetime

from urllib.parse import urlencode

from modules.bullhorn.session import BullhornSession
from modules.utilities.request import UtilitiesRequest



class BullhornData:
    def __init__(self):
        self.__session = BullhornSession()
        self.__session.createSession()

        self.__request = UtilitiesRequest()

    def getEntityById(self, entity, id, fields):
        url = "entity/%s/%s"%(entity, str(id))
        params = {}
        if len(fields):
            params["fields"] = ",".join(fields)

        return self.get(url, params)

    def searchEntity(self, entity, query, fields, start = 0, sort_field = None, count = None):
        params = {
            "start": start
        }
        if count is not None:
            params["count"] = count
        else:
            params["count"] = 500
        if sort_field is not None:
            params["sort"] = sort_field
        if len(fields):
            params["fields"] = ",".join(fields)
        url = "search/%s?"%(entity) + urlencode(params)
        data = {"query": query}
        return self.postJson(url, data)

    def queryEntity(self, entity, query, fields, start = 0, sort_field = None, count = None):
        params = {
            "start": start
        }
        if count is not None:
            params["count"] = count
        else:
            params["count"] = 20
        if sort_field is not None:
            params["sort"] = sort_field
        if len(fields):
            params["fields"] = ",".join(fields)
        url = "query/%s?"%(entity) + urlencode(params)
        data = {"where": query}
        return self.get(url, data)

    def dumpEntity(self, entity, fields, last_run_time = 0, current_run_time = None):
        # return self.dumpEntityWithQuery(entity, fields, last_run_time, current_run_time)
        return self.dumpEntityWithSearch(entity, fields, last_run_time, current_run_time)

    def dumpEntityWithQuery(self, entity, fields, last_run_time = 0, current_run_time = None):
        current_run = int(time.time() * 1000)
        seconds = datetime.datetime.now() - datetime.timedelta(days = 3)
        last_run = int(seconds.timestamp() * 1000)
        sort_field = "dateLastModified"
        all_results = []
        query = "dateLastModified > %s AND dateLastModified < %s" % (str(last_run), str(current_run))
        processed = 0
        done = False
        while not done:
            response = self.queryEntity(entity, query, fields, start = processed, sort_field = sort_field)
            data = json.loads(response["response"]["text"])
            num_results = len(data["data"])
            if num_results == 0:
                done = True
            else:
                processed += num_results
                all_results.extend(data["data"])
        return json.dumps(all_results)

    def dumpEntityWithSearch(self, entity, fields, last_run_time = 0, current_run_time = None):
        time_format = "%Y%m%d%H%M%S"
        last_run = datetime.datetime.fromtimestamp(last_run_time, datetime.timezone.utc)
        formatted_last_run = last_run.strftime(time_format)
        if current_run_time is None:
            formatted_current_run = datetime.datetime.now().strftime(time_format)
        else:
            current_run = datetime.datetime.fromtimestamp(current_run_time, datetime.timezone.utc)
            formatted_current_run = current_run.strftime(time_format)
        sort_field = "dateLastModified"
        all_results = []
        query = "dateLastModified:[%s TO %s]" % (str(formatted_last_run), str(formatted_current_run))
        processed = 0
        num_records = 1
        while processed < num_records:
            response = self.searchEntity(entity, query, fields, start = processed, sort_field = sort_field)
            data = json.loads(response["response"]["text"])
            print(data)
            num_records = data["total"]
            processed += data["count"]
            all_results.extend(data["data"])
        return json.dumps(all_results)

    def get(self, url, params):
        url = self.__session.getRestUrl() + '/' + url
        params["BhRestToken"] = self.__session.getRestToken()
        request = self.__request.get(url, params = params)
        return request

    def postJson(self, url, params):
        token = {"BhRestToken": self.__session.getRestToken()}
        url = self.__session.getRestUrl() + url + "&" + urlencode(token)
        request = self.__request.postJson(url, params = params)
        return request

