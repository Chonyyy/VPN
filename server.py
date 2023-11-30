import socket
import threading

# usuarios y contraseñas | poner  en una DB si deseas , to esa weba la haces tu 
users = {
    "user1": "password1",
    "user2": "password2",
}

# Direcciones IP virtuales | lo de  arriba x2
ip_assignments = {
    "user1": "10.6.1.1",
    "user2": "10.6.2.1",
}

# Servidor VPN
def vpn_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8888))
    server.listen(5)
    print("Servidor VPN escuchando en el puerto 8888...")

    while True:
        client, addr = server.accept()
        print(f"Conexión entrante desde {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

# Manejo de clientes
def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    username, password = request.split(':')
    
    if authenticate(username, password):
        virtual_ip = assign_virtual_ip(username)
        client_socket.send(virtual_ip.encode())
    else:
        client_socket.send("Autenticación fallida".encode())
    
    client_socket.close()

# Autenticacion de usuarios
def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    return False

# IP virtual
def assign_virtual_ip(username):
    if username in ip_assignments:
        return ip_assignments[username]
    return "IP no asignada"

if __name__ == "__main__":
    vpn_server()