import requests
import json
import urllib3
import sys, csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ISE_hostname="10.10.20.70"
ISE_admin="apiadmin"
ISE_password="C1sco123"

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
  except Exception as err:
    raise RuntimeError(exception_string(err)) from err   
  try:
    json_response = json.loads(response.text)
    profileID = json_response["ERSEndPoint"]["profileId"]  
  except:  
    print(f'Error! Endpoint: {response}')
  if profileID == "" :
      return "Not_Profiled"
  baseurl = "https://"+ISE_hostname +":9060/ers/config/profilerprofile/"+profileID
  try:
    response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except requests.exceptions.HTTPError as err:
    print(f'Error: {err}, URL:{baseurl}, Endpoint: {json_response["ERSEndPoint"]}')
  try:
    json_response_profile=json.loads(response.text)
    name=json_response_profile["ProfilerProfile"]["name"]
  except:
    name="No_profilename_yet"
  return name

def List_ISE_Endpoints_with_Profile():
  dev=0
  try:
    response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except Exception as err:
    raise RuntimeError(exception_string(err)) from err 
  res=json.loads(response.text)
  total=res["SearchResult"]["total"]
  #print("Total number of endpoints:",total)
  print("index,MAC_address,Profile_Name")
  for device in res["SearchResult"]["resources"]:
    dev=dev+1
    print(f"{dev},{device['name']},{GetProfileName( device['link']['href'])}")
      
  while "nextPage" in res["SearchResult"] :
  # use the next page reference after we've retrieved the first page    
    url = res["SearchResult"]["nextPage"]["href"]
    try:
      response = requests.get(url, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
      response.raise_for_status()
    except Exception as err:
      raise RuntimeError(exception_string(err)) from err 
    res = json.loads(response.text)
    for device in res["SearchResult"]["resources"]:
      dev=dev+1
      print(f"{dev},{device['name']},{GetProfileName( device['link']['href'])}")

def List_ISE_Endpoints(filename=None):
  dev=0
  baseurl = "https://"+ISE_hostname +":9060/ers/config/endpoint"
  try:
    response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except Exception as err:
    raise RuntimeError(exception_string(err)) from err
  res=json.loads(response.text)
  total=res["SearchResult"]["total"]
  #print("Total number of endpoints:",total)
  print("index,MAC_address")
  for device in res["SearchResult"]["resources"]:
    dev=dev+1
    print(f"{dev},{device['name']}")
  
  while "nextPage" in res["SearchResult"] :
  # use the next page reference after we've retrieved the first page    
    url = res["SearchResult"]["nextPage"]["href"]
    try:
      response = requests.get(url, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
      response.raise_for_status()
    except Exception as err:
      raise RuntimeError(exception_string(err)) from err
    res = json.loads(response.text)
    for device in res["SearchResult"]["resources"]:
      dev=dev+1
      print(f"{dev},{device['name']}")

# main 
if __name__ == "__main__":
    #print("List ISE Endpoints:")
    if len(sys.argv) == 2:
      if str(sys.argv[1]) == "profiling_info=true":
        List_ISE_Endpoints_with_Profile()
      else:
        print("HOW TO USE:")
        print("python3 ise_endpoints.py [profiling_info=true]" )
    else:
      List_ISE_Endpoints()


