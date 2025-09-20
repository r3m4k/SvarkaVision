# System imports
import socket

# External imports

# User imports


##########################################################

class PhotoReceiver:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.server: socket.socket = None

    def __del__(self):
        self.server.close()

    def _init_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)