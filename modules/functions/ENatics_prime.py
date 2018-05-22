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

def prime_getAlarmSummary(BASE_URL,PRIME_AUTH,ALARM_TYPE):

    FULL_URL = 'https://'+BASE_URL+'/webacs/api/v1/data/Alarms.json?.full=true&severity='+ALARM_TYPE



    headers = {
                'Authorization': PRIME_AUTH
            }


    response = requests.get(FULL_URL, headers=headers, verify=False, timeout=5.0).json()
    alarm_list=response['queryResponse']['entity']
    #print (response)
    #alarm_number=response['queryResponse']['@count']
    #description_item=[]
    line_item=[]
    for i in alarm_list:
        item4=i['alarmsDTO']['category']['value']
        line_item.append(item4)
    ###returns alarm source type of alarms
    return line_item



def prime_getAlarm(BASE_URL,PRIME_AUTH,ALARM_TYPE):

    FULL_URL = 'https://'+BASE_URL+'/webacs/api/v1/data/Alarms.json?.full=true&severity='+ALARM_TYPE+'&.maxResults=5'

    headers = {
                'Authorization': PRIME_AUTH
            }

    response = requests.get(FULL_URL, headers=headers, verify=False, timeout=5.0).json()
    alarm_list=response['queryResponse']['entity']
    
    #num = 1
    description_item=[]
    line_item=[]
    for i in alarm_list:
        item1="Alarm ID: "+i['alarmsDTO']['@id']+"\n\n"
        item2="Alarm Name: "+i['alarmsDTO']['condition']['value']+"\n\n"
        item3="Alarm Date&Time: "+i['alarmsDTO']['alarmFoundAt']+"\n\n"
        item4="Alarm Source Type: "+i['alarmsDTO']['category']['value']+"\n\n"
        item5="Alarm Device Source: "+i['alarmsDTO']['source']+"\n\n"
        item6="Alarm Message: "+i['alarmsDTO']['message']+"\n\n"
        line_item.append(item1+item2+item3+item4+item5+item6)
        #num = num + 1

    return line_item
