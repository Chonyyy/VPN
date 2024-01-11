
from restricciones import RestriccionUsuario, RestriccionVLAN
import PySimpleGUI as sg
from udp import *
from vpn import VPN, Usuario
import threading

# Create a VPN instance

ip = 'localhost'
puerto = 5001
vpn = VPN(UDP(ip, puerto))
vpn_thread = None



def CreateUser():
    """Create a window to input a user"""
    layout = [
        [sg.Text('')],
        [sg.Text('GangVPN', font=('Helvetica',42))],
        [sg.Text("Create User",font=('Arial',18))],
        [sg.Text('Username:',size=(15,1),expand_x=True), sg.Input(key='username')],
        [sg.Text('Password:',size=(15,1),expand_x=True), sg.Input(key='password',password_char='*')],
        [sg.Text('Check password:',size=(15,1),expand_x=True), sg.Input(key='Check',password_char='*')],
        [sg.Text('VLAN:',size=(15,1),expand_x=True), sg.Input(key='vlan')],
        [sg.Text('')],
        [sg.Button('Submit', bind_return_key=True), sg.Cancel('Exit')],
        [sg.Text('')]
        ]
    window = sg.Window('VPN User Creator', layout, return_keyboard_events=True,element_justification='c')
    while True:
        event, values = window.Read()
        if event == 'Submit':
            try:
                usuario = values['username']
               
                if usuario == '' or usuario is None:
                    sg.PopupOK("Please introduce user name")
                    continue
                
                contrasenna = values['password']
                if contrasenna == '' or contrasenna is None:
                    sg.PopupOK("Please introduce password")
                    continue
                if values['Check'] != contrasenna:
                    sg.PopupOK("The passwords don't match")
                    continue
                
                id_vlan = int(values['vlan'])
                vpn.crear_usuario(Usuario(usuario, contrasenna, id_vlan))
               
                sg.PopupOK('User Created')
                #update values
                window['username'].Update("")
                window['password'].Update("")
                window['Check'].Update("")
                window['vlan'].Update("")
            except Exception as e:
                sg.PopupError(f'Error {e}')
        if event == 'Exit':
            break
        if event == sg.WIN_CLOSED:
            break
    window.Close()
    main()

def RestrictUser():
    """Create a Window to restrict user"""

   
    layout=[
        [sg.Text('')],
        [sg.Text('GangVPN', font=('Helvetica',42))],
        [sg.Text('Username to restrict:')],
        # [sg.Listbox(values=allUsers, key='name', size=(25,6), enable_events=True)],
        [sg.Text('Port:'),sg.Input(key="dest_ip", size=(15,1))],
        [sg.Text('userName:'),sg.Input(key="userName", size=(15,1))],
        [sg.Text('userId:'),sg.Input(key="userId", size=(15,1))],
        [sg.Text('puerto_dest:'),sg.Input(key="puerto_dest", size=(15,1))],
        [sg.Text('')],
        [sg.Button('Restrict Access',bind_return_key=True),sg.Button('Go Back')],
        [sg.Text('')]
    ]
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True,element_justification='c')
    
    while True:
        event, values = restricted_window.Read()
        if event=='Restrict Access':
            try:
                regla_nombre = values["userName"]
                id_usuario=values["userId"]
                dest_ip=values["dest_ip"]
                puerto_dest=["puerto_dest"]
                regla = RestriccionUsuario(regla_nombre, dest_ip,puerto_dest, id_usuario)
                vpn.agregar_regla(regla)
                sg.PopupOK('Access Restricted')
            except Exception as e:
                sg.PopupError(f'Error {e}')
        elif event=='Go Back':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    main()

