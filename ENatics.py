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
from flask import Flask, request, render_template, url_for
from slackclient import SlackClient

#####################Connector
from modules.connectors.spark import spark_connector,send_spark_get,spark_webhook, spark_send_message
from modules.connectors.facebook import fb_connector,send_message,send_media, send_attachment_id
from modules.connectors.slack import slack_connector,slack_send_message,slack_send_media
#####################APIC-EM
from modules.functions.ENatics_apic_em import apic_em_getDevices, apic_em_checkStatus, apic_em_getConfig, apic_em_getDetails
#####################DNAC
from modules.functions.ENatics_dnac import dnac_checkStatus,dnac_getDetails, dnac_getDevices, dnac_getUsers
#####################CMX
from modules.functions.ENatics_cmx import cmx_map_download, cmx_list_client, cmx_client_info, cmx_list_floors, cmx_collect_client, cmx_collect_zones, cmx_edit_map, get_floor_id
#####################meraki
from modules.functions.ENatics_meraki import meraki_org, meraki_network, meraki_network_devices, meraki_network_ssid
#####################netconf
from modules.functions.ENatics_netconf import netconf_get_interface
#####################google
from modules.functions.ENatics_google import googling

#####################Settings

from credentials.settings import get_settings
settings=get_settings()
APIC_EM_BASE_URL = settings[0]
APIC_EM_USER = settings[1]
APIC_EM_PASS = settings[2]
CMX_BASE_URL = settings[3]
CMX_Auth = settings[4]
MERAKI_BASE_URL = settings[5]
MERAKI_TOKEN = settings[6]
CSR1KV_URL = settings[7]
NETCONF_PORT = settings[8]
NETCONF_USER = settings[9]
NETCONF_PASS = settings[10]
GOOGLE_TOKEN = settings[11]
DNAC_BASE_URL = settings[12]
DNAC_Auth = settings[13]
FB_BASE_URL = settings[14]
FB_BOT_TOKEN = settings[15]
FB_BOT_VERIFY_PASS = settings[16]
FB_WEBHOOK_URL = settings[17]
SPARK_BASE_URL = settings[18]
SPARK_BOT_TOKEN = settings[19]
SPARK_WEBHOOK_URL=settings[20]
SPARK_BOT_EMAIL=settings[21]
SPARK_BOT_NAME=settings[22]
SLACK_BOT_TOKEN = settings[23]
SLACK_WEBHOOK_SECRET=settings[24]
SLACK_BASE_URL=settings[25]
SLACK_BOT_USERNAME=settings[26]

#################Check Authorized Users

spark_authorized_users=open('credentials/spark_email.txt').read().split('\n')
if "###" in spark_authorized_users[0]:
	del spark_authorized_users[0]

slack_authorized_users=open('credentials/slack_username.txt').read().split('\n')
if "###" in slack_authorized_users[0]:
	del slack_authorized_users[0]

###############Slack Client
slack_client = SlackClient(SLACK_BOT_TOKEN)

