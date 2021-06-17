import requests
import json
import urllib3
import sys

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

baseurl = "https://"+ISE_hostname +":9060/ers/config/endpoint"
 

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
  res2=json.loads(response.text)
  try:
    name=res2["ProfilerProfile"]["name"]
  except:
    name="No_profilename_yet"
  return name

def List_ISE_Endpoints_with_Profile():
  dev=0
  try:
    response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

  res=json.loads(response.text)
  total=res["SearchResult"]["total"]
  print("Total number of endpoints:",total)

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

def List_ISE_Endpoints():
  dev=0
  try:
    response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

  res=json.loads(response.text)
  total=res["SearchResult"]["total"]
  print("Total number of endpoints:",total)

  for device in res["SearchResult"]["resources"]:
    dev=dev+1
    print(dev,":",device["name"])

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
      print(dev,":",device["name"])


# main 
if __name__ == "__main__":
    print("List ISE Endpoints:")
    if len(sys.argv) == 2:
      if str(sys.argv[1]) == "profiling_info=true":
        List_ISE_Endpoints_with_Profile()
        exit()
      else:
        print("HOW TO USE:")
        print("python3 ise_endpoints.py [profiling_info=true]" )
        exit()
    List_ISE_Endpoints()


