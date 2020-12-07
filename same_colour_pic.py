import tkinter
from tkinter import messagebox as mb
from tkinter import Canvas
import tkinter.scrolledtext as scroll

window = tkinter.Tk()
window.geometry('730x400')
window.title('SameColourPic')
window.resizable(False,False)

field_for_image = Canvas(window, width = 400, height = 300)
field_for_image.place(x = 25, y =10)
field_for_image.focus_set()
field_for_image.score = 0

pallete = Canvas(width=250, height=250, bg = 'white').place(x = 450, y = 45)
pallete_name = tkinter.Label(text='Палитра').place(x = 540, y = 20)

def quit():
    que = mb.askyesno(title = 'Внимание!', message = 'Вы точно хотите выйти из программы?')
    if que == True:
        window.destroy()
    else:
        pass
        
    
menu_menu = tkinter.Menu()

file_menu = tkinter.Menu(tearoff = 0)
file_menu.add_command(label="Upload new image")
file_menu.add_separator()
file_menu.add_command(label="Exit", command = quit)

menu_menu.add_cascade(label="File", menu = file_menu)
menu_menu.add_cascade(label="Instruction")

take_to_pallete = tkinter.Button(window, text = 'Добавить в палитру', width = 25, bg = '#bcb100').place(x = 35,y = 330)
find_similar = tkinter.Button(window, text = 'Найти похожие', width = 25, bg = '#ccccb3').place(x = 235,y = 330)

window.config(menu = menu_menu)
window.mainloop()
