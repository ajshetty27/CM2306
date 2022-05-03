from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
import cv2


def add_person():
    os.system('add_person.py')


def intruder_images():
    # Open a new window
    window = Toplevel()
    window.title("Intruder Images")
    window.geometry('500x500')
    # Show the images in intruder_images folder
    for i in os.listdir('intruder_images'):
        # Open the image and resize it
        img = Image.open('intruder_images/' + i)
        img = img.resize((150, 150), Image.ANTIALIAS)
        # Get the filename of the image
        filename = os.path.splitext(i)[0]
        # Convert the image to Tkinter format
        img = ImageTk.PhotoImage(img)
        # Create a label for the image and add it to the window, also add the filename
        label = Label(window, image=img)
        label.image = img
        label.pack()
        label = Label(window, text=filename)
        label.pack()


root = Tk()
root.resizable(width=False, height=False)
# root.resizable(width=True, height=True)
root.geometry("800x650")
root.title("Communication Networks")
# root.configure(bg='white smoke')

w = Label(root, text='Communication Networks', font=("Helvetica", "30", 'bold'))
w.pack(pady=20)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')

img = ImageTk.PhotoImage(Image.open("example.png"))
panel = Label(root, image=img)
panel.pack(side="top", fill="both")

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')

# Create buttons with commands
btn = Button(root, text='Add Person', bd='4', command=add_person)
btn2 = Button(root, text='Display Intruder Images', bd='4', command=intruder_images)

# Set the position of buttons
btn.place(relx=0.1, rely=0.80, relheight=0.1, relwidth=0.2)
btn2.place(relx=0.4, rely=0.80, relheight=0.1, relwidth=0.2)

root.mainloop()
