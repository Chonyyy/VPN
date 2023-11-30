import subprocess
import time

# Iniciar el servidor VPN en un proceso separado
server_process = subprocess.Popen(["python3", "server.py"])

# Esperar unos segundos para asegurarse de que el servidor VPN este activo
time.sleep(20)

# Número de clientes que deseas conectar
num_clients = 2

# Iniciar clientes VPN en procesos separados
for i in range(num_clients):
    client_process = subprocess.Popen(["python3", "client.py"])
    time.sleep(20)  # Esperar unos segundos entre la conexión de cada cliente 
    