#####################Business Logic
class global_command():
	def handle_text(chat,senders_id,cmd,token=None, room_id=None):
		result = None
		content_file=None
		cmd=cmd.lower()
		

		if 'hi' in cmd:
			#result="Hi <@personEmail:"+senders_email+">"
			result="Hi"
		elif 'hello' in cmd:
			#result="Hello <@personEmail:"+senders_email+">"
			result="Hello"
		
		elif 'thank' in cmd:
			result="Your Welcome!"

		elif 'help' in cmd:
			result="Please see list of commands below:\n\n\n" \
			"\"list fabric\" - shows SDA fabric devices managed by DNA Center and has option for device details and fabric users\n\n" \
			"\"list devices\" - shows devices managed by APIC-EM and has options for device config and details\n\n" \
			"\"list clients\" - shows active clients and option for location of clients on map managed by CMX Location Analytics\n\n" \
			"\"list floors\" - shows all the floors managed by CMX Location Analytics and has 2 options: location of all the users in each floor and zones (restroom)\n\n" \
			"\"list meraki\" - shows meraki networks and has 2 options: devices inside a network and SSIDs\n\n" \
			"\"netconf interface - shows the netconf yang model of a cisco interface\n\n" \
			"\"google <Cisco search item>\" - ENatics will search the Cisco.com site for links and references of search item\n\n" \
			"\"about\" - information about the ENatics Bot\n\n"
			if chat == "spark":
				content_file=('temp/enatics.png', open('temp/enatics.png', 'rb'),'image/png')
			elif chat == "facebook": 
				send_to_page=send_attachment_id(FB_BOT_TOKEN,senders_id, '157994951529488')
			elif chat == "slack":
				content_file=('temp/enatics.png', open('temp/enatics.png', 'rb'),'image/png')
				slack_send_media(token,room_id,content_file)


		elif 'about' in cmd:
			result="Hello I'm ENatics! I'm here to help you manage your network easily by tapping the full potential of all the APIs inside your network! I'm currently on version 1 \n\nI'm created by Jon Warner Campo of Cisco GVE and you can reach him at joncampo@cisco.com. Your feedback is most welcome. \n\nThank you and I hope you appreciate my service! "\
			"See Terms of Service - https://arcane-spire-45844.herokuapp.com/terms\n"\
			"See Privacy Policy - https://arcane-spire-45844.herokuapp.com/privacy"


		elif 'list fabric' in cmd:
			
			if chat == "spark":
				spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
			elif chat == "facebook":
				send_message(FB_BOT_TOKEN, senders_id, "Got it! Please wait...")
			elif chat == "slack":
				slack_send_message(senders_id,room_id, "Got it! Please wait...")

			dnac_status=dnac_checkStatus(DNAC_BASE_URL,DNAC_Auth)
			
			if dnac_status[0] is True:
				global_command.DNAC_Cookies=dnac_status[1]
				global_command.dnac_raw_result=dnac_getDevices(DNAC_BASE_URL,DNAC_Auth,global_command.DNAC_Cookies)
				welcome_text="Hi Please see your requested Network Status Summary\n\n Hostname - Model- SDA Fabric Role:\n"
				ending_text="\n\n\nType \"fabric #\" to get fabric device details (ex. fabric 1)"
				result=welcome_text+"\n".join(str(x) for x in global_command.dnac_raw_result[0])+ending_text

			else:
				result="\n\nFailed to Connect to DNA Center \n\n"
		
		elif 'fabric users' in cmd:

			if chat == "spark":
				spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
			elif chat == "facebook":
				send_message(FB_BOT_TOKEN, senders_id, "Got it! Please wait...")
			elif chat == "slack":
				slack_send_message(senders_id,room_id, "Got it! Please wait...")

			dnac_status=dnac_checkStatus(DNAC_BASE_URL,DNAC_Auth)
			
			if dnac_status[0] is True:
				DNAC_Cookies=dnac_status[1]
				dnac_user=dnac_getUsers(DNAC_BASE_URL,DNAC_Auth,DNAC_Cookies)
				welcome_text="Hi Please see SDA Fabric Users:\n\n\n"
				
				result=welcome_text+"\n".join(str(x) for x in dnac_user)

			else:
				result="\n\nFailed to Connect to DNA Center \n\n"

		elif 'fabric' in cmd:
			config_text=cmd.split()
			var_num=len(config_text)-1
			try: 
				config_num=config_text[var_num]
				place_num = int(config_num) - 1
				int(global_command.dnac_raw_result[2])
			except:
				result="\n\nError found! Please retry sending the command\n\n"
				return result,content_file

			if int(place_num) >= 0 and int(place_num) < int(global_command.dnac_raw_result[2]):

				if chat == "spark":
					spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
				elif chat == "facebook":
					send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
				elif chat == "slack":
					slack_send_message(senders_id,room_id, "Got it! Please wait...")
				device_id=global_command.dnac_raw_result[1][int(place_num)][str(config_num)]
				result=dnac_getDetails(DNAC_BASE_URL,DNAC_Auth,global_command.DNAC_Cookies,device_id)
			else:
				result="\n\nPlease choose a correct number within list\n\n"

		elif 'network status' in cmd or 'list devices' in cmd or 'list device' in cmd:
			if chat == "spark":
				spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
			elif chat == "facebook":
				send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
			elif chat == "slack":
				slack_send_message(senders_id,room_id, "Got it! Please wait...")				
			#spark_send_message(BOT_SPARK_TOKEN, room_id, "Got it <@personEmail:"+senders_email+">. Please wait.")
			ticket=apic_em_checkStatus(APIC_EM_BASE_URL,APIC_EM_USER,APIC_EM_PASS)
			
			if ticket[0]:
				global_command.apic_ticket=ticket[1]
				global_command.raw_result=apic_em_getDevices(APIC_EM_BASE_URL,global_command.apic_ticket)
				welcome_text="Hi Please see your requested Network Status Summary (hostname-model-status):\n"
				ending_text="\n\n\nType \"config #\" to get config (ex. config 1)\n\nType \"details #\" to get devices details (ex. details 1)"
				result=welcome_text+"\n".join(str(x) for x in global_command.raw_result[0])+ending_text

			else:
				result="\n\nFailed to Connect to APIC-EM \n\n"

		elif 'config' in cmd:
			config_text=cmd.split()
			var_num=len(config_text)-1

			try: 
				config_num=config_text[var_num]
				place_num = int(config_num) - 1
				int(global_command.raw_result[2])
			except:
				result="\n\nError found! Please retry sending the command\n\n"
				return result,content_file

			if int(place_num) >= 0 and int(place_num) < int(global_command.raw_result[2]):
				if chat == "spark":
					spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
				elif chat == "facebook":
					send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
				elif chat == "slack":
					slack_send_message(senders_id,room_id, "Got it! Please wait...")
				device_id=global_command.raw_result[1][int(place_num)][str(config_num)]
				config=apic_em_getConfig(APIC_EM_BASE_URL,global_command.apic_ticket,device_id)
				config_split=config.split("\n\n\n\n\n\n\n\n")
				num=0
				while num < len(config_split):
					print (config_split[num])

					if chat == "spark":
						spark_send_message(SPARK_BOT_TOKEN, room_id, config_split[num])
					elif chat == "facebook":
						send_message(FB_BOT_TOKEN,senders_id, config_split[num])
					elif chat == "slack":
						slack_send_message(senders_id,room_id, "Got it! Please wait...")
					num=num+1
				result="End of config"

			else:
				result="\n\nPlease choose a correct number within list\n\n"
		
		elif 'details' in cmd or 'detail' in cmd:
			config_text=cmd.split()
			var_num=len(config_text)-1
			try: 
				config_num=config_text[var_num]
				place_num = int(config_num) - 1
				int(global_command.raw_result[2])
			except:
				result="\n\nError found! Please retry sending the command\n\n"
				return result,content_file

			if int(place_num) >= 0 and int(place_num) < int(global_command.raw_result[2]):
				
				if chat == "spark":
					spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
				elif chat == "facebook":
					send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
				elif chat == "slack":
					slack_send_message(senders_id,room_id, "Got it! Please wait...")
				device_id=global_command.raw_result[1][int(place_num)][str(config_num)]
				result=apic_em_getDetails(APIC_EM_BASE_URL,global_command.apic_ticket,device_id)
			else:
				result="\n\nPlease choose a correct number within list\n\n"

		elif 'list clients' in cmd or 'list client' in cmd:
			try:
					FULL_URL = "https://"+CMX_BASE_URL+"/api/config/v1/maps/floor/list"
					headers = {"Authorization": CMX_Auth}
					A=requests.get(FULL_URL, headers=headers, verify=False, timeout=3)
			except:
				result="Please kindly check CMX connectivity or user/pass!"
				return result,content_file
			

			global_command.raw_cmx_list_users=cmx_list_client(CMX_BASE_URL,CMX_Auth)
			#result=cmx_list_users
			#print (raw_cmx_list_users)
			welcome_text="Hi Please see your requested Wireless Devices:\n"
			ending_text="\n\n\nType locate client # to get user location details (ex. locate client 1)"
			result=welcome_text+"\n".join(str(x) for x in global_command.raw_cmx_list_users[0])+ending_text

		elif 'list floors' in cmd or 'list floor' in cmd:
			try:
					FULL_URL = "https://"+CMX_BASE_URL+"/api/config/v1/maps/floor/list"
					headers = {"Authorization": CMX_Auth}
					A=requests.get(FULL_URL, headers=headers, verify=False, timeout=3)
			except:
				result="Please kindly check CMX connectivity or user/pass!"
				return result,content_file
			#result=cmx_list_users
			#print (raw_cmx_list_floors)
			global_command.raw_cmx_list_floors=cmx_list_floors(CMX_BASE_URL,CMX_Auth)
			welcome_text="Hi Please see your requested list of floors:\n"
			ending_text="\n\n\nType \"floor # clients\" to get location of clients in a floor (ex. floor 1 clients)\n\nType \"floor # restroom\" to get location of users in a floor"
			result=welcome_text+"\n".join(str(x) for x in global_command.raw_cmx_list_floors[0])+ending_text
		
		elif 'locate client' in cmd:
			config_text=cmd.split()
			var_num=len(config_text)-1
			config_num=config_text[var_num]

			if "client" in config_num:
				result="\n\nPlease choose a correct number within list\n\n"
				return result,content_file

			try: 
				total_users=len(global_command.raw_cmx_list_users[1])
			except:
				result="\n\nError found! Please retry sending the command\n\n"
				return result,content_file

			if int(config_num) >= 1 and int(config_num) <= total_users:
				cmx_user=global_command.raw_cmx_list_users[1][str(config_num)]
				if chat == "spark":
					spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
				elif chat == "facebook":
					send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
				#print (cmx_user)
				cmx_client_details=cmx_client_info(CMX_BASE_URL,CMX_Auth,cmx_user)

				if cmx_client_details[0] is True:
					try:

						if chat == "spark":
							content_file=('temp/map2.png', open('temp/map2.png', 'rb'),'image/png')
							result="Client "+cmx_user+"(Red Pin) is at "+cmx_client_details[1]
						elif chat == "facebook":
							content_filename="temp/map2.png"
							upload_id=send_media(FB_BOT_TOKEN,content_filename)
							send_to_page=send_attachment_id(FB_BOT_TOKEN,senders_id,upload_id)
							print ("upload successful!")
							result="Client "+cmx_user+"(Red Pin) is at "+cmx_client_details[1]
						elif chat == "slack":
							content_file=('temp/map2.png', open('temp/map2.png', 'rb'),'image/png')
							slack_send_media(token,room_id,content_file)
							result="Client "+cmx_user+"(Red Pin) is at "+cmx_client_details[1]
					
					except:
						result="Error Uploading Map"

			else:
				result="\n\nPlease choose a correct number within list\n\n"



		elif 'floor' in cmd:
			config_text=cmd.split()
			#print ("config")
			#print (config_text[1])
			var_num=len(config_text)-2
			var_num2=len(config_text)-1
			#if type(config_text[1]) == int:
			config_command=config_text[var_num2]
			config_num=config_text[var_num]
			#elif type(config_text[2]) == int:
			#	config_num=config_text[2]
			if "floor" in config_num:
				result="\n\nPlease choose a correct number within list\n\n"
				return result,content_file
			try: 
				total_users=len(global_command.raw_cmx_list_floors[1])
				if chat == "spark":
					spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
				elif chat == "facebook":
					send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
				elif chat == "slack":
					slack_send_message(senders_id,room_id, "Got it! Please wait...")					
			except:
				result="\n\nError found! Please retry sending the command\n\n"
				return result,content_file

			if "restroom" in config_command or "restrooms" in config_command:
				if int(config_num) >= 1 and int(config_num) <= total_users:
					floor=global_command.raw_cmx_list_floors[1][str(config_num)]

					floor_normalized=(floor.replace(">","/"))
					cmx_floor_clients=cmx_collect_zones(CMX_BASE_URL,CMX_Auth,floor_normalized)
					if cmx_floor_clients is True:
						
						try:
							if chat == "spark":
								content_file=('temp/map2.png', open('temp/map2.png', 'rb'),'image/png')
								result="Restroom(s) (GREEN BOX) Found!"
							elif chat == "facebook":
								content_filename="temp/map2.png"
								upload_id=send_media(FB_BOT_TOKEN,content_filename)
								send_to_page=send_attachment_id(FB_BOT_TOKEN,senders_id,upload_id)
								print ("upload successful!")
								result="Restroom(s) (GREEN BOX) Found!"
							elif chat == "slack":
								content_file=('temp/map2.png', open('temp/map2.png', 'rb'),'image/png')
								slack_send_media(token,room_id,content_file)
								result="Restroom(s) (GREEN BOX) Found!"
						except:
							result="Error Uploading Map"
						
					else:
						result="\n\nSorry No restroom in floor!\n\n"
				else:
					result="\n\nPlease choose a correct number within list\n\n"

			elif "clients" in config_command or "client" in config_command:	
				
				if int(config_num) >= 1 and int(config_num) <= len(global_command.raw_cmx_list_floors[1]):
					floor=global_command.raw_cmx_list_floors[1][str(config_num)]				
					
					if chat == "spark":
						spark_send_message(SPARK_BOT_TOKEN, room_id, "Locating clients and Downloading Map. Please wait...")
					elif chat == "facebook":
						send_message(FB_BOT_TOKEN,senders_id, "Locating clients and Downloading Map. Please wait...")
					elif chat == "slack":
						slack_send_message(senders_id,room_id, "Locating clients and Downloading Map. Please wait...")

					floor_normalized=(floor.replace(">","/"))
					floor_id=get_floor_id(CMX_BASE_URL,CMX_Auth,floor_normalized)

					if floor_id[0] is True:
						print ("processing ",floor_id[1])
						cmx_floor_clients=cmx_collect_client(CMX_BASE_URL,CMX_Auth,floor_id[1])

						if cmx_floor_clients[0] is True:
							print("editing maps")
							users_x=cmx_floor_clients[1]
							users_y=cmx_floor_clients[2]
							total=len(users_x)
							#print (len(users_x),"user(s) detected!")
							if chat == "spark":
								spark_send_message(SPARK_BOT_TOKEN, room_id, "Processing "+str(total)+" clients on map! Please wait...")
							elif chat == "facebook":
								send_message(FB_BOT_TOKEN,senders_id, "Processing "+str(total)+" clients on map! Please wait...")
							elif chat == "slack":
								slack_send_message(senders_id,room_id, "Processing "+str(total)+" clients on map! Please wait...")
							
							cmx_edit=cmx_edit_map(users_x,users_y,bundle=1)
							print ("Uploading file")
							
							try:
								if chat == "spark":
									content_file=('temp/map2.png', open('temp/map2.png', 'rb'),'image/png')
									result=str(total)+" Active Clients (Red Pin) found on \n\n"+floor
								elif chat == "facebook":
									content_filename="temp/map2.png"
									upload_id=send_media(FB_BOT_TOKEN,content_filename)
									send_to_page=send_attachment_id(FB_BOT_TOKEN,senders_id,upload_id)
									print ("upload successful!")
									result=str(total)+" Active Clients (Red Pin) found on \n\n"+floor
								elif chat == "slack":
									content_file=('temp/map2.png', open('temp/map2.png', 'rb'),'image/png')
									slack_send_media(token,room_id,content_file)
									result=str(total)+" Active Clients (Red Pin) found on \n\n"+floor

							except:
								result="Error Uploading Map"
									
						else:
							result="\n\nSorry No clients found!\n\n"
					else:
						result="\n\nError on Maps!\n\n"
				else:
					result="\n\nPlease choose a correct number within list\n\n"


		elif 'list meraki network' in cmd or 'list meraki networks' in cmd or 'list meraki' in cmd:
			try:
				mrki_org=meraki_org(MERAKI_BASE_URL,MERAKI_TOKEN)
			except:
				result="Please check your Meraki token"
				return result,content_file

			mrki_org_id=str(mrki_org[0])
			mrki_org_name=mrki_org[1]
			print (mrki_org_id)
			global_command.raw_mrki_ntw=meraki_network(MERAKI_BASE_URL,MERAKI_TOKEN,mrki_org_id)
			welcome_text="Hi please see list of Meraki Network(s) under Organization **"+mrki_org_name+"**:\n"
			ending_text1="\n\nType \"meraki # devices\" to get list of Meraki Devices under chosen network. (ex. meraki 1 devices)"
			ending_text2="\n\nType \"meraki # ssid\" to get list of SSIDs under chosen network. (ex. meraki 1 ssid)"
			result=welcome_text+"\n".join(str(x) for x in global_command.raw_mrki_ntw[0])+ending_text1+ending_text2

		elif 'meraki' in cmd:
			config_text=cmd.split()
			#print ("config")
			#print (config_text[1])
			var_num1=len(config_text)-1
			config_command=config_text[var_num1]

			var_num2=len(config_text)-2
			config_num=config_text[var_num2]

			if "meraki" in config_num:
				result="\n\nPlease choose a correct number within list\n\n"
				return result,content_file

			try: 
				total_users=len(global_command.raw_mrki_ntw[1])
			except:
				result="\n\nError found! Please retry sending the command\n\n"
				return result,content_file

			if "device" in config_command or "devices" in config_command:
				if int(config_num) >= 1 and int(config_num) <= total_users:
					if chat == "spark":
						spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
					elif chat == "facebook":
						send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
					meraki_network_id_chosen=global_command.raw_mrki_ntw[1][config_num]
					welcome_text="Please see list of Meraki Devices under Network ID **"+meraki_network_id_chosen+"**:\n\n"
					result=welcome_text+meraki_network_devices(MERAKI_BASE_URL,MERAKI_TOKEN,meraki_network_id_chosen)
				else:
					result="\n\nPlease choose a correct number within list\n\n"
			
			elif "ssid" in config_command or "ssids" in config_command:
				if int(config_num) >= 1 and int(config_num) <= total_users:
					if chat == "spark":
						spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
					elif chat == "facebook":
						send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
					meraki_network_id_chosen=global_command.raw_mrki_ntw[1][config_num]
					result="End of SSID List"
					config=meraki_network_ssid(MERAKI_BASE_URL,MERAKI_TOKEN,meraki_network_id_chosen)
				
					config_split=config.split("number")
					num=0
					while num < len(config_split):
						print (config_split[num])

						if chat == "spark":
							spark_send_message(SPARK_BOT_TOKEN, room_id, config_split[num])
						elif chat == "facebook":
							send_message(FB_BOT_TOKEN,senders_id, config_split[num])
						num=num+1
					result="End of config"


				else:
					result="\n\nPlease choose a correct number within list\n\n"
					
		elif 'netconf interface' in cmd or 'yang interface' in cmd:

			if chat == "spark":
				spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
			elif chat == "facebook":
				send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
			elif chat == "slack":
				slack_send_message(senders_id,room_id, "Got it! Please wait...")				
			netconf_result_raw=netconf_get_interface(CSR1KV_URL, NETCONF_PORT, NETCONF_USER, NETCONF_PASS)
			netconf_result=(xml.dom.minidom.parseString(netconf_result_raw.xml).toprettyxml())

			netconf_result_split=netconf_result.split("</interface>")
			num=0
			while num < len(netconf_result_split):
				print (netconf_result_split[num])
				
				if chat == "spark":
					spark_send_message(SPARK_BOT_TOKEN, room_id, netconf_result_split[num])
				elif chat == "facebook":
					send_message(FB_BOT_TOKEN,senders_id, netconf_result_split[num])
				num=num+1

			result="End of config"


		elif 'reference' in cmd or 'google' in cmd:
			if chat == "spark":
				spark_send_message(SPARK_BOT_TOKEN, room_id, "Got it <@personEmail:"+senders_id+">. Please wait.")
			elif chat == "facebook":
				send_message(FB_BOT_TOKEN,senders_id, "Got it! Please wait...")
			elif chat == "slack":
				slack_send_message(senders_id,room_id, "Got it! Please wait...")				
			config_text=cmd.split()
			del config_text[0]
			if config_text is None:
				result="Please provide a search term! ex. google catalyst 9000"
				return result,content_file
			else:
				search_string=" ".join(config_text)
			
			google_result=googling(GOOGLE_TOKEN,search_string)
			print(google_result)

			if chat == "spark":
				spark_send_message(SPARK_BOT_TOKEN, room_id, "Hi Please see your requested references for "+search_string)
			elif chat == "facebook":
				send_message(FB_BOT_TOKEN,senders_id, "Hi Please see your requested references for "+search_string)


			total_result=len(google_result)
			num=0
			while num < total_result:

				if chat == "spark":
					spark_send_message(SPARK_BOT_TOKEN, room_id, google_result[num])
				elif chat == "facebook":
					send_message(FB_BOT_TOKEN,senders_id, google_result[num])

				num=num+1

			result="End of result!\n\n To search more, just type google \"cisco search item\" (ex. google Catalyst 9000)"


		if result == None:
			result = "I did not understand your request. Please type *help* to see what I can do"

		return result, content_file

