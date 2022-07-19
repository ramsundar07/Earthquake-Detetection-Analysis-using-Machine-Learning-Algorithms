from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
from tkinter.ttk import Style
from gui_algorithm import dt,svm,rf,knn,showmap,freqgraph,maggraph
from PIL import ImageTk
# Creating a GUI Window
window = Tk()
window.geometry("600x700")
window.title("Earthquake Detection")
window.config(bg="black")

def alert(a):
    if((a>=5.5) and (a<=6)):
        messagebox.showwarning("Magnitude : "+str(a), "May Cause Slight damage to buildings and other structures.")
    elif((a>6)and(a<=7)):
        messagebox.showerror("Magnitude : "+str(a), "May cause a lot of damage in very populated areas")
    elif(a>2.5):
        messagebox.showinfo("Magnitude : "+str(a),"Often felt, but only causes minor damage")
    else:
         messagebox.showinfo("Magnitude : "+str(a),"No Earthquake has been detected")
def dectree():
    year = float(e2_value.get())
    lat = float(e4_value.get())
    lon = float(e6_value.get())
    depth=float(e8_value.get())
    if depth==0:
        alert(0)
        return 0
        
    a=dt([year,lat,lon,depth])
    e9 = Label(window, text="Magnitude",font=("Cooper Black", 14),bg="black",fg="white",bd='5',pady=5)
    e9.place(x=100,y=300)
    t1 = Text(window, height=2, width=30,font=("calibri", 14))
    t1.place(x=250,y=300)
    t1.delete("1.0",END)
    t1.insert(END, a)
    alert(a)

def svr():
     year = float(e2_value.get())
     lat = float(e4_value.get())
     lon = float(e6_value.get())
     depth=float(e8_value.get())
     if depth==0:
        alert(0)
        return 0
    
     a=float(svm([year,lat,lon,depth]))
     e9 = Label(window, text="Magnitude",font=("Cooper Black", 14),bg="black",fg='white',bd='5',pady=5)
     e9.place(x=100,y=300)
     t1 = Text(window, height=2, width=30,font=("Calibri", 14))
     t1.place(x=250,y=300)
     t1.delete("1.0",END)
     t1.insert(END, a)
     alert(a)

def randf():
    lat = float(e4_value.get())
    lon = float(e6_value.get())
    depth=float(e8_value.get())
    if depth==0:
        alert(0)
        return 0

    a=rf([lat,lon,depth])
    e9 = Label(window, text="Magnitude",font=("Cooper Black", 14),bg="black",fg='white',bd='5',pady=5)
    e9.place(x=100,y=300)
    t1 = Text(window, height=2, width=30,font=("calibri", 14))
    t1.place(x=250,y=300)
    t1.delete("1.0",END)
    t1.insert(END, a)
    alert(a)
def knnr():
     year = float(e2_value.get())
     lat = float(e4_value.get())
     lon = float(e6_value.get())
     depth=float(e8_value.get())
     if depth==0:
        alert(0)
        return 0

     a= knn([year,lat,lon,depth])
     e9 = Label(window, text="Magnitude",font=("Cooper Black", 14,'bold'),bg="black",fg='white',bd='5',pady=5)
     e9.place(x=100,y=300)
     t1 = Text(window, height=2, width=30,font=("calibri", 14))
     t1.place(x=250,y=300)
     t1.delete("1.0",END)
     t1.insert(END, a)
     alert(a)


style = Style()
 
style.configure('TButton', font =
               ('Cooper Black', 20, 'bold'),
                    borderwidth = '4')
 
# Changes will be reflected
style.map('TButton', foreground = [('active', '!disabled', 'green')],
                     background = [('active', 'black')])

img=ImageTk.PhotoImage(file="C:\\Users\\Ramz\\Jupyter ML\\1st Review\\bgimg.png")
label_img = Label(window,image=img)
label_img.pack()
titleLabel=Label(window,bg='black',fg="floral white",text="Earthquake Detection",font=("Agency FB",30,"bold"))
titleLabel.place(x=170,y=10)
  

e1 = Label(window, text="Year",font=("Cooper Black", 14,'bold'),bg="black",fg='white',bd='5',pady=5)
e2_value = StringVar()
e2 = Entry(window, textvariable=e2_value,font=("calibri", 14,'bold'))
e3 = Label(window, text="Latitude",font=("Cooper Black", 14,'bold'),bg="black",fg='white',bd='5',pady=5)
e4_value = StringVar()
e4 = Entry(window, textvariable=e4_value,font=("calibri", 14,'bold'))
e5 = Label(window, text="Longitude",font=("Cooper Black", 14,'bold'),bg="black",fg='white',bd='5',pady=5)
e6_value = StringVar()
e6 = Entry(window, textvariable=e6_value,font=("calibri", 14,'bold'))
e7 = Label(window, text="Depth",font=("Cooper Black", 14,'bold'),bg="black",fg='white',bd='5',pady=5)
e8_value = StringVar()
e8 = Entry(window, textvariable=e8_value,font=("calibri", 14,'bold'))

b1 = Button(window,text="Decision Tree",bd ='5',bg='black',fg='white',pady=5,font=("calibri", 14,'bold'),command=dectree)
b2 = Button(window, text="SVM",bd ='5', bg='black',fg='white',pady=5,font=("calibri", 14,'bold'),command=svr)
b3 = Button(window, text="Random Forest",bd ='5',bg='black',fg='white',pady=5,font=("calibri", 14,'bold'),command=randf)
b4 = Button(window, text="KNN",bd ='5',bg='black',fg='white',pady=5,font=("calibri", 14,'bold'),command=knnr)
b5 = Button(window, text="Plot Map",bd ='5',bg='black',fg='white',pady=5,font=("calibri", 14,'bold'),command=showmap)
b6 = Button(window, text="Frequency Graph",bd ='5',bg='black',fg='white',pady=5,font=("calibri", 14,'bold'),command=freqgraph)
b7 = Button(window, text="Magnitude chart",bd ='5',bg='black',fg='white',pady=5,font=("calibri", 14,'bold'),command=maggraph)

e1.place(x=100,y=140)
e2.place(x=250,y=140)
e3.place(x=100,y=180)
e4.place(x=250,y=180)
e5.place(x=100,y=220)
e6.place(x=250,y=220)
e7.place(x=100,y=260)
e8.place(x=250,y=260)

b1.place(x=55,y=380)
b2.place(x=205,y=380)
b3.place(x=355,y=380)
b4.place(x=505,y=380)
b5.place(x=60,y=470)
b6.place(x=205,y=470)
b7.place(x=410,y=470)


window.mainloop()