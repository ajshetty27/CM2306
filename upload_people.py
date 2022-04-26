import dropbox
import os
from dotenv import load_dotenv
load_dotenv()
dbx = dropbox.Dropbox(os.environ.get('DROPBOX_API_KEY'))

# Upload people to  Dropbox
for filename in os.listdir("known_people/"):
    print("Uploading " + filename)
    dbx.files_upload(open("known_people/" + filename, 'rb').read(), '/' + filename)
    print("Uploaded " + filename)
    print("")