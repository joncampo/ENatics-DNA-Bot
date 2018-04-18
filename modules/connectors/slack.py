#!/usr/bin/python3
'''
#################################################################################################################################################################
ENatics is a beta project about Software Defined Networking, and created by Jon Warner Campo. For any issues or concerns, you may email him at joncampo@cisco.com.
See Terms of Service - https://arcane-spire-45844.herokuapp.com/terms
See Privacy Policy - https://arcane-spire-45844.herokuapp.com/privacy
#################################################################################################################################################################
'''
# Import necessary modules
import requests
import os
from slackclient import SlackClient
from flask import Flask, request, Response
from requests_toolbelt.multipart.encoder import MultipartEncoder

#slack_client = SlackClient(SLACK_BOT_TOKEN)



def slack_connector(global_command, SLACK_BASE_URL, SLACK_BOT_TOKEN, SLACK_WEBHOOK_SECRET,SLACK_BOT_USERNAME,slack_client, request,slack_authorized_users):

    if request.method == 'POST':
        if request.form.get('token') == SLACK_WEBHOOK_SECRET:
            sender_username = request.form.get('user_name')
            #sender_id = request.form.get('user_id')
            channel_ID=request.form.get('channel_id')
            message_text = request.form.get('text')

            msg = None

            if sender_username != 'slackbot' and sender_username != SLACK_BOT_USERNAME:
                
                match=0
                for i in slack_authorized_users:
                    if sender_username == i.lower() or "any" == i.lower():
                        match=1
                        print('Success')
                        break

                if match == 1:

                    msg = global_command.handle_text(chat="slack",senders_id=slack_client,cmd=message_text,token=SLACK_BOT_TOKEN, room_id=channel_ID)

                    if msg[0] != None:
                        slack_send_message(slack_client,channel_ID, msg[0])

        #return Response(), 200
        return True



#####################Splack send message

def slack_send_message(slack_client,channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        #username='pythonbot',
        #icon_emoji=':robot_face:'
    )
    return True

def slack_send_media(SLACK_BOT_TOKEN,channel_id,content_file):

    URL="https://slack.com/api/files.upload"
    m = MultipartEncoder({'channels': channel_id,
                        'token': SLACK_BOT_TOKEN,
                        'file': content_file})

    r = requests.post(URL, 
        data=m,headers={'Content-Type': m.content_type})
