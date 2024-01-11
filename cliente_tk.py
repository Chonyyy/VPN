import tkinter as tk
from tkinter import *
from tkinter import messagebox
import PIL
import login
from vpn import Paquete
import json
import udp


#methods
def verificar_loguin():
    if login.login(username_entry.get(),password_entry.get())==1 :
        messagebox.showinfo("Alerta", "ok")
        show_menuFrame()
    else:
        messagebox.showinfo("Alerta", "Try again!!!!")

#change frame
def showFrame_loguin():
    myFirstFrame.pack_forget()
    myFrame.pack(fill="both", expand="True")
def show_menuFrame():
    myFrame.pack_forget()
    menu_Frame.pack(fill="both", expand="True")        
def send_message():
    #data
    username=usernameM_entry.get()
    password=passwordM_entry.get()
    ip_dest=int(ipdest_entry.get())
    puerto_dest= int(puerto_dest_entry.get())
    data=data_entry.get()
    client = udp.UDP('localhost', 5000)
    paquete = Paquete(username, password, ip_dest, puerto_dest, data)
    paquete = json.dumps(paquete, default=lambda o: o.__dict__)
    client.enviar(paquete, ('localhost', 5001))
      
# Create the main window
root = tk.Tk()
# Set the window size to the size of the screen
#root.geometry("{}x{}".format(tk.Tk().winfo_screenwidth(), tk.Tk().winfo_screenheight()))

# Set the title of the window
root.title("Login vpn")
#root.iconbitmap('vpnn.ico')
# # Cargar la imagen y convertirla en un objeto PhotoImage
# imagen = PIL.ImageTk.PhotoImage(Image.open("img/imagenPrincipal1.png"))
root.resizable(True,False)
root.configure(bg='#87cefa')

#Frames...
#create frame-start
myFirstFrame=Frame(root)
myFirstFrame.configure(bg='#87cefa')
myFirstFrame.configure(width=900,height=750)
myFirstFrame.configure(relief="solid")
myFirstFrame.pack(fill="both", expand="True")
welcome_label=Label(myFirstFrame,text='Welcome to the fastes VPN',fg='white',bg='#87cefa')
welcome_label.config(font=("Comic Sans MS", 25, "bold"))
welcome_label.place(x='300',y='100')

# # Crear un widget Label y establecer su atributo image en el objeto PhotoImage
# label_imagen = tk.Label(myFirstFrame, image=imagen)
# label_imagen.place(x='250',y='240')

#buttom start
start_button = tk.Button(myFirstFrame, text="start-vpn",bg='#87cefa',fg='black',command=showFrame_loguin)
start_button.config(font=("Comic Sans MS", 20, "bold"))
start_button.place(x='450',y='350')

#create frame-loguin 
myFrame=Frame(root)
myFrame.configure(bg='#87cefa')
myFrame.configure(width=900,height=750)
myFrame.configure(relief="solid")
# Create a label for the username
username_label = tk.Label(myFrame, text="Username",fg='black',bg='#87cefa')
username_label.config(font=("Comic Sans MS", 25, "bold"))
username_label.place(x='450',y='200')
# Create a text entry box for the username
username_entry = tk.Entry(myFrame,bg='#87cefa')
username_entry.place(x='450',y='270')
# Create a label for the password
password_label = tk.Label(myFrame, text="Password",fg='black',bg='#87cefa')
password_label.config(font=("Comic Sans MS", 25, "bold"))
password_label.place(x='450',y='350')
# Create a text entry box for the password
password_entry = tk.Entry(myFrame, show="*",bg='#87cefa')
password_entry.place(x='450',y='400')
# Create a button to login
login_button = tk.Button(myFrame, text="Login",bg='#87cefa',fg='black',command=verificar_loguin)
login_button.config(font=("Comic Sans MS", 15, "bold"))
login_button.place(x='450',y='500')




#Create menu-frame
menu_Frame=Frame(root)
menu_Frame.configure(bg='#87cefa')
menu_Frame.configure(width=900,height=750)
menu_Frame.configure(relief="solid")
#label menu
menu_label=Label(menu_Frame,text='Send Data🦉',fg='black',bg='#87cefa')
menu_label.config(font=("Comic Sans MS", 40, "bold"))
menu_label.place(x='730',y='100')
#imputs to send messenger
# Create a label for the username
usernameM_label = tk.Label(menu_Frame, text="Username",fg='black',bg='#87cefa')
usernameM_label.config(font=("Comic Sans MS", 18, "bold"))
usernameM_label.place(x='730',y='300')
# Create a text entry box for the username
usernameM_entry = tk.Entry(menu_Frame,bg='#87cefa')
usernameM_entry.place(x='730',y='350')
# Create a label for the password
passwordM_label = tk.Label(menu_Frame, text="Password",fg='black',bg='#87cefa')
passwordM_label.config(font=("Comic Sans MS", 18, "bold"))
passwordM_label.place(x='730',y='450')
# Create a text entry box for the password
passwordM_entry = tk.Entry(menu_Frame,bg='#87cefa')
passwordM_entry.place(x='730',y='500')
# Create a label for the ip_dest
ipdest_label = tk.Label(menu_Frame, text="ip dest",fg='black',bg='#87cefa')
ipdest_label.config(font=("Comic Sans MS", 18, "bold"))
ipdest_label.place(x='730',y='550')
# Create a text entry box for the ip_dest
ipdest_entry = tk.Entry(menu_Frame,bg='#87cefa')
ipdest_entry.place(x='730',y='600')
# Create a label for the puerto_dest
puerto_dest_label = tk.Label(menu_Frame, text="puerto_dest",fg='black',bg='#87cefa')
puerto_dest_label.config(font=("Comic Sans MS", 18, "bold"))
puerto_dest_label.place(x='730',y='650')
# Create a text entry box for the puerto_dest
puerto_dest_entry = tk.Entry(menu_Frame,bg='#87cefa')
puerto_dest_entry.place(x='730',y='700')
# Create a label for the data
data_label = tk.Label(menu_Frame, text="data",fg='black',bg='#87cefa')
data_label.config(font=("Comic Sans MS", 18, "bold"))
data_label.place(x='730',y='750')
# Create a text entry box for the puerto_dest
data_entry = tk.Entry(menu_Frame,bg='#87cefa')
data_entry.place(x='730',y='800')

# Create a button to send_messenger
send_sms_button = tk.Button(menu_Frame, text="send",bg='#7DBFE8',fg='black',command=send_message)
send_sms_button.config(font=("Comic Sans MS", 18, "bold"))
send_sms_button.place(x='730',y='850')


# Start the main loop
root.mainloop()