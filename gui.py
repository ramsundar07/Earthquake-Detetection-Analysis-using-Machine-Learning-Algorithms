from tkinter import *
from tkinter.ttk import *
from m2 import dt,svm,rf
# Creating a GUI Window
window = Tk()
window.geometry('800x800')
window.title("Earthquake Detection")
def dectree():
    year = float(e2_value.get())
    lat = float(e4_value.get())
    lon = float(e6_value.get())
    depth=float(e8_value.get())
    a=dt([year,lat,lon,depth])
    t1 = Text(window, height=2, width=30)
    t1.grid(row=4, column=1)
    t1.delete("1.0",END)
    t1.insert(END, a)

def svr():
     year = float(e2_value.get())
     lat = float(e4_value.get())
     lon = float(e6_value.get())
     depth=float(e8_value.get())
     a=float(svm([year,lat,lon,depth]))
     t1 = Text(window, height=2, width=30)
     t1.grid(row=4, column=1)
     t1.delete("1.0",END)
     t1.insert(END, a)
def randf():
    lat = float(e4_value.get())
    lon = float(e6_value.get())
    depth=float(e8_value.get())
    a=rf([lat,lon,depth])
    e9 = Label(window, text="Magnitude")
    e9.grid(row=4, column=0)
    t1 = Text(window, height=2, width=30)
    t1.grid(row=4, column=1,font=("calibri", 14))
    t1.delete("1.0",END)
    t1.insert(END, a)
#     t2.delete("1.0", END)
#     t2.insert(END, pound)
#     t3.delete("1.0", END)
#     t3.insert(END, ounce)

style = Style()
 
style.configure('TButton', font =
               ('calibri', 20, 'bold'),
                    borderwidth = '4')
 
# Changes will be reflected
# by the movement of mouse.
style.map('TButton', foreground = [('active', '!disabled', 'green')],
                     background = [('active', 'black')])

e1 = Label(window, text="Year",font=("calibri", 14))
e2_value = StringVar()
e2 = Entry(window, textvariable=e2_value,font=("calibri", 14))
e3 = Label(window, text="Latitude",font=("calibri", 14))
e4_value = StringVar()
e4 = Entry(window, textvariable=e4_value,font=("calibri", 14))
e5 = Label(window, text="Longitude",font=("calibri", 14))
e6_value = StringVar()
e6 = Entry(window, textvariable=e6_value,font=("calibri", 14))
e7 = Label(window, text="Depth",font=("calibri", 14))
e8_value = StringVar()
e8 = Entry(window, textvariable=e8_value,font=("calibri", 14))

b1 = Button(window, text="Decision Tree", command=dectree)
b2 = Button(window, text="SVM", command=svr)
b3 = Button(window, text="Random Forest", command=randf)
e1.grid(row=1, column=0,padx=2)
e2.grid(row=1, column=1,padx=2)
e3.grid(row=2, column=0,padx=2)
e4.grid(row=2, column=1,padx=2)
e5.grid(row=3, column=0,padx=2)
e6.grid(row=3, column=1,padx=2)
e7.grid(row=4, column=0,padx=2)
e8.grid(row=4, column=1,padx=2)

b1.grid(row=6, column=0,padx=20,pady=50)
b2.grid(row=6,column=1,padx=20,pady=50)
b3.grid(row=6,column=2,padx=20,pady=50)

window.mainloop()