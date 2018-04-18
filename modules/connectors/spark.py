#!/usr/bin/python3
'''
#################################################################################################################################################################
ENatics is a beta project about Software Defined Networking, and created by Jon Warner Campo. For any issues or concerns, you may email him at joncampo@cisco.com.
See Terms of Service - https://arcane-spire-45844.herokuapp.com/terms
See Privacy Policy - https://arcane-spire-45844.herokuapp.com/privacy
#################################################################################################################################################################
'''
# Import necessary modules
from pprint import pprint
import requests
import json
import sys
import subprocess
import platform
import zipfile
import logging
import time
import os
import argparse
from shutil import copyfile
from requests_toolbelt.multipart.encoder import MultipartEncoder
from PIL import Image
from ncclient import manager
import xml.dom.minidom

###################Connector

def spark_connector(global_command, SPARK_BASE_URL,SPARK_BOT_TOKEN,SPARK_BOT_EMAIL,SPARK_BOT_NAME, request,spark_authorized_users):

    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        resource = webhook['resource']
        senders_email = webhook['data']['personEmail']
        room_id = webhook['data']['roomId']

        print (webhook)

        msg = None
        content_file = None
        if senders_email != SPARK_BOT_EMAIL:

            match=0
            for i in spark_authorized_users:
                if senders_email == i.lower() or "any" == i.lower():
                    match=1
                    print('Success')
                    break

            if match == 1:

                result = send_spark_get(SPARK_BOT_TOKEN,'messages/{0}'.format(webhook['data']['id']))  ###gets message content based on data id of webhook data

                in_message = result["text"]

                raw_msg = global_command.handle_text(chat="spark",senders_id=senders_email,cmd=in_message,token=SPARK_BOT_TOKEN, room_id=room_id)
                ending_next="\n\n*Type **help** to see what's next!*"
                msg=raw_msg[0]
                content_file=raw_msg[1]

                if msg != None:
                    spark_send_message(SPARK_BOT_TOKEN, room_id, msg+ending_next,content_file)
                    return "true"

        return True

    elif request.method == 'GET':
        message = "<center><img src=\"http://bit.ly/SparkBot-512x512\" alt=\"Spark Bot\" style=\"width:256; height:256;\"</center>" \
        "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
        "<center><b><i>Please don't forget to create Webhooks to start receiving events from Cisco Spark!</i></b></center>" % SPARK_BOT_NAME
        return message, 200


#####################Spark Header and API
def _spark_api(noun):

    return ''.join(('https://api.ciscospark.com/v1/', noun))
    
def _headers(bot_token):
    return {'Content-type': 'application/json',
            'Authorization': 'Bearer ' + bot_token}

def spark_send_message(token, room_id, msg,content_file=None):

    m = MultipartEncoder({'roomId': room_id,
                        'markdown': msg,
                        'files':content_file})

    r = requests.post(_spark_api('messages'), 
        data=m,
        headers={'Authorization': 'Bearer ' + token,
        'Content-Type': m.content_type})

    return r.ok

#####################Webhook Function
def spark_webhook(bot_token, SPARK_WEBHOOK_URL):

    m = { "name":'ENatics', "targetUrl":SPARK_WEBHOOK_URL, "resource":"all", "event":"all"}
    
    r = requests.post(_spark_api('webhooks'), json=m, headers=_headers(bot_token))
    return r.ok


#######################Spark Get

def send_spark_get(SPARK_BOT_TOKEN, end_url, payload=None, js=True):

  if payload == None:
    request = requests.get(_spark_api(end_url), headers=_headers(SPARK_BOT_TOKEN))
  else:
    request = requests.get(_spark_api(end_url), headers=_headers(SPARK_BOT_TOKEN), params=payload)
  if js == True:
    request = request.json()

  return request