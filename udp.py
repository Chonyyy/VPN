import socket
import struct

class UDP:
    def __init__(self, ip, puerto):
        self.__stop = False
        self._ip = '127.0.0.1' if ip == 'localhost' else ip
        self._port = puerto
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.__s.bind((self._ip, self._port))
        self.__s.setblocking(False)

    def enviar(self, data, dest_addr):
        
        s = self.__s
        dest_ip, puerto_dest = dest_addr
        dest_ip = '127.0.0.1' if dest_ip == 'localhost' else dest_ip

        data = data.encode('utf-8')

        length = 8+len(data)
        checksum = 0

        udp_data = struct.pack("!HHHH", self._port,
                               puerto_dest, length, checksum) + data

        checksum = UDP.__calculate_checksum(self._ip, dest_ip, udp_data)
        udp_header = struct.pack('!HHHH', self._port,
                                 puerto_dest, length, checksum)

        s.sendto(udp_header + data, (dest_ip, puerto_dest))

        print(f'UDP data sent to {dest_ip}:{puerto_dest}\n')

    def ejecutar(self):
        self.__stop = False
        s = self.__s

        while not self.__stop:
            try:
                data, src_addr = s.recvfrom(1024)
                p = False

                udp_header = data[20:28]
                udp_header = struct.unpack('!HHHH', udp_header)

                src_port = udp_header[0]
                puerto_dest = udp_header[1]
                length = udp_header[2]
                checksum = udp_header[3]

                if (puerto_dest != self._port):
                    continue

                sender_ip, _ = src_addr

                zero_checksum_header = (data[20:28])[:6] + \
                    b'\x00\x00' + (data[20:28])[8:]
                calculated_checksum = UDP.__calculate_checksum(
                    sender_ip, self._ip, zero_checksum_header + data[28:])

                print(f'UDP data received from {sender_ip}:{puerto_dest}')

                if checksum != calculated_checksum:
                    print('Corrupted data\n')
                else:
                    data = data[28:].decode('utf-8')
                    print(f'Data: {data}')
                    print(f'Length: {length}, Checksum: {checksum}\n')

                    p = True

                if p:
                    yield data
            except BlockingIOError:
                #se queda aqui infinitamente
                continue

    def parar(self):
        self.__stop = True

    def __calculate_checksum(source_ip, dest_ip, data):
        source_ip = socket.inet_aton(source_ip)
        dest_ip = socket.inet_aton(dest_ip)

        packet = struct.pack('!4s4sHH', source_ip,
                             dest_ip, len(data), 0) + data

        checksum = 0
        for i in range(0, len(packet), 2):
            if i + 1 < len(packet):
                checksum += (packet[i] << 8) + packet[i+1]
            else:
                checksum += packet[i]
            while checksum >> 16:
                checksum = (checksum & 0xFFFF) + (checksum >> 16)

        checksum = ~checksum

        return checksum & 0xFFFF
