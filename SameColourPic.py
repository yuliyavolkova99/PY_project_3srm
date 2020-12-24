import tkinter
from tkinter import messagebox as mb
import tkinter.scrolledtext as scroll
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
        self.image_cv1 = None
        self.frm = tkinter.Frame(self.window, width=310, height=250, bg = 'darkslategrey')
        self.frm.place(x = 450, y = 50)
        self.a = None
        self.colours = {'RED': [255, 0, 0],'GREEN': [0, 128, 0],'BLUE': [0, 0, 255]}

        

        pallete_name = tkinter.Label(text='The pallete', bg = 'darkslategrey').place(x = 540, y = 20)
        
        self.menu_menu = tkinter.Menu()

        self.file_menu = tkinter.Menu(tearoff = 0)
        self.file_menu.add_command(label="Upload new image", command = self.upload_new)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command = self.quit)

        self.menu_menu.add_cascade(label="File", menu = self.file_menu)
        self.menu_menu.add_cascade(label="Instruction", command = self.helpp)

        take_to_pallete = tkinter.Button(self.window, text = 'Find the pallete', width = 20, bg = 'teal', command = self.add_to_the_pallete).place(x = 30,y = 330)
        add_to_comparison = tkinter.Button(self.window, text = 'Add for comparison', width = 20, command = self.add_for_comparison ).place(x = 215, y = 330)
        colour = tkinter.Button(self.window, text = 'Chose the main colour', width = 20,command = self.chose_colour, bg = '#ccccb3').place(x = 400,y = 330)
        find_similar = tkinter.Button(self.window, text = 'Find similar images', width = 20,command = self.show_selected_images, bg = '#ccccb3').place(x = 585,y = 330)

        self.window.config(menu = self.menu_menu)
        
        self.window.mainloop()

    def helpp(self):
        self.root_rules = tkinter.Toplevel()
        self.root_rules.geometry('400x450')
        self.root_rules.title('Instruction')
        self.root_rules.resizable(False, False)
        self.ress = scroll.ScrolledText(self.root_rules, width = 45, height = 25)
        self.ress.place(x = 10, y = 10)
        with open("Instruction.txt") as fp:
                message = fp.read()
                self.ress.delete('1.0', 'end')
                self.ress.insert('insert', message)
        self.root_rules.mainloop()


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

    def get_im(self,im):
        self.image_cv1 = im
        self.image_cv1 = cv2.imread(self.window.filename)
        self.image_cv1 = cv2.cvtColor(self.image_cv1, cv2.COLOR_BGR2RGB)
        return self.image_cv1

    def RGB_to_HEX(self, colour):#преобразование RGB into hex
        return "#{:02x}{:02x}{:02x}".format(int(colour[0]), int(colour[1]), int(colour[2]))


    def get_colors(self, number_of_colours=8, show_chart = True):
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
        self.t = hex_colours
        if(show_chart): #диаграмма цветов
            plot = plt.figure(figsize=(5,3))
            plot1 = plot.add_subplot(111)
            plot1.pie(counts.values(), labels = hex_colours, colors = hex_colours, textprops={'fontsize': 5})
            plot1 = plt.gcf()
            plot1.set_size_inches(2.5,2.5)
            return plot1
                            

    def get_colors1(self, number_of_colours=8):
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
        rgb_colors = [ordered_colors[i] for i in counts.keys()]
        return rgb_colors

    def add_to_the_pallete(self): #добавление цветовой палитры в окно
        self.get_image()
        ans = self.get_colors()
        pallete = FigureCanvasTkAgg(ans, master = self.frm)
        pallete.get_tk_widget().pack()
        pallete.draw()

    def add_for_comparison(self, n = 0): #добавление изображений для сравнения из проводника 
        self.a = []
        while n != 3:
            self.window.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.JPG"),("png files","*.png")))
            imagee1 = Image.open(self.window.filename)
            base_width = 400
            width_percent = (base_width / float(imagee1.size[0]))
            hsize = int((float(imagee1.size[1] * float(width_percent))))
            imagee1 = imagee1.resize((base_width, hsize), Image.ANTIALIAS)
            self.my_image1 = ImageTk.PhotoImage(imagee1)
            self.temp = self.get_im(self.my_image1)
            self.a.append(self.temp)
            n +=1
    
    def match_image_by_colour(self, threshold = 60,number_of_colours = 8):
        for x in range(len(self.a)):
            self.match_colour = self.chose_colour()
            self.get_image()
            self.image_colours = self.get_colors1()#RGB_colors
            self.selected_colour = rgb2lab(np.uint8(np.asarray([self.match_colour])))
            self.select_image = False
            for x in range(self.number_of_colours):
                self.current_colour = rgb2lab(np.uint8(np.asarray([[self.image_colours[x]]])))
                self.diff = deltaE_cie76(self.selected_colour,self.current_colour)
                if(self.diff < threshold):
                    self.select_image = True
                return self.select_image #True or False
        
    def show_selected_images(self):
        selected = self.match_image_by_colour() #result of match_ == True or False with chosen colour!
        if (selected):
            self.root = tkinter.Toplevel() #создание дочернего окна
            self.root.geometry('700x450')
            self.root.title('Find similar image')
            self.root1.configure(background = 'darkslategrey')
            self.root.resizable(False, False)
            pallete_name11 = tkinter.Label(self.root, text='The result', bg = 'darkslategrey', font = ('Times New Roman',15), fg = 'white').place(x = 305, y = 20)
            self.frm1 = tkinter.Frame(self.root, width=400, height=300, bg = 'darkslategrey')
            self.frm1.place(x = 145, y = 80)
            plottt = plt.figure(figsize = (20, 10))
            self.ans2 = plt.subplot(1,3,i)
            self.ans2 = plt.imshow(self.a[x])
            pallete1 = FigureCanvasTkAgg(ans2, master = self.frm1)
            pallete1.get_tk_widget().pack()
            pallete1.draw() #вывод результата

    def change(self): #helping_function
        if self.var1.get() == 0:
            self.colour = self.colours.get('RED')
        elif self.var1.get() == 1:
            self.colour = self.colours.get('GREEN')
        elif self.var1.get() == 2:
            self.colour = self.colours.get('BLUE')
        return self.colour

    def chose_colour(self): #графический способ выбора цвета для поиска изо
        self.root1 = tkinter.Toplevel()
        self.root1.geometry('200x150')
        self.root1.title('Chosen of match colour')
        self.root1.configure(background = 'darkslategrey')
        self.root1.resizable(False, False)
        self.var1 = tkinter.IntVar()
        self.var1.set('0')
        r1 = tkinter.Radiobutton(self.root1,text='RED',variable=self.var1, value=0, bg = 'darkslategrey' )
        r2 = tkinter.Radiobutton(self.root1,text='GREEN',variable=self.var1, value=1, bg = 'darkslategrey')
        r3 = tkinter.Radiobutton(self.root1,text='BLUE',variable=self.var1, value=2, bg = 'darkslategrey')
        button = tkinter.Button(self.root1,text="Change",command=self.change())
        r1.pack()
        r2.pack()
        r3.pack()
        button.pack()
        self.root1.mainloop()
        
app = app()



