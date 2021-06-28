# ISE_Endpoints

This python script lists the Endpoint of ISE. 

Please modify the ISE hostname, admin account and password in the script!

Use this way:

# WARNING:
The script has an optional switch, "profiling_info". If You run this script with this option, it is slow, because profiling query is NOT a bulk method! 
 

# Option 1: without profiling_info 

$ python3 ise_endpoints.py  
ISE Endpoints:  
Total number of endpoints: 140  
1,F0:18:9A:9A:B3:FE    
2,00:50:5A:AE:E3:39    
3,00:50:5A:AE:F3:34   
...  
139,00:0A:5A:0A:60:45   
140,00:51:5E:AE:AB:48   
  

# Option 2: with profiling_info [slow] 
  
$ python3 ise_endpoints.py profiling_info=true  
ISE Endpoints:  
Total number of endpoints: 140  
1,F0:18:9A:9A:B3:FE,Linux-Workstation  
2,00:50:5A:AE:E3:39,Microsoft-Workstation  
3,00:50:5A:AE:F3:34,Cisco-Device  
...  
139,00:0A:5A:0A:60:45,FreeBSD-Workstation  
140,00:51:5E:AE:AB:48,Cisco-Device  


Script can generate a CSV file if you direct the output into a CSV file, like this way:

$ python3 ise_endpoints.py profiling_info=true > output.csv
