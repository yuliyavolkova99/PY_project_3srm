import tkinter
from tkinter import messagebox as mb
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class app():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry('760x400')
        self.window.title('SameColourPic')
        self.window.resizable(False,False)
        self.window.configure(background = 'darkslategrey')
        self.window.filename = None
        self.labell = tkinter.Label(width=400, height=300, bg = 'darkslategrey')
        self.labell.place(x=25,y=10)
        self.image_cv = None
        self.frm = tkinter.Frame(self.window, width=310, height=250, bg = 'darkslategrey')
        self.frm.place(x = 450, y = 50)

        pallete_name = tkinter.Label(text='The pallete', bg = 'darkslategrey').place(x = 540, y = 20)
        
        self.menu_menu = tkinter.Menu()

        self.file_menu = tkinter.Menu(tearoff = 0)
        self.file_menu.add_command(label="Upload new image", command = self.upload_new)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command = self.quit)

        self.menu_menu.add_cascade(label="File", menu = self.file_menu)
        self.menu_menu.add_cascade(label="Instruction")

        take_to_pallete = tkinter.Button(self.window, text = 'Find the pallete', width = 25, bg = 'teal', command = self.add_to_the_pallete).place(x = 35,y = 330)
        find_similar = tkinter.Button(self.window, text = 'Find similar images', width = 25, bg = '#ccccb3').place(x = 235,y = 330)

        self.window.config(menu = self.menu_menu)
        self.window.mainloop()


    def quit(self):
        que = mb.askyesno(title = 'Attention!', message = 'Do you really want to go out of the programm?')
        if que == True:
            self.window.destroy()
        else:
            pass

    def upload_new(self): #функция загрузки изображения в окно
        self.window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.JPG"),("png files","*.png")))
        imagee = Image.open(self.window.filename)
        base_width = 400
        width_percent = (base_width / float(imagee.size[0]))
        hsize = int((float(imagee.size[1] * float(width_percent))))
        imagee = imagee.resize((base_width, hsize), Image.ANTIALIAS)
        self.my_image = ImageTk.PhotoImage(imagee)
        self.labell.config(image = self.my_image)
        for widget in self.frm.winfo_children():
            widget.destroy()
        
    def get_image(self):
        self.image_cv = cv2.imread(self.window.filename)#считываем изображение
        self.image_cv = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2RGB)#преобразование в RGB (переход из BGR)

    def RGB_to_HEX(self, colour):#преобразование RGB into hex
        return "#{:02x}{:02x}{:02x}".format(int(colour[0]), int(colour[1]), int(colour[2]))


    def get_colors(self, number_of_colours=8, show_chart=True):
        #уменьшим изображение (пиксели), чтобы сократить время для извлечения цветов
        modified_image = cv2.resize(self.image_cv, (600, 400), interpolation = cv2.INTER_AREA)
        modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
                            
        clf = KMeans(n_clusters = number_of_colours) #создание кластеров на основе количества цветов
        labels = clf.fit_predict(modified_image) #извлечение прогноза == выполнение кластеризации и возвращение метки кластеров
        counts = Counter(labels) #подсчет количества меток
        counts = dict(sorted(counts.items())) #формирование словаря для сортировки на основе кортежа
                            
        center_colours = clf.cluster_centers_ #поиск цветов
        ordered_colours = [center_colours[i] for i in counts.keys()] #перебор ключей/255
        hex_colours = [self.RGB_to_HEX(ordered_colours[i]) for i in counts.keys()] #получение hex_colours

        if show_chart: #диаграмма цветов
            plot = plt.figure(figsize=(5,3))
            plot1 = plot.add_subplot(111)
            plot1.pie(counts.values(), labels = hex_colours, colors = hex_colours, textprops={'fontsize': 5})
            plot1 = plt.gcf()
            plot1.set_size_inches(2.5,2.5)
            return plot1
                            
    def add_to_the_pallete(self): #добавление цветовой палитры в окно
        self.get_image()
        ans = self.get_colors()
        pallete = FigureCanvasTkAgg(ans, master = self.frm)
        pallete.get_tk_widget().pack()
        pallete.draw()


app = app()