def DeleteUser():
    """Create a Window for deleting users"""
    
    deleted = False
    layout=[
        [sg.Text('')],
        [sg.Text('GangVPN', font=('Helvetica',42))],
        [sg.Text('Username to delete:')],
        [sg.Text('userId:'),sg.Input(key="userId", size=(15,1))],
        [sg.Text('')],
        [sg.Button('Delete User',bind_return_key=True),sg.Button('Go Back')],
        [sg.Text('')]
    ]
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True,element_justification='c')
    
    while True:
        event, values = restricted_window.read()
        if event=='Delete User':
            try:
                id = values["userId"]
                vpn.eliminar_usuario(int(id))
                sg.PopupOK('User Deleted')
                deleted=True
                break
            except Exception as e:
                sg.PopupError(f'Error {e}')
        elif event=='Go Back':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    if deleted:
        DeleteUser()
    else:
        main()
#averiguar como pincha este
def RestrictVLAN():
    """Create a Window for VLAN restriction"""
    layout=[
        [sg.Text('')],
        [sg.Text('GangVPN', font=('Helvetica',42))],
        [sg.Text('Enter the rule name VLAN to restrict')],
        [sg.Input(key='rule_name',size=(35,1),enable_events=True)],
        [sg.Text('Enter the id_vlan')],
        [sg.Input(key='id_vlan',size=(35,1))],
        [sg.Text('Enter the dest_ip')],
        [sg.Input(key='dest_ip',size=(35,1))],
        [sg.Text('Enter the puerto_dest')],
        [sg.Input(key='puerto_dest',size=(35,1))],
        [sg.Text('')],
        [sg.Button('Restrict'), sg.Button('Return')],
        [sg.Text('')]
    ]
  
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True,element_justification='c')
    
    while True:
        event, values = restricted_window.Read()
        if event=='Restrict':
            try:
                rule_name = values["rule_name"]
                id_vlan = int(values["id_vlan"])
                dest_ip= values["dest_ip"]
                puerto_dest= int(values["puerto_dest"])
                regla = RestriccionVLAN(rule_name, dest_ip,int(puerto_dest), int(id_vlan))
                vpn.agregar_regla(regla)
               
                
                sg.PopupOK('Access Restricted')
            except:
                sg.PopupError("Invalid Input!")
        elif event=='Return':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    main()
def show_rules():
    vpn.mostrar_reglas()
    main()
def show_users():
    vpn.mostrar_usuarios()
    main()    


def main():

    """Main function of the program."""
    # Set up GUI layout and window

    sg.theme('LightBlue')
    sg.set_options(font=('Comic Sans MS',18))

    layout = [
        [sg.Text('')],
        [sg.Text('Gang Connection VPN', font=('Helvetica',30))],
        
        [sg.Text('')],
        [sg.Button('Start VPN')],
        [sg.Button('Stop VPN')],
        [sg.Button('Create User')],
        [sg.Button('Delete User')],
        [sg.Button('Restrict User')],
        [sg.Button('Restrict VLAN')],
        [sg.Button('Show Rules')],
        [sg.Button('Show Users')],
        [sg.Button('Exit')],
        [sg.Text("Sure & Fastest 😉",font=('Arial',14))],
        [sg.Text('')],
    ]
    
    window2 = sg.Window('VPN', layout, element_justification='c')
    
    window2.size = (400, 400)
    

    window2.Resizable = False
    while True:
        event, values = window2.read()
        if event == sg.WIN_CLOSED or event=='Exit' :
            window2.close()
            break
        if event =='Start VPN':
            vpn_thread = threading.Thread(target=vpn.ejecutar)
            vpn_thread.start()
        if event == 'Stop VPN':
            if (vpn_thread is None):
                continue
            vpn.parar()
            vpn_thread.join()
            vpn_thread = None
        if event == 'Create User':
            window2.close()
            CreateUser()
        if event == 'Restrict User':
            window2.close()
            RestrictUser()
        if event == 'Restrict VLAN':
            window2.close()
            RestrictVLAN()
        if event == 'Show Rules':
            window2.close()
            show_rules()
        if event == 'Show Users':
            window2.close()
            show_users()    
        if event == 'Delete User':
            window2.close()
            DeleteUser()
       
        


if __name__ == "__main__":
    main()
