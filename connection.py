import subprocess
import time

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


    
a = "10.6.8.12"
b = "10.8.x.x"
print(is_ip_in_subnet(a, b))


""""
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
    
"""