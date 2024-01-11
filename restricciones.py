from abc import ABC, abstractmethod

class Usuario:
    def __init__(self, usuario: str, contrasenna: str, id_vlan: int):
        self.usuario = usuario
        self.contrasenna = contrasenna
        self.id_vlan = id_vlan
        self.id = 0

    def diccionario_a_objeto(dict):
        usuario = dict['usuario']
        contrasenna = dict['contrasenna']
        id_vlan = dict['id_vlan']

        value = Usuario(usuario, contrasenna, id_vlan)
        value.id = dict['id']

        return value

class Paquete:
    def __init__(self, usuario: str, contrasenna: str, dest_ip: str, puerto_dest: int, data: str):
        self.usuario = usuario
        self.contrasenna = contrasenna
        self.dest_ip = "localhost"
        self.puerto_dest = 5002
        self.data = data

    def diccionario_a_objeto(dict):
        usuario = dict['usuario']
        contrasenna = dict['contrasenna']
        dest_ip = dict['dest_ip']
        puerto_dest = dict['puerto_dest']
        data = dict['data']

        value = Paquete(usuario, contrasenna, dest_ip, puerto_dest, data)
        return value

class Regla(ABC):
    def __init__(self, nombre, tipo, ip, puerto, e_id, ):
        self.nombre = nombre
        self.tipo = tipo
        self.ip = '127.0.0.1' if ip == 'localhost'else ip
        self.puerto = puerto
        self.e_id = e_id
        self.id = 0

    def check(self, usuario: Usuario, paquete: Paquete):
        pass

class RestriccionVLAN(Regla):
    def __init__(self, nombre, ip, puerto, id_vlan):
        super().__init__(nombre, 0 ,ip, puerto, id_vlan)
        self._id_vlan = id_vlan

    def check(self, usuario: Usuario, paquete: Paquete) -> bool:
        dest_ip = '127.0.0.1' if paquete.dest_ip == 'localhost' else paquete.dest_ip
        return usuario.id_vlan != self._id_vlan or dest_ip != self.ip or self.puerto != paquete.puerto_dest

    def diccionario_a_objeto(dict):
        nombre = dict['nombre']
        ip = dict['ip']
        puerto = dict['puerto']
        id_vlan = dict['e_id']

        value = RestriccionVLAN(nombre, ip, puerto, id_vlan)
        return value

class RestriccionUsuario(Regla):
    def __init__(self, nombre, ip, puerto, usuario_id):
        super().__init__(nombre, 1, ip, puerto, usuario_id)
        self.__usuario_id = usuario_id

    def check(self, usuario: Usuario, paquete: Paquete) -> bool:
        dest_ip = '127.0.0.1' if paquete.dest_ip == 'localhost' else paquete.dest_ip
        return usuario.id != self.__usuario_id or dest_ip != self.ip or self.puerto != paquete.puerto_dest

    def diccionario_a_objeto(dict):
        nombre = dict['nombre']
        ip = dict['ip']
        puerto = dict['puerto']
        usuario_id = dict['e_id']

        value = RestriccionUsuario(nombre, ip, puerto, usuario_id)
        return value
