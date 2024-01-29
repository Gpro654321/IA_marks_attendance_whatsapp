import requests
import urllib.parse
import os
import json
from requests_toolbelt import MultipartEncoder

from dotenv import load_dotenv

#{{{ old POST api endpoint
def sendFileViaWhatsapp_post(
    college_token,whatsapp_phone_no,filename,caption):

    '''
    # this was the login post parameters for the old portal
    post_params1 = {
        "uid" : os.getenv("UID"),
        "pass" : os.getenv("PASS") 
    }

    '''
    # url and login parameters for the new portal
    post_url1 = "https://api.enotify.app/auth/auth/login"
    post_params1 = {
        "phoneNumber": os.getenv("UID"),
        "password": os.getenv("PASS")
    }

    # new api end point and its parameters
    post_url2 = "https://api.enotify.app/test-message/media"
    post_params2 = {
        "instance" : college_token,
        "phone" : whatsapp_phone_no,
        "caption" : caption
    }

    print(post_params1)

    '''
    # old api endpoint and its parameters

    post_url2 = "http://whatsappsms.creativepoint.in/api/sendFileWithCaption"

    post_params2 = {
        "token" : college_token,
        "phone" : whatsapp_phone_no,
        "message" : caption
    }

    '''

    files = {
                'file': (open(filename, 'rb') ),
            }

    #post_url1 = "https://wasmsapi.com/public/v1/client/login"
    #post_url2 = "https://wasmsapi.com/client/v1/message/send-file"
    
    session = requests.Session()
    response1 = session.post(post_url1, json=post_params1)
    print(response1.text)
    response1a = session.options(post_url2)
    print(response1a.text)
    response2= session.post(post_url2,files=files, data=post_params2)


    print(response2.text)
    return

#}}}

# {{{ old GET endpoint
def sendFileViaWhatsapp_get(
    college_token,whatsapp_phone_no,file_link,caption):


    get_params = {
        "token": college_token,
        "phone": whatsapp_phone_no,
        "link": file_link,
        "message": caption 
    }

    #get_url = "http://whatsappsms.creativepoint.in/api/sendFileWithCaption"

    get_url = "http://whatsappsms.creativepoint.in/api/sendFileWithCaption"
    print(get_params["link"])

    response = requests.get(get_url, params=get_params)
    print(response.text)
    return

#}}}

#{{{ 20240126 POST api endpoint
# sendFileViaWhatsapp_post2(instanceId,to_phone,imageUrl,message)
def sendFileViaWhatsapp_post2(
    token,
    to_phone,
    imageURL,
    message
):
    print("inside sendFileViaWhatsapp_post2")
    post_url = "http://whatsappsms.creativepoint.in/api/sendFileWithCaption"
    post_data = {
        'token' : token,
        'phone' : to_phone,
        'link'  : imageURL,
        'message': message
    }

    print(post_url)
    print(post_data)

    r1 = requests.options(post_url)
    print(r1)

    print("Headers:")
    for header, value in r1.headers.items():
        print(f"  {header}: {value}")

    r2 = requests.post(post_url, data=post_data)
    print(r2.text)
    return
#}}}

# {{{ sendFileViaWhatsapp_get2(instanceId,to_phone,imageUrl,message)

def sendFileViaWhatsapp_get2(
    token,
    to_phone,
    imageURL,
    message
):
    print("inside sendFileViaWhatsapp_get2")
    get_url = "http://whatsappsms.creativepoint.in/api/sendFileWithCaption"
    params = {
        'token' : token,
        'phone' : to_phone,
        'link'  : imageURL,
        'message': message
    }

    print(get_url)
    print(params)

    r1 = requests.options(get_url)
    print(r1)

    print("Headers:")
    for header, value in r1.headers.items():
        print(f"  {header}: {value}")

    r2 = requests.get(get_url, params=params)
    print(r2.text)
    return

#}}}

# {{{sendTextMessage_post(token,phone,message)

def sendTextMessage_post(token,phone, message):
    print("Insdie sendTextMessage")

    post_url = 'http://whatsappsms.creativepoint.in/api/sendText'
    print(post_url)

    post_data = {
        'token' : token,
        'phone' : phone,
        'message': message
    }
    print(post_data)

    r1 = requests.post(post_url, data=post_data)
    print(r1.text)
    return

    
    
# }}}

#{{{sendTextMessage_get(token,phone,message)
def sendTextMessage_get(token, phone, message):
    print("Inside sendTextMessage_get")

    get_url = 'http://whatsappsms.creativepoint.in/api/sendText'

    params = {
        'token' : token,
        'phone' : phone,
        'message': message
    }
    r1 = requests.get(get_url, params=params)
    print(r1.text)
    return

#}}}

