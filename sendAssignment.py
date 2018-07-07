import requests
from requests.auth import HTTPBasicAuth
from elasticsearch import Elasticsearch
import json
import sys
import datetime
from operator import itemgetter
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

INCIDENT_INDEX = 'incident'
INCIDENT_TYPE = 'incident'
RESOURCE_INDEX = 'resource'
RESOURCE_TYPE = 'resource'
LOG_INDEX = 'log'
LOG_TYPE = 'log'

####    TODO Change ServiceNow instance
SN_REST_BASE_URL = 'https://devXXXXX.service-now.com'
SN_REST_SUFFIX_URL = '/api/now/v1/table/incident'
headers = {'Content-Type':'application/json', 'Accept':'application/json'}

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

incidentRes = es.search(index=INCIDENT_INDEX, body={
    "query": {
    "bool": {
      "must": [
        { "match" : { 
          "assignment_group.display_value" : "Database" }
        },
        { "match" : { 
          "assigned_to.display_value" : "" }
        }
      ]
    }
  },
  "from": 0,
  "size": 10000
})

incidentsPending = []
for hit in incidentRes['hits']['hits']:
    incidentsPending.append(["%s" % hit["_source"]["sys_id"], "%s" % hit["_source"]["number"]])

#### BUG The GT range query does NOT return expected results! 
####    More investigation needed.
####    Update: End date is not being saved as date, but as string.
####    Try reindexing.
currentTime = str(datetime.datetime.now().time())[:5]
shiftRes = es.search(index=RESOURCE_INDEX, body={
  "query": {
    "bool": {
      "must": [
        { "match" : { 
          "resource.team_name" : "Database" }
        }, 
        { 
          "range" : {
            "resource.employee.start_time" : {
              "lte" :  currentTime
            }
          }
        }, 
        { 
          "range" : {
            "resource.employee.end_time" : {
              "gt" :  currentTime
            }
          }
        }
      ]
    }
  },
  "from": 0,
  "size": 10000
})

shiftFree = []
workloads = []
for hit in shiftRes['hits']['hits']:
    shiftFree.append(hit)

for incident in incidentsPending:
    for i in range(0, shiftRes['hits']['total']):
        if int(shiftFree[i]["_source"]["resource"]['employee']['workload']) == int(min(shift["_source"]["resource"]["employee"]["workload"] for shift in shiftFree)):
            shiftFree[i]["_source"]["resource"]['employee']['workload'] = int(shiftFree[i]["_source"]["resource"]['employee']['workload']) + 1
            ticket_url = SN_REST_BASE_URL + SN_REST_SUFFIX_URL + "/" + incident[0]
            
            ####    TODO Change auth
            response = requests.put(ticket_url, verify=False, auth=HTTPBasicAuth("uName", "pWord"), headers=headers, data='{"assigned_to":"' + shiftFree[i]["_source"]["resource"]['employee']['name'] + '"}')
            logTime = str(datetime.datetime.now())[:-7]
            logData = {"number": incident[1], "assignment_group": "Database", "assigned_to": shiftFree[i]["_source"]["resource"]['employee']['name'], "sys_updated_on": logTime}
            es.index(index=LOG_INDEX, doc_type=LOG_TYPE, body=logData)
            es.index(index=RESOURCE_INDEX, doc_type=RESOURCE_TYPE, id=shiftFree[i]['_id'], body=shiftFree[i]["_source"])
            break

print('automatic-ticket-assignment: Tickets Assigned Successfully')