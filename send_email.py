import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

file_path = '' #insert image file path (include filetype in name)

message = Mail(
    from_email='groomj@cardiff.ac.uk',
    to_emails='ShettyA6@cardiff.ac.uk',
    subject='INTRUDER WTF',
    html_content='<h1> Intruder Detected </h1><p>An intruder has been detected at your security camera. Please find attached the following image captured. </p>'
)

with open(file_path, 'rb') as f:
    data = f.read()
    f.close()
encoded_file = base64.b64encode(data).decode()

#If file is a PNG then convert to JPG
if file_path.endswith('.png'):
    file_path = file_path.replace('.png', '.jpg')
    
attachedFile = Attachment(
    FileContent(encoded_file),
    FileName(file_path),
    FileType('application/jpg'),
    Disposition('attachment')
)

message.attachment = attachedFile
        
try:
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.msg)

