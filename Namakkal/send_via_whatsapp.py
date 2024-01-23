import requests
import urllib.parse
import os

from dotenv import load_dotenv

def sendFileViaWhatsapp_post(
    college_token,whatsapp_phone_no,filename,caption):
    post_params1 = {
        "uid" : os.getenv("UID"),
        "pass" : os.getenv("PASS") 
    }
    print(post_params1)

    post_params2 = {
        "token" : college_token,
        "phone" : whatsapp_phone_no,
        "message" : caption
    }


    files = {
                'file': (open(filename, 'rb') ),
            }

    post_url1 = "https://wasmsapi.com/public/v1/client/login"
    #post_url2 = "https://wasmsapi.com/client/v1/message/send-file"
    post_url2 = "http://whatsappsms.creativepoint.in/api/sendFileWithCaption"
    session = requests.Session()
    response1 = session.post(post_url1, json=post_params1)
    print(response1.text)
    response2= session.post(post_url2,files=files, data=post_params2)

    print(response2.text)
    return


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

if __name__ == "__main__":
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



