import socket
from tkinter import Button, Label, Tk, Toplevel, ttk, messagebox
from PIL import ImageTk, Image
import os
import webbrowser


def sync_people():
    # Execute the add_people.py script
    exec(open("add_people.py").read())
    # Provide a message box to confirm that the person has been added
    messagebox.showinfo(
        "Sync complete",
        "Latest known people have been added to the local known_people folder",
    )


def intruder_images():
    # Open a new window
    window = Toplevel()
    window.title("Intruder Images")
    window.geometry("500x500")
    # Show the images in intruder_images folder
    for i in os.listdir("intruder_images"):
        # Open the image and resize it
        img = Image.open("intruder_images/" + i)
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


def display_known_people():
    # Open a new window
    window = Toplevel()
    window.title("Known People")
    window.geometry("500x500")
    # Show the images in known_people folder
    for i in os.listdir("known_people"):
        # Open the image and resize it
        img = Image.open("known_people/" + i)
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


# Get your own IP address


def get_own_ip():
    ip_address = socket.gethostbyname(socket.gethostname())
    return ip_address


# Open a new window and display the camera feed


def view_camera():
    os.system("python3 rpi_camera_surveillance_system.py")
    # Open camera in your browser with your IP address
    webbrowser.open(get_own_ip() + ":8080")


root = Tk()
root.resizable(width=False, height=False)
# root.resizable(width=True, height=True)
root.geometry("800x650")
root.title("Communication Networks")
# root.configure(bg='white smoke')

w = Label(root, text="Communication Networks", font=("Helvetica", "30", "bold"))
w.pack(pady=20)

separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x")

img = ImageTk.PhotoImage(Image.open("example.png"))
panel = Label(root, image=img)
panel.pack(side="top", fill="both")

separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x")

# Create buttons with commands
btn = Button(root, text="Add Person", bd="4", command=sync_people)
btn2 = Button(root, text="Display Intruder Images", bd="4", command=intruder_images)
btn3 = Button(root, text="Display Known People", bd="4", command=display_known_people)

# Set the position of buttons
btn.place(relx=0.1, rely=0.80, relheight=0.1, relwidth=0.2)
btn2.place(relx=0.4, rely=0.80, relheight=0.1, relwidth=0.2)
btn3.place(relx=0.7, rely=0.80, relheight=0.1, relwidth=0.2)

root.mainloop()
