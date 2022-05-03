from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import webview
import os

def add_person():
    os.system('add_person.py')

def intruder_images():
    os.system('')

def view_camera():
    os.system('rpi_surveillance_camera.py')
    webview.create_window('Camera View', 'https://www.google.com') #insert website here
    webview.start()
    
root = Tk()
root.resizable(width=False, height=False)
#root.resizable(width=True, height=True)
root.geometry("800x650")
root.title("Communication Networks")
#root.configure(bg='white smoke')

w = Label(root, text='Communication Networks', font=("Helvetica", "30", 'bold'))
w.pack(pady=20)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')

img = ImageTk.PhotoImage(Image.open("example.png"))
panel = Label(root, image = img)
panel.pack(side = "top", fill = "both")

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')

# Create buttons with commands
btn = Button(root, text = 'Add Person', bd = '4', command = add_person)
btn2 = Button(root, text = 'Display Intruder Images', bd = '4', command = intruder_images)
btn3 = Button(root, text = 'View Camera Feed', bd = '4', command = view_camera)

# Set the position of buttons
btn.place(relx=0.1, rely=0.80, relheight=0.1, relwidth=0.2)
btn2.place(relx=0.4, rely=0.80, relheight=0.1, relwidth=0.2)
btn3.place(relx=0.7, rely=0.80, relheight=0.1, relwidth=0.2)


root.mainloop()
