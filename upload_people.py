import dropbox
import os
from dotenv import load_dotenv
load_dotenv()
dbx = dropbox.Dropbox(os.environ.get('DROPBOX_API_KEY'))

# Upload people to but check if they already exist in Dropbox
for filename in os.listdir("known_people/"):
    if filename.endswith(".jpg"):
        with open("known_people/" + filename, "rb") as f:
            try:
                dbx.files_upload(f.read(), "/known_people/" + filename)
            except dropbox.exceptions.AccessError:
                print("File already exists in Dropbox")
                continue
            print("Uploaded " + filename)