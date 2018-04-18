#!/usr/bin/env python
import requests
import json
import time
import sys

# Disable all warning messages since we're dealing with a
# self-signed certificate on APIC-EM
requests.packages.urllib3.disable_warnings()
'''
#################################################################################################################################################################
ENatics is a beta project about Software Defined Networking, and created by Jon Warner Campo. For any issues or concerns, you may email him at joncampo@cisco.com.
See Terms of Service - https://arcane-spire-45844.herokuapp.com/terms
See Privacy Policy - https://arcane-spire-45844.herokuapp.com/privacy
#################################################################################################################################################################
'''

########################################################################
def dnac_checkStatus(BASE_URL,DNAC_Auth):
    
    FULL_URL = 'https://'+BASE_URL+'/api/system/v1/auth/login'
    
    headers = {
                "Authorization": DNAC_Auth,
                'Content-Type': 'application/json'
            }

    status =  requests.get(FULL_URL, headers=headers, verify=False)
    raw_header=status.headers['Set-Cookie'].split("=")
    raw_cookie=raw_header[1].split(";")
    DNAC_Cookies=raw_cookie[0]

    if status.ok:
        return True, DNAC_Cookies
    else:
        return False, False
    
    
########################################################################

def dnac_getDevices(BASE_URL, DNAC_Auth, DNAC_Cookies):
    #api = "/network-device"
    FULL_URL = "https://"+BASE_URL+"/api/v1/network-device"
    print (FULL_URL)
    headers = {
                "Authorization": DNAC_Auth,
                'Content-Type': 'application/json'    
            }

    cookie={
                'X-JWT-ACCESS-TOKEN': DNAC_Cookies

            }
    response = requests.get(FULL_URL, headers=headers, verify=False, cookies=cookie,timeout=5.0).json()

    num = 1
    description_item=[]
    line_item=[]
    print (response)
    #print (response["response"])
    #for i in response["response"]:
    for i in response["response"]:
        '''
        if i["errorCode"] == 'null' or i["errorCode"] is None:
            dev_status="Ok"
        else:
            dev_status="Not ok"
        '''
        if ".com" in i["hostname"]:
            new_hostname = i["hostname"].replace(".com", "")
        else:
            new_hostname=i["hostname"]

        #line_item.append(str(num)+". **"+i["hostname"]+"** - "+i["platformId"]+" - "+dev_status)
        #line_item={str(num)+". **"+i["hostname"]+"** - "+i["platformId"]+" - "+dev_status:str(i["id"])}
        #inside_item={i["hostname"]:i["id"]}
        item=str(num)+". "+new_hostname+" - "+i["platformId"]+" - "+i["role"]
        inside_item={str(num):str(i["id"])}
        
        description_item.append(item)
        line_item.append(inside_item)
        
        num = num + 1
    return description_item,line_item, num



###########################################################################


def dnac_getDetails(BASE_URL,DNAC_Auth,DNAC_Cookies,id):
    #api = "/network-device"

    FULL_URL = "https://"+BASE_URL+"/api/v1/network-device/"+id
    headers = {
            "Authorization": DNAC_Auth,
            'content-type': 'application/json'
            }
    cookie={
                'X-JWT-ACCESS-TOKEN': DNAC_Cookies

            }
    result = requests.get(FULL_URL, headers=headers,cookies=cookie, verify=False).json()
    #print (json.dumps(response, indent = 4, separators = (",",":")))
    #print (response)
   
    if "response" in result:
        config=json.dumps(result["response"], indent = 4, separators = (",",":"))
        return config
        
    else:
        return "Device Details Not Available"
    #config=repr(response["response"]) --> this will print \n in a given string
    
    #print (config)

###########################################################################


def dnac_getUsers(BASE_URL,DNAC_Auth,DNAC_Cookies):
    #api = "/network-device"

    FULL_URL = "https://"+BASE_URL+"/api/v1/host"
    headers = {
            "Authorization": DNAC_Auth,
            'content-type': 'application/json'
            }
    cookie={
                'X-JWT-ACCESS-TOKEN': DNAC_Cookies

            }
    result = requests.get(FULL_URL, headers=headers,cookies=cookie, verify=False).json()
    #print (json.dumps(response, indent = 4, separators = (",",":")))
    #print (response)
    
    line_item=[]
    num=1
    for i in result["response"]:
        line_item.append(str(num)+". Host IP: "+ i["hostIp"]+"\n")
        line_item.append("Host Mac: "+ i["hostMac"]+"\n")
        line_item.append("Connection Type: "+ i["hostType"]+"\n")
        line_item.append("Connected Device: "+ i["connectedNetworkDeviceName"]+"\n")
        line_item.append("Connected Interface: "+ i["connectedInterfaceName"]+"\n")
        line_item.append("\n\n")
        num = num+1

    return line_item


###########################################################################

'''
def apic_em_getConfig(BASE_URL,ticket,id):
    #api = "/network-device"

    FULL_URL = "https://"+BASE_URL+"/network-device/"+id+"/config"
    headers = {"Content-Type":"application/json", "X-Auth-Token": ticket}
    result = requests.get(FULL_URL, headers=headers, verify=False).json()
    #print (json.dumps(response, indent = 4, separators = (",",":")))
    #print (response)
   
    if "response" in result:
        config=(result["response"].replace("\n!","\n"))
        #config=json.dumps(config, indent = 0, separators = ("\n","\n"))
        return config
        
    else:
        return "Configration Not Available"
        
    #config=repr(response["response"]) --> this will print \n in a given string
    
    #print (config)
'''
    