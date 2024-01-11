import os
import json
from udp import UDP
from restricciones import RestriccionUsuario, RestriccionVLAN, Usuario,Paquete, Regla

class VPN:
    def __init__(self, protocolo:UDP) -> None:
        self._usuarios = VPN.leer_usuarios()
        self._reglas = VPN.leer_reglas()
        self.protocolo = protocolo

    def crear_usuario(self, usuario: Usuario):
        if any(usuario.usuario == i.usuario for i in self._usuarios):
            print('Usuario registrado\n')
            return

        usuario.id = len(self._usuarios)
        self._usuarios.append(usuario)
        self.guardar_usuarios()
        print('Usuario registrado\n')

    def eliminar_usuario(self, usuario_id: int):
        if usuario_id < 0 or usuario_id >= len(self._usuarios):
            print('Usuario no encontrado\n')
            return

        nuevos_usuarios = []
        ind = 0

        for i in self._usuarios:
            if i.id != usuario_id:
                i.id = ind
                ind += 1

                nuevos_usuarios.append(i)

        self._usuarios = nuevos_usuarios
        self.guardar_usuarios()

        print('Usuario eliminard\n')

    def ejecutar(self):
        print('VPN iniciado\n')

        for i in self.protocolo.ejecutar():
            try:
                paquete = Paquete.diccionario_a_objeto(json.loads(i))
                self.solicitud(paquete)
            except:
                continue

    def parar(self):
        self.protocolo.parar()
        print('VPN parado\n')

    def agregar_regla(self, regla: Regla):
        
        if any(regla.nombre == i.nombre for i in self._reglas):
            print('Ya existe una regla con ese nombre\n')
            return

        regla.id = len(self._reglas)
        self._reglas.append(regla)
        self.guardar_reglas()
        print('Regla agregada\n')

    def mostrar_reglas(self):
        for i in self._reglas:
            tipo = 'VLAN Restriction' if i.tipo == 0 else 'Usuario Restriction'
            e_id = f'id_vlan: {i.e_id}' if i.tipo == 0 else f'usuario_id: {i.e_id}'
            print(
                f'Id: {i.id} Nombre: {i.nombre} Tipo: {tipo} {e_id} ip: {i.ip} puerto: {i.puerto}')
        print()

    def eliminar_regla(self, regla_id: int):
        if regla_id < 0 or regla_id >= len(self._reglas):
            print('Regla no encontrada\n')
            return

        nuevas_reglas = []
        ind = 0

        for i in self._reglas:
            if i.id != regla_id:
                i.id = ind
                ind += 1
                nuevas_reglas.append(i)

        self._reglas = nuevas_reglas
        self.guardar_reglas()

        print('Regla eliminada\n')

    def mostrar_usuarios(self):
        for i in self._usuarios:
            print(
                f'Id: {i.id} Usuario: {i.usuario} Contrasenna: {i.contrasenna} Id_VLAN: {i.id_vlan}')
        print()

    def solicitud(self, paquete: Paquete):
        usuario = next(
            (i for i in self._usuarios if i.usuario == paquete.usuario and i.contrasenna == paquete.contrasenna), None)

        if usuario is None:
            print('Usuario no encontrado\n')
            return

        for i in self._reglas:
            if not i.check(usuario, paquete):
                print(f'Regla {i.nombre} blocked\n')

                return

        self.protocolo.enviar(paquete.data, (paquete.dest_ip, paquete.puerto_dest))

    def leer_usuarios():
        path: str = 'data/usuarios.json'

        if not os.path.exists(path):
            return []
        try:
            file = open(path, 'r')
            data = json.load(file)
            file.close()

            return [Usuario.diccionario_a_objeto(i) for i in data]
        except:
            return []

    def guardar_usuarios(self):
        path: str = 'data/usuarios.json'

        file = open(path, 'w+')
        json.dump(self._usuarios,  file, default=lambda o: o.__dict__)
        file.close()

    def leer_reglas():
        path: str = 'data/reglas.json'

        if not os.path.exists(path):
            return []

        try:
            file = open(path, 'r')
            data = json.load(file)
            file.close()

            reglas = []
            for i in data:
                if i['tipo'] == 0:
                    reglas.append(RestriccionVLAN.diccionario_a_objeto(i))
                else:
                    reglas.append(RestriccionUsuario.diccionario_a_objeto(i))

            return reglas
        except:
            return []

    def guardar_reglas(self):
        path: str = 'data/reglas.json'

        file = open(path, 'w+')
        json.dump(self._reglas,  file, default=lambda o: {
            'nombre': o.nombre,
            'tipo': o.tipo,
            'ip': o.ip,
            'puerto': o.puerto,
            'e_id': o.e_id
        })
        file.close()