#{{{sendMediaViaTestApi(token, phone, caption):
def sendMediaViaTestApi(token, phone, filename, caption):

    # url and login parameters for the new portal
    post_url1 = "https://api.enotify.app/auth/auth/login"
    post_params1 = {
        "phoneNumber": os.getenv("UID"),
        "password": os.getenv("PASS")
    }


    print(post_params1)

    session = requests.Session()
    response1 = session.post(post_url1, json=post_params1)
    print(response1.text)
    print(type(response1))
    response1_dict = json.loads(response1.text)
    print(response1_dict)
    auth_token = 'Bearer' + " " +(response1_dict["tokens"]["accessToken"])

    # new api end point and its parameters
    post_url2 = "https://api.enotify.app/test-message/media"
    post_params2 = {
        "instance" : token,
        "phone" : phone,
        "caption" : caption,
        #"file" : ('filename', open(filename, 'rb'), 'application/pdf')
    }

    print(post_params2)

    m = MultipartEncoder(post_params2)

    headers2 = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Authorization': auth_token,
        #'Content-Type': m.content_type 
    }

    print(headers2)


    files = {
                'file': ('filename', open(filename, 'rb'), ),
            }

    #response2= session.post(post_url2, headers= headers2, files=files, data=post_params2)
    encoder2 = MultipartEncoder(fields=post_params2)
    print(encoder2.to_string())

    response2= session.post(post_url2, headers= headers2, files=files, data=post_params2)


    print(response2.text)
    return

#}}}

# {{{sendMessageViaTestApi(token, phone, caption)
def sendMessageViaTestApi(token, phone, caption):

    # url and login parameters for the new portal
    post_url1 = "https://api.enotify.app/auth/auth/login"
    post_params1 = {
        "phoneNumber": os.getenv("UID"),
        "password": os.getenv("PASS")
    }


    print(post_params1)

    session = requests.Session()
    response1 = session.post(post_url1, json=post_params1)
    print(response1.text)
    print(type(response1))
    response1_dict = json.loads(response1.text)
    print(response1_dict)
    auth_token = 'Bearer' + " " +(response1_dict["tokens"]["refreshToken"])

    post_url2 = "https://api.enotify.app/test-message/text"
    post_params2 = {
        "to": phone,
        "message": caption,
        "instance" : token
    }

    print(post_params2)

    headers2 = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Authorization': auth_token  
    }

    print(headers2)

    response2= session.post(post_url2, headers= headers2, data=post_params2)

    print(response2.text)
    return
#}}}

#{{{ sendFileViaWasmpi(token,phone,link,caption)
def sendFileViaWasmapi(token, phone, link, caption):
    post_url = 'https://wasmsapi.com/api/sendFileWithCaption'
    params = {
        'instance_id' : token,
        'phone' : phone,
        'link' : link,
        'message': message
    }

    r1 = requests.post(post_url, data = params)
    print(r1.text)
    return
# }}}



if __name__ == "__main__":
    '''
    old test
    print("I am inside main")
    #load the environment variables from the file
    load_dotenv('./.param.env')

    thiruvarur_token = os.getenv('TIRUVARUR_TEST_TOKEN')
    print(thiruvarur_token)

    test_phone = "91" + str("9443015064")
    test_file_link = "./pdf_files/test.pdf"
    test_caption = ("Dear Parent,\n" +
                    "The document attached above," +
                    "contains the performance evaluation of [son/daughter] in the Department of Physiology."+
                    "\n\n"+
                    "HOD of Physiology,\n"+
                    "Govt. Tiruvarur Medical College, Tiruvarur")

    #sendFileViaWhatsapp_get(thiruvarur_token,test_phone,test_file_link,test_caption)
    sendFileViaWhatsapp_post(thiruvarur_token, test_phone, test_file_link, test_caption)
    '''

    load_dotenv('./.param.env')
    print('Inside main function of send_via_whatsapp')

    token = os.getenv('TOKEN')
    print(token)

    phone = str('91') + os.getenv('SELF_PHONE') 
    print(phone)

    #imageURL = 'https://cdn.pixabay.com/photo/2014/02/27/16/10/flowers-276014_640.jpg'
    #imageURL = 'https://apod.nasa.gov/apod/image/2401/Ain_4096.jpg'

    imageURL = 'https://gladly-leading-moose.ngrok-free.app/student_report_0001_Test%201.pdf'
    print(imageURL)

    # message = '20240126'
    message = 'wasmapi test'
    print(message)

    filename = './flowers-276014_640.jpg'

    # sendMessageViaTestApi(token, phone, message)
    # sendMediaViaTestApi(token, phone,filename, message)
    # sendFileViaWhatsapp_post2(token,phone,filename,message)
    sendFileViaWhatsapp_get2(token, phone, imageURL, message)
    # sendFileViaWasmapi(token,phone,imageURL,message)

    
    '''
    print('sending a plain text message')
    sendTextMessage_post(token, phone, message)

    print("sending text via get")
    sendTextMessage_get(token, phone, message)

    '''



