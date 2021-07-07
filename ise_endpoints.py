
import requests
import json
import urllib3
import sys, csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ISE_hostname="ise"
ISE_admin="apiadmin"
ISE_password="secret"

csvfilename = None
profilermode = False

header = ['index', 'MAC_address' ]
headerWithProfiler = ['index', 'MAC_address', 'Profile_Name' ]


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

def List_ISE_Endpoints_with_Profile(csvfilename = None):

  dev=0
  try:
    response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except Exception as err:
    print('Error: ISE is not available')
  res=json.loads(response.text)
  total=res["SearchResult"]["total"]
  #print("Total number of endpoints:",total)


  if csvfilename: 
    # open the file in the write mode
    f = open(csvfilename, 'w')
    # create the csv writer
    writer = csv.writer(f) 
    # write a row to the csv file

  if csvfilename:  
    writer.writerow(headerWithProfiler)
  print("index,MAC_address,Profile_Name")

  
  for device in res["SearchResult"]["resources"]:
    dev=dev+1

    if csvfilename:  
      # write a row to the csv file
      writer.writerow( [ dev , device['name'], GetProfileName( device['link']['href']) ]) 
    print(f"{dev},{device['name']},{GetProfileName( device['link']['href'])}")
      
  while "nextPage" in res["SearchResult"] :
  # use the next page reference after we've retrieved the first page    
    url = res["SearchResult"]["nextPage"]["href"]
    try:
      response = requests.get(url, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
      response.raise_for_status()
    except Exception as err:
      print('Error: wrong ISE request') 
    res = json.loads(response.text)
    for device in res["SearchResult"]["resources"]:
      dev=dev+1

      if csvfilename:  
        # write a row to the csv file
        writer.writerow( [ dev , device['name'], GetProfileName( device['link']['href']) ])

      print(f"{dev},{device['name']},{GetProfileName( device['link']['href'])}")

  if csvfilename:  
    # close the file
    f.close()    


def List_ISE_Endpoints(filename=None):

  dev=0
  baseurl = "https://"+ISE_hostname +":9060/ers/config/endpoint"
  try:
    response = requests.get(baseurl, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
    response.raise_for_status()
  except Exception as err:
    print('Error: wrong ISE request')
  res=json.loads(response.text)
  total=res["SearchResult"]["total"]
  #print("Total number of endpoints:",total)

  if csvfilename: 
    # open the file in the write mode
    f = open(csvfilename, 'w')
    # create the csv writer
    writer = csv.writer(f) 
    # write a row to the csv file

  if csvfilename:  
    writer.writerow(header)
  
  print("index,MAC_address")

  for device in res["SearchResult"]["resources"]:
    dev=dev+1
    
    if csvfilename:  
      # write a row to the csv file
      writer.writerow( [ dev , device['name'] ])
    
    print(f"{dev},{device['name']}") 
  
  while "nextPage" in res["SearchResult"] :
    # use the next page reference after we've retrieved the first page    
    url = res["SearchResult"]["nextPage"]["href"]
    try:
      response = requests.get(url, headers=headers, data=payload, verify=False, auth=(ISE_admin, ISE_password))
      response.raise_for_status()
    except Exception as err:
      print('Error: wrong ISE request')
    res = json.loads(response.text)
    for device in res["SearchResult"]["resources"]:
      dev=dev+1

      if csvfilename:  
        # write a row to the csv file
        writer.writerow([ dev , device['name'] ])
  
      print(f"{dev},{device['name']}" ) 

  if csvfilename:  
    # close the file
    f.close()

def SmartExit(outstring):
   print(f"Not supported option:{outstring}")
   print("HOW TO USE:")
   print("python3 ise_endpoints.py [profiling_info=true] [csvfilename=output.csv]" )
   sys.exit("Wrong argument")

#
# main
#
if __name__ == "__main__":
 
  for i in sys.argv:
    if i=="ise_endpoints.py": 
      continue

    split_string = i.split("=", 1)
    if split_string[0] == "profiling_info":
      if split_string[1] == 'true':
        profilermode = True
      elif profilermode == "false":
        profilermode = False
      else:
        SmartExit(i)

    elif split_string[0] == "csvfilename":
      csvfilename = split_string[1]
    else:
      SmartExit(i)

  if profilermode:
    List_ISE_Endpoints_with_Profile(csvfilename)
  else:  
    List_ISE_Endpoints(csvfilename)