#####################Flask for Webhook
app = Flask(__name__)
@app.route('/', methods=['GET'])
def webhook():
	message = "<center><img src=\"http://bit.ly/SparkBot-512x512\" alt=\"Spark Bot\" style=\"width:256; height:256;\"</center>" \
	"<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
	"<center><b><i>Please don't forget to create Webhooks to start receiving events from Cisco Spark!</i></b></center>" % SPARK_BOT_NAME

	return message, 200

@app.route('/facebook', methods=['GET', 'POST'])
def facebookconnector():

	#print (request)
	if FB_BASE_URL != "XXX" and FB_BOT_TOKEN != "XXX" and FB_BOT_VERIFY_PASS != "XXX":
		message=fb_connector(global_command, FB_BASE_URL,FB_BOT_TOKEN,FB_BOT_VERIFY_PASS,request)
	else:
		print ("Please check FB URL, FB Bot Token or FB Bot Verify pass!")
		message=False

	return message

@app.route('/spark', methods=['GET', 'POST'])
def sparkconnector():

	if SPARK_BASE_URL != "XXX" and SPARK_BOT_TOKEN != "XXX" and SPARK_BOT_EMAIL != "XXX" and SPARK_BOT_NAME != "XXX":
		message=spark_connector(global_command, SPARK_BASE_URL, SPARK_BOT_TOKEN, SPARK_BOT_EMAIL, SPARK_BOT_NAME, request,spark_authorized_users)
	else:
		print ("Please check Spark settings and credentials!")
		message=False

	return message

