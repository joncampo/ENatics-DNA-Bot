#!/usr/bin/env python

import requests
import os
import sys
import json
import base64
'''
#################################################################################################################################################################
ENatics is a beta project about Software Defined Networking, and created by Jon Warner Campo. For any issues or concerns, you may email him at joncampo@cisco.com.
See Terms of Service - https://arcane-spire-45844.herokuapp.com/terms
See Privacy Policy - https://arcane-spire-45844.herokuapp.com/privacy
#################################################################################################################################################################
'''
def get_settings():

    #################replace XXX with APIC-EM URL, Username and Password
    APIC_EM_BASE_URL = 'XXX' ####ex. 'sandboxapic.cisco.com/api/v1'
    APIC_EM_USER = 'XXX'
    APIC_EM_PASS = 'XXX'

    #################replace XXX with CMX URL, Username and Password
    CMX_BASE_URL = 'XXX'   ###ex. 'cmxlocationsandbox.cisco.com'
    CMX_User = 'XXX'
    CMX_Pass = 'XXX'

    CMX_Auth=base_64_encoder(CMX_User,CMX_Pass)

    #################Meraki URL and Profile API token
    MERAKI_BASE_URL = 'dashboard.meraki.com'
    MERAKI_TOKEN='XXX'
    
    #################CSR1kv URL, Netconf port, Username and Password
    CSR1KV_URL='XXX'
    NETCONF_PORT=10000
    NETCONF_USER = 'XXX'
    NETCONF_PASS = 'XXX'

    #################Google Token
    GOOGLE_TOKEN='XXX'

    #################DNAC_BASE_URL
    DNAC_BASE_URL='XXX' ####ex. "sandboxdnac.cisco.com"
    DNAC_USER='XXX'
    DNAC_PASS='XXX'


    DNAC_Auth=base_64_encoder(DNAC_USER,DNAC_PASS)
    
    #################Prime Infrastructure
    PRIME_BASE_URL='XXX' ###ex. "primeinfrasandbox.cisco.com"
    PRIME_USER='XXX'
    PRIME_PASS='XXX'


    PRIME_Auth=base_64_encoder(PRIME_USER,PRIME_PASS)

    #################IOT
    IOT_Token='XXX'
    GOOGLE_MAP_KEY='XXX'

    #################FB URL, BOT Token, FB Verify Password
    FB_BASE_URL="graph.facebook.com/v2.6"
    FB_BOT_TOKEN='XXX'
    FB_BOT_VERIFY_PASS='XXX'
    FB_WEBHOOK_URL="https://XXX/facebook"

    #################Cisco Spark URL and BOT Token
    SPARK_BASE_URL="https://api.ciscospark.com/v1"
    SPARK_BOT_TOKEN='XXX'
    SPARK_WEBHOOK_URL="https://XXX/spark"
    SPARK_BOT_EMAIL='XXX'
    SPARK_BOT_NAME='XXX'
    #################SLACK BOT Token
    SLACK_BOT_TOKEN='XXX'
    SLACK_WEBHOOK_SECRET = 'XXX'
    SLACK_BASE_URL="https://slack.com/api"
    SLACK_BOT_USERNAME='XXX'


    return APIC_EM_BASE_URL, APIC_EM_USER, APIC_EM_PASS, CMX_BASE_URL, CMX_Auth, MERAKI_BASE_URL, MERAKI_TOKEN, CSR1KV_URL, NETCONF_PORT, NETCONF_USER, NETCONF_PASS, GOOGLE_TOKEN, DNAC_BASE_URL, DNAC_Auth,PRIME_BASE_URL,PRIME_Auth, FB_BASE_URL, FB_BOT_TOKEN, FB_BOT_VERIFY_PASS,FB_WEBHOOK_URL, SPARK_BASE_URL, SPARK_BOT_TOKEN, SPARK_WEBHOOK_URL,SPARK_BOT_EMAIL, SPARK_BOT_NAME, SLACK_BOT_TOKEN,SLACK_WEBHOOK_SECRET,SLACK_BASE_URL,SLACK_BOT_USERNAME,IOT_Token,GOOGLE_MAP_KEY

def base_64_encoder(username,password):
    raw_encoded = base64.b64encode(bytes(username+":"+password,'utf-8'))
    encoded=raw_encoded.decode("utf-8")
    basic_encoded = 'Basic '+encoded
    return basic_encoded
