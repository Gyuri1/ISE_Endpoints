import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ISE_hostname="ise.local"
ISE_admin="admin"
ISE_password="secret"

total=0
payload={}
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

def GetProfileName(EndpointID):
  try:
    response = requests.get(EndpointID, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
  #print(response.text)
  
  res1=json.loads(response.text)

  profileID = res1["ERSEndPoint"]["profileId"]  

  if profileID == "":
      return "Not_Profiled"

  baseurl = "https://"+ISE_hostname +":9060/ers/config/profilerprofile/"+profileID
  try:
    response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
  #print(response.text)
  res2=json.loads(response.text)
  name=res2["ProfilerProfile"]["name"]
  #print(res2["ProfilerProfile"]["name"])
  return name


dev=0
print("ISE Endpoints:")
baseurl = "https://"+ISE_hostname +":9060/ers/config/endpoint"
try:
  response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
  response.raise_for_status()
except requests.exceptions.HTTPError as err:
  raise SystemExit(err)


res=json.loads(response.text)
total=res["SearchResult"]["total"]
print("Total number of endpoints:",total)

#print("Endpoints:",response.text)

for device in res["SearchResult"]["resources"]:
  dev=dev+1
  print(dev,":",device["name"], GetProfileName( device["link"]["href"] ))

while "nextPage" in res["SearchResult"] :
  # use the next page reference after we've retrieved the first page    
  url = res["SearchResult"]["nextPage"]["href"]
  try:
    response = requests.get(url, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

  res = json.loads(response.text)
  for device in res["SearchResult"]["resources"]:
    dev=dev+1
    print(dev,":",device["name"], GetProfileName( device["link"]["href"] ))
