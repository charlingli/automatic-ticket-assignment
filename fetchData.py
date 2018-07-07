import requests
from requests.auth import HTTPBasicAuth
from elasticsearch import Elasticsearch
import json
import sys
import datetime
from operator import itemgetter

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

INCIDENT_INDEX = "incident"
INCIDENT_TYPE = "incident"
RESOURCE_INDEX = "resource"
RESOURCE_TYPE = "resource"
LOG_INDEX = "log"
LOG_TYPE = "log"

es = Elasticsearch([{"host": "localhost", "port": 9200}])

if es.indices.exists(index="incident"):
    es.indices.delete(index="incident")

incident_mapping = {
    "incident": {
        "properties": {
            "number": {"type": "text"},
            "sys_id": {"type": "text"},
            "assignment_group": {
                "properties": {
                    "display_value": {"type": "keyword"},
                    "value": {"type": "keyword"}
                }
            },
            "assigned_to":{
                "properties": {
                    "display_value": {"type": "keyword"},
                    "value": {"type": "keyword"}
                }
            },
            "sys_updated_on":{"type": "date", "format": "yyyy-MM-dd HH:mm:ss"}
        }
    }
}
es.indices.create(INCIDENT_INDEX, body={"mappings": incident_mapping})

if not es.indices.exists(index="resource"):
    resource_mapping = {
        "resource": {
            "properties": {
                "team_name": {"type": "text"},
                "employee": {
                    "properties": {
                        "name": {"type": "keyword"},
                        "start_time": {"type": "date", "format": "hh:mm"},
                        "end_time": {"type": "date", "format": "hh:mm"},
                        "workload": {"type": "integer"}
                    }
                }
            }
        }
    }
    es.indices.create(RESOURCE_INDEX, body={"mappings": resource_mapping})

if not es.indices.exists(index="log"):
    log_mapping = {
        "log": {
            "properties": {
                "number": {"type": "keyword"},
                "assignment_group": {"type": "keyword"},
                "assigned_to": {"type": "keyword"},
                "sys_updated_on": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"}
            }
        }
    }
    es.indices.create(LOG_INDEX, body={"mappings": log_mapping})

maxTime = es.search(index=INCIDENT_INDEX, body={
    "aggs" : {
            "max_val" : { "max" : { "field" : "sys_updated_on" } }
        }
})

####    TODO Change ServiceNow instance
SN_REST_BASE_URL = "https://devXXXXX.service-now.com"
SN_REST_SUFFIX_URL = "/api/now/v1/table/incident"

if maxTime["hits"]["total"] != 0:
    maxTime = maxTime["aggregations"]["max_val"]["value_as_string"]
    latestTime = maxTime[:10] + "+" + maxTime[11:]
    SN_REST_PARAMS_URL = "?sysparm_display_value=true&sysparm_query=sys_updated_on>=" + latestTime
else:
    SN_REST_PARAMS_URL = "?sysparm_display_value=true"

URL = SN_REST_BASE_URL + SN_REST_SUFFIX_URL + SN_REST_PARAMS_URL
headers = {"Content-Type":"application/json", "Accept":"application/json"}
response = requests.get(URL, verify = False, auth = HTTPBasicAuth("admin", "Test1234"))

rawData = response.json()["result"]
for count, row in enumerate(rawData):
    cleanData = {key:row[key] for key in ("number", "sys_id", "assignment_group", "assigned_to", "sys_updated_on")}
    if cleanData["assignment_group"] == "":
        cleanData["assignment_group"] = {"display_value": "", "link": ""}
    if cleanData["assigned_to"] == "":
        cleanData["assigned_to"] = {"display_value": "", "link": ""}
    es.index(index=INCIDENT_INDEX, doc_type=INCIDENT_TYPE, id=count, body=cleanData)

jsonFile = open("data/resource.json", "r")

####    TODO Add a firstrun condition
# for index, data in enumerate(jsonFile):
#     postData = json.loads(data)
#     # print(postData["resource"]["employee"]["workload"])
#     es.index(index=RESOURCE_INDEX, doc_type=RESOURCE_TYPE, id=index, body=postData)
# jsonFile.close()

print('automatic-ticket-assignment: Retrieved Updated Ticket Data from ServiceNow')