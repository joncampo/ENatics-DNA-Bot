# ENatics-DNA-Bot
ENatics All-in-One DNA Bot

[Hi I'm ENatics! Your All-In-One EN DNA Bot! -> ENatics Presentation and Demo Video](https://youtu.be/lZmXtx_qcds)

![alt tag](images/main.png)

Table of Contents
=================

   * [ENatics](#enatics)
   * [Table of Contents](#table-of-contents)
      * [Features](#features)
      * [Quick Usage](#quick-usage)
      * [Installation Guide](#installation-guide)
    * [Demo](#demo)

Created by [https://github.com/joncampo]

## Features
![alt tag](images/what_is_enatics_arch.png)

## Quick Usage

![alt tag](images/how_to_use.png)

## Installation Guide

Installation Guide for Cloud Based ENatics Bot

A.	Preparation
1.	Download or clone ENatics from Github on your desktop- https://github.com/joncampo/ENatics-DNA-Bot.git<br />
2.	From your desktop, install Heroku Tools - https://toolbelt.heroku.com/<br />
3.	Login to Heroku – heroku login<br />
4.	Create Heroku App - heroku create<br />
5.	Get the Heroku URL via this command – heroku open<br />

B.	Credentials<br />
1.	Create Bots in chat platforms:<br />
•	Spark<br />
a)	Create bot - https://developer.ciscospark.com/apps.html<br />
b)	Get the token<br />
•	Facebook<br />

a)	Create FB bot page - https://www.facebook.com/pages/create/<br />
b)	Create App - https://developers.facebook.com/apps/<br />
c)	Inside the app, go to messenger to subscribe to created FB bot page in Step A and get the token<br />
d)	Inside the app, go to webhook and enter the Heroku URL from Step A/4. Create and get the verify token.<br />
2.	Gather device IP/URL and username/password for any of the following:<br />
•	DNA Center<br />
•	APIC-EM<br />
•	CMX<br />
3.	Enter the Heroku App name, Bot tokens, device URL/IP and username/password on settings.py file in credentials folder.
4.	Important For Security! 
Perform the following:
•	Spark – edit spark_email.txt found in credentials folder. Replace any with authorized user Spark Email Accounts<br />
•	Facebook – Do not publish the FB Bot page. Add as admins the authorized user FB accounts<br />
•	Slack -  edit slack_username.txt found in credentials folder. Enter the authorized Slack user names.<br />
C.	Deploy<br />
1.	Secure connectivity options between Heroku Cloud and On-premises devices:<br />
a.	Perform port forwarding and allow https in Firewall between DNA platforms and Heroku public IPs<br />
b.	For paid Heroku deployment, establish SSL between Heroku cloud and customer network - https://devcenter.heroku.com/articles/ssl<br />

2.	Perform the following commands to deploy ENatics to Heroku cloud.<br />
a. git add . <br />
b. git commit -m "Update" <br />
c. git push heroku master<br />



## Demo

Message me on the following to see me work!<br />
Facebook - https://www.facebook.com/ENaticsBot <br />
Cisco Spark - ENatics@sparkbot.io  <br />

Please See Presentation and Demo Video!
[ENatics Presentation and Demo Video](https://youtu.be/lZmXtx_qcds)
https://youtu.be/lZmXtx_qcds


Note: By using this software, you agree that the author has no liability whatsoever and you agree to Terms of Service and Privacy Policy.  <br />
See Terms of Service - https://arcane-spire-45844.herokuapp.com/terms <br />
See Privacy Policy - https://arcane-spire-45844.herokuapp.com/privacy <br />
