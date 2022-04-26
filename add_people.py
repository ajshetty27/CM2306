import dropbox
import os

dbx = dropbox.Dropbox('ACCESS TOKEN (will add when downloaded to raspberry pi)')

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

#Below function needs help with

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
