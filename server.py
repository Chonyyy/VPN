import socket
import threading
import logging
# usuarios y contraseñas 
users = {
    "user1": "password1",
    "user2": "password2",
}

# VLANs de los usuarios
user_vlans = {
    "user1": 1,
    "user2": 2,
}

# Direcciones IP virtuales 
ip_assignments = {
    "user1": "10.6.1.1",
    "user2": "10.6.2.1",
}

# Servidor VPN
def vpn_server(protocol_type="tcp"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8888))
    server.listen(5)
    print(f"Servidor VPN escuchando en el puerto 8888 (protocolo {protocol_type})...")

    while True:
        client, addr = server.accept()
        print(f"Conexión entrante desde {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client, ))
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
     
#Creacion de un usuario
def create_user(name, password, vlan_id):
    users[name] = password
    user_vlans[name] = vlan_id
    ip_assignments[name] = "10.6.1.1"

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

#Verifica si el IP dado pertenece a la subred dada.
def is_ip_in_subnet(ip, subnet):
   
    a = ip.split(".")
    b = subnet.split(".")

    for i in range(0,3):
        if b[i] == 'x':
            return True
        
        if a[i] == b[i]:          
            continue
        
        if a[i] != b[i]: 
            return False

# Restricción de VLANs
def restrict_vlan(vlan_id, ip_network):
    for user_id, user_vlan in user_vlans.items():
        if user_vlan == vlan_id:
            if(is_ip_in_subnet(ip_assignments[user_id],ip_network)):
                ip_assignments[user_id] = "IP bloqueada"

# Restricción de usuarios
def restrict_user(user_id, ip_network):
    if(is_ip_in_subnet(ip_assignments[user_id],ip_network)):
                ip_assignments[user_id] = "IP bloqueada"

# Actualizar el log
def write_log(log_entry):
    logging.basicConfig(filename='vpn_server.log', format='%(asctime)s %(message)s', level=logging.INFO)
    logger = logging.getLogger()
    logger.info(log_entry)

if __name__ == "__main__":
    protocol_type = input("Protocolo de comunicación (tcp/udp): ")
    vpn_server(protocol_type)
    
    