@app.route('/slack', methods=['GET', 'POST'])
def slackconnector():

	if SLACK_BASE_URL != "XXX" and SLACK_BOT_TOKEN != "XXX" and SLACK_WEBHOOK_SECRET != "XXX" and SLACK_BOT_USERNAME != "XXX":
		message=slack_connector(global_command, SLACK_BASE_URL, SLACK_BOT_TOKEN, SLACK_WEBHOOK_SECRET,SLACK_BOT_USERNAME,slack_client, request, slack_authorized_users)
	else:
		print ("Please check Slack settings and credentials!")
		message=False

	return message

#####################Legal
@app.route('/terms', methods=['GET'])
def terms():
	terms_service = open('legal/terms_and_conditions.txt', 'r') 
	terms=terms_service.read() 
	print ("Terms of Service")
	message = "<html>%s</html>" % terms

	return message, 200

@app.route('/privacy', methods=['GET'])
def privacy():
	privacy_policy = open('legal/privacy.txt', 'r') 
	privacy_pol=privacy_policy.read() 
	print ("privacy_pol")
	message = "<html>%s</html>" % privacy_pol

	return message, 200


#####################Main Function

def main():
	app.run(debug=True)

#####################Main
if __name__ == "__main__":
	
	#if SPARK_BOT_TOKEN != "XXX":
		#if spark_webhook(SPARK_BOT_TOKEN, SPARK_WEBHOOK_URL):
			#print("Webhook Success!")
	
	main()
