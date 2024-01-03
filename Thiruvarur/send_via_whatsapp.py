import requests
import urllib.parse
import os

from dotenv import load_dotenv

#load the environment variables from the file
load_dotenv('./.param.env')


thiruvarur_token = os.getenv('TIRUVARUR_TOKEN')
print(token)

def sendFileViaWhatsapp(token,phone_no,link,message):
    get_params = {
        token = thiruvarur_token,
        phone = "",
        link = "",
        message = ""
    }

    get_url = "http://whatsappsms.creativepoint.in/api/sendFileWithCaption"


