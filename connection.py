import subprocess
import time

# Iniciar el servidor VPN en un proceso separado
server_process = subprocess.Popen(["python3", "server.py"])

# Esperar unos segundos para asegurarse de que el servidor VPN este activo (chony ajusta segun recursos de la maquina)
time.sleep(2)

# Número de clientes que deseas conectar
num_clients = 2

# Iniciar clientes VPN en procesos separados
for i in range(num_clients):
    client_process = subprocess.Popen(["python3", "client.py"])
    time.sleep(60)  # Esperar unos segundos entre la conexión de cada cliente - tienes q insertar user y contra para acceder al server vpn
    
