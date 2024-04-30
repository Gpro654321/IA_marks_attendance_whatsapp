import os
from twilio.rest import Client

from dotenv import load_dotenv

load_dotenv('./.param.env')

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_ = 'whatsapp:+14155238886',
    body = 'how do you do', 
    to = 'whatsapp:+919443015064',
    media_url=['http://tinyurl.com/5n9xfebb']
)

print(message.status)
print(message.sid)
