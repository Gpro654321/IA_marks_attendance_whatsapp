from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError
import os
import datetime
import sys


from dotenv import load_dotenv


def upload_file_to_folder(folder_id, filepath):

    scope = ['https://www.googleapis.com/auth/drive'] 

    # load the environment variables
    load_dotenv('./.param.env')

    script_key_file_path = os.getenv('ACCESS_KEY_FILE_PATH')
    service_account_json_key = script_key_file_path 

    credentials = service_account.Credentials.from_service_account_file(
        filename = service_account_json_key,
        scopes=scope

    )

    service = build('drive', 'v3', credentials=credentials)

    
    abs_file_path = os.path.abspath(filepath)
    print(abs_file_path)
    dest_file = os.path.basename(filepath) 

    file_metadata = {
        'name' : dest_file,
        'parents' : [folder_id]
    }

    media = MediaFileUpload(
        abs_file_path,
        mimetype = 'application/pdf',
        resumable = True
    )

    file = service.files().create(body=file_metadata, 
                                 media_body=media,
                                 fields='id').execute()
    print("i have uploaded")


def create_folder(parent_folder_id):
    '''
    create a folder inside a parent folder with name of the form
    YYYYMMDD
    '''

    now = datetime.datetime.now()
    current_time_string = now.strftime("%Y%m%d")

    scope = ['https://www.googleapis.com/auth/drive'] 

    # load the environment variables
    load_dotenv('./.param.env')

    script_key_file_path = os.getenv('ACCESS_KEY_FILE_PATH')
    service_account_json_key = script_key_file_path 

    credentials = service_account.Credentials.from_service_account_file(
        filename = service_account_json_key,
        scopes=scope

    )

    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': current_time_string,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents' : [parent_folder_id]
    }

    file = service.files().create(body=file_metadata,
                                  fields='id'
                                 ).execute()
    print("created folder")
    folder_id = file.get('id')
    print(folder_id)
    return folder_id

    


# filepath = './pdf_files/iec_cert_10_Dr.pdf'
parent_folder_id = '16D_aac1kHTpFsLmmqIz8Ji9FpqACZAOx'
# upload_file_to_folder(folder_id, filepath)

file_list = os.listdir('./pdf_files')
print(file_list)

# terminate the script if there are no files
if len(file_list) == 0:
    print("Exiting!!! as there are no files to upload")
    sys.exit(0)

sub_folder_id = create_folder(parent_folder_id)

for i in file_list:
    file_path = os.path.join('./pdf_files', i)
    upload_file_to_folder(sub_folder_id,file_path)
    # to prevent cluttering of the pdf_files folder
    # files will be removed once uploaded
    os.remove(file_path)



