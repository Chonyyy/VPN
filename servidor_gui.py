
import PySimpleGUI as sg
from udp import *
from vpn import VPN, Usuario




def windows_mesg():
    layout1 = [
        [sg.Text('Server started!')],
        [sg.Button('OK')]
    ]
    window2 = sg.Window('confirm', layout1, return_keyboard_events=True,element_justification='c')
    window2.size = (400, 400)
    while True:
        event, values = window2.read()
        if event == 'OK':
            if start_server()==0:
                print("llego")
                break
    window2.close()
    main()
            
def start_server():
    server = UDP('localhost', 5002)
    
    print('Servidor UDP iniciado\n')
    for i in server.ejecutar():
        print(f'Received: {i}\n')
     
    

def main():

    """Main function of the program."""
    # Set up GUI layout and window

    sg.theme('LightBlue')
    sg.set_options(font=('Comic Sans MS',18))

    layout = [
        [sg.Text('')],
        [sg.Text('Server', font=('Helvetica',30))],
        [sg.Text('')],
        [sg.Button('Start server')],
        [sg.Text('')],
    ]
    
    
    window1 = sg.Window('VPN', layout, element_justification='c')
    window1.size = (400, 400)
   
    

    window1.Resizable = False
    while True:
        event, values = window1.read()
        window1.Refresh()
        if event == sg.WIN_CLOSED:
            break
        if event== "Start server":
            start_server()
            

           

       
        


if __name__ == "__main__":
    main()
