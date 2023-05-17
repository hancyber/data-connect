import socket

from threading import Thread, Lock
from openopsdata.common import COMMON, logger
from openopsdata.gateway.gateway import Gateway
from openopsdata.aggregator import Aggregator


class GatewaySocket(Gateway):
    __HOST = "127.0.0.1"
    __PORT = 9999
    __BACKLOG = 10
    __BUFFER_SIZE = 1024
    __SHUTDOWN_MSG = "shutdown hgb aggregator"

    def __init__(self, config):
        super().__init__(config)
        sock_info = self._config[COMMON.CONFIG_SECTION_SOCKET()] \
            if COMMON.CONFIG_SECTION_SOCKET() in self._config else None
        self.__host = sock_info[COMMON.SOCKET_HOST()] \
            if sock_info and COMMON.SOCKET_HOST() in sock_info else self.__HOST
        self.__port = int(sock_info[COMMON.SOCKET_PORT()]) \
            if sock_info and COMMON.SOCKET_PORT() in sock_info else self.__PORT
        self.__backlog = int(sock_info[COMMON.SOCKET_BACKLOG()]) \
            if sock_info and COMMON.SOCKET_BACKLOG() in sock_info else self.__BACKLOG
        self.__buffer_size = int(sock_info[COMMON.SOCKET_BUFFER_SIZE()]) \
            if sock_info and COMMON.SOCKET_BUFFER_SIZE() in sock_info else self.__BUFFER_SIZE

        self.__lock = Lock()
        self.__clients = 0
        self.__shutdown = False
        self.__thread_list = []
        self.__is_wait = True
        self.__server_socket = None

    def __socket_handle(self, client_sock, address):
        with self.__lock:
            self.__clients += 1
            self.__shutdown = False

        logger.info("connected " + str(address))
        rev_data = client_sock.recv(self.__buffer_size)
        rev_msg = rev_data.decode()
        rev_msg_str = rev_msg.rstrip()
        logger.debug("received: " + rev_msg_str)
        if rev_msg_str == self.__SHUTDOWN_MSG:
            with self.__lock:
                self.__shutdown = True
        else:
            self._executor(msg=str(rev_msg_str), socket=client_sock)
            # msg_thread = Thread(target=msg_parser, kwargs={'msg': str(rev_msg_str)})
            # msg_thread.start()
        # client_sock.send(rev_msg.encode())
        # client_sock.close()

        with self.__lock:
            self.__clients -= 1
            self.__shutdown_check()

    # abnormal function
    def __shutdown_check(self):
        if self.__shutdown:
            if self.__clients == 0:
                # for thread in self.thread_list:
                #     if thread.is_alive():
                #         thread.join()
                self.__thread_list.clear()
                self.__is_wait = False
                logger.info("shutdown accepted")
                logger.info("server shutdown")
                self.__server_socket.close()
            else:
                self.__shutdown = False
                self.__is_wait = True
                logger.debug("shutdown rejected")

    def __socket_server(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__host, self.__port))
        self.__server_socket.listen(self.__backlog)
        logger.debug(str(self.__host) + ":" + str(self.__port) + " (" + str(self.__backlog) + ")")
        logger.info("hgb aggregator server start")

        while self.__is_wait:
            client_socket, address = None, None
            try:
                client_socket, address = self.__server_socket.accept()
            except ConnectionAbortedError as err:
                if not self.__is_wait and self.__shutdown:
                    logger.info("server closed")
                else:
                    logger.error(str(err))
            if self.__is_wait and client_socket and address:
                thread = Thread(target=self.__socket_handle, args=(client_socket, address))
                self.__thread_list.append(thread)
                thread.start()

    def _async_executor(self, executor: Aggregator, **kwargs):
        exec_thread = Thread(target=executor.execute)
        exec_thread.start()
        socket_client: socket = kwargs["socket"]
        socket_client.send(bytes("async detected, will be closed\r\n", encoding="utf-8"))
        socket_client.close()
        logger.debug("client closed")

    def _sync_executor(self, executor: Aggregator, **kwargs):
        rst, msg = executor.execute()

        socket_client: socket = kwargs["socket"]
        # socket_client.send(bytes("result: " + str(rst) + ", " + str(msg) + "\r\n", encoding="utf-8"))
        socket_client.send(bytes(str(msg), encoding="utf-8"))
        socket_client.close()
        logger.debug("client closed")

    def run(self):
        self.__socket_server()
