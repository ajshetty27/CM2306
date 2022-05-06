import os
import http.client
from dotenv import load_dotenv
load_dotenv()


# Sends SMS using infobip API


BASE_URL = "jdzk4v.api.infobip.com"
API_KEY = os.environ.get('INFOBIP_API_KEY')

print('THE API KEY: ',API_KEY)

SENDER = "InfoSMS"
RECIPIENT = "447341033081"
MESSAGE_TEXT = "ALERT - An unknown person has been detected at your security camera. Check your email for more details."

conn = http.client.HTTPSConnection(BASE_URL)

payload1 = "{\"messages\":" \
          "[{\"from\":\"" + SENDER + "\"" \
          ",\"destinations\":" \
          "[{\"to\":\"" + RECIPIENT + "\"}]," \
          "\"text\":\"" + MESSAGE_TEXT + "\"}]}"

headers = {
    'Authorization': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
conn.request("POST", "/sms/2/text/advanced", payload1, headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
