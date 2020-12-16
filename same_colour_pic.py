import tkinter
from tkinter import messagebox as mb
from tkinter import Canvas
from tkinter import filedialog
from PIL import ImageTk, Image
import pandas as pd
import cv2
import numpy as np

class app():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry('730x400')
        self.window.title('SameColourPic')
        self.window.resizable(False,False)

        pallete = Canvas(width=250, height=250, bg = 'white').place(x = 450, y = 45)
        pallete_name = tkinter.Label(text='The pallete').place(x = 540, y = 20)
        
        self.menu_menu = tkinter.Menu()

        self.file_menu = tkinter.Menu(tearoff = 0)
        self.file_menu.add_command(label="Upload new image", command = self.upload_new)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command = self.quit)

        self.menu_menu.add_cascade(label="File", menu = self.file_menu)
        self.menu_menu.add_cascade(label="Instruction")

        take_to_pallete = tkinter.Button(self.window, text = 'Add to pallete', width = 25, bg = '#bcb100').place(x = 35,y = 330)
        find_similar = tkinter.Button(self.window, text = 'Find similar', width = 25, bg = '#ccccb3').place(x = 235,y = 330)

        self.window.config(menu = self.menu_menu)
        self.window.mainloop()

    def quit(self):
        que = mb.askyesno(title = 'Attention!', message = 'Do you really want to go out of the programm?')
        if que == True:
            self.window.destroy()
        else:
            pass

    def upload_new(self):
        self.window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (('all files','*.*'),("jpeg files","*.JPG"),("png files","*.png")))
        self.image = Image.open(self.window.filename)
        base_width = 400
        width_percent = (base_width / float(self.image.size[0]))
        hsize = int((float(self.image.size[1] * float(width_percent))))
        self.image1 = self.image.resize((base_width, hsize), Image.ANTIALIAS)
        self.my_image = ImageTk.PhotoImage(self.image1)
        self.labell = tkinter.Label(image = self.my_image, width=400, height=300).place(x=25,y=10)

        index=["color","color_name","hex","R","G","B"]
        self.df = pd.read_csv('colors.csv', names = index)

        img = cv2.imread('self.image',cv2.IMREAD_COLOR)
        

        

app = app()


