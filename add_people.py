import dropbox
import os
from dotenv import load_dotenv
load_dotenv()
dbx = dropbox.Dropbox(os.environ.get('DROPBOX_API_KEY'))

dropbox_dict = {}
local_list = []
new_addition = []

for entry in dbx.files_list_folder('').entries:
    path = entry.name
    path_check = entry.id
    dropbox_dict[path] = path_check
    #print(path)
    #print(path_check)

for filename in os.listdir("known_people/"):
    #print(filename)
    local_list.append(filename)

print(dropbox_dict)
print(local_list)

#Checks new files in dropbox api
new_addition = list(set(dropbox_dict.keys()) - set(local_list))
print(new_addition)

if not new_addition:
    print("known_people is upto date")

else:
    for i in new_addition:
        print("Downloading " + i)
        dbx.files_download_to_file(i, i)
        print("Downloaded " + i)
        print("Adding " + i + " to known_people")
        os.rename(i, "known_people/" + i)
        print("Added " + i + " to known_people")
        print("")
