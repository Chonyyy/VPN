import socket

def vpn_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8888))  # Coneectar al servidor VPN en localhost

    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")

    credentials = f"{username}:{password}"
    client.send(credentials.encode())

    response = client.recv(1024).decode()
    print(f"Respuesta del servidor: {response}")

    client.close()

if __name__ == "__main__":
    vpn_client()