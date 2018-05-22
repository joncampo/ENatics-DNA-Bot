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

def fb_connector(global_command, FB_BASE_URL,FB_BOT_TOKEN,FB_BOT_VERIFY_PASS,request):
    if request.method == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            #if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            if not request.args.get("hub.verify_token") == FB_BOT_VERIFY_PASS:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200

        return "Hello world", 200

    elif request.method == 'POST':
        data = request.get_json()
        #print(data) # you may not want to log every incoming message in production, but it's good for testing
        print (data)
        if data["object"] == "page":
            
            for entry in data["entry"]:
                page_id=entry["id"]
                for messaging_event in entry["messaging"]:
                    
                    if messaging_event.get("message"):  # someone sent us a message
                        msg=[None,None]
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text

                        if sender_id != page_id:
                            msg = global_command.handle_text(chat="facebook",senders_id=sender_id,cmd=message_text,token=FB_BOT_TOKEN, room_id=None)
                            
                            if msg[0] != None:
                                send_message(FB_BOT_TOKEN,sender_id, msg[0])
                        else:
                            pass
            
        return "ok", 200

#####################FB send text message
def send_message(FB_BOT_TOKEN, recipient_id, message_text):

    params = {
        "access_token": FB_BOT_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
            "quick_replies":[
              {
                "content_type":"text",
                "title":"list fabric",
                "payload":"list fabric"
              },
              {
                "content_type":"text",
                "title":"fabric users",
                "payload":"fabric users"
              },
		      {
		        "content_type":"text",
		        "title":"list devices",
		        "payload":"list devices"
		      },
			  {
		        "content_type":"text",
		        "title":"list clients",
		        "payload":"list clients"
		      },
			  {
		        "content_type":"text",
		        "title":"list floors",
		        "payload":"list floors"
		      },
			  {
		        "content_type":"text",
		        "title":"list meraki",
		        "payload":"list meraki"
		      },
              {
                "content_type":"text",
                "title":"list iot",
                "payload":"list iot"
              },    	  
              {
                "content_type":"text",
                "title":"list alarms",
                "payload":"list alarms"
              },                   
			  {
		        "content_type":"text",
		        "title":"troubleshoot interface",
		        "payload":"troubleshoot interface"
		      },
		      {
		        "content_type":"text",
		        "title":"about",
		        "payload":"about"
		      },
		      {
		        "content_type":"text",
		        "title":"help",
		        "payload":"help"
		      }	  	  
		    ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

#####################FB send media message

def send_media(FB_BOT_TOKEN,imagepath):
    
    address=''.join(('https://graph.facebook.com/v2.6/me/message_attachments?access_token=', FB_BOT_TOKEN))
    data = {'message': '{"attachment":{"type":"image", "payload":{"is_reusable":"true"}}}'}

    files = { "filedata" : (imagepath, open(imagepath, 'rb'), 'image/png') }

    r = requests.post(address, data=data,files=files).json()
    attach_id=r['attachment_id']
    print ("Attachment ID is: ",attach_id)
    return attach_id

def send_attachment_id(FB_BOT_TOKEN,recipient_id, attach_id):

    params = {
        "access_token": FB_BOT_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
                "attachment":{
                    "type":"image", 
                    "payload":{
                        "attachment_id": attach_id
                    }
                }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    print (r)