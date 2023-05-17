import socket
import json


class SocketClient:
    def __init__(self, host="localhost", port="19999"):
        self.__host = host
        self.__port = port
        self.__sock = None

    def __connect(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.__host, self.__port)
        self.__sock.connect(server_address)

    def __close(self):
        if self.__sock:
            self.__sock.close()

    def test_socket(self, msg: dict):
        try:
            data = json.dumps(msg)
            self.__connect()
            self.__sock.sendall(bytes(data, "utf-8"))
            ret_msg = ""
            while True:
                resp = self.__sock.recv(4096)
                if not resp:
                    break
                ret_msg += resp.decode("utf-8")
            self.__close()
            return ret_msg
        except Exception as err:
            return str(err)
