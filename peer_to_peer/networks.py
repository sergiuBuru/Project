"""
SIG Blockchain
Peer-to-Peer Node class
"""

import threading
import socket
import json


def get_ip():
    """
    Gets the IP Address

    :returns: ip address in string form
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.google.com', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


class Node:

    def __init__(self, port=9001):
        """
        Constructor for Node class.

        :param self: references itself
        :param port: integer port number, defaulted to 9001
        """
        self.ip = get_ip()
        self.port = port
        self.sockets = []
        self.server = socket.socket()
        self.server.bind(('', self.port))
        self.edges = set()

        self.integrated = threading.Event()
        self.integrated.clear()
        self.new_message = threading.Event()
        self.new_message.clear()

    def listen(self):
        """
        Listens for connections

        :param self: reference to self
        """
        self.server.listen()
        print("Listening for connections...")
        accept_conns_thread = threading.Thread(
            target=self.accept_conns, name="Accept Connections", daemon=True)
        accept_conns_thread.start()

    def handler(self, conn, addr):
        """
        Handles incoming communication

        :param self: reference to self
        :param conn: socket object
        :param addr: string, int tuple representing address of other node
        :raises ConnectionError: thrown when connection has been severed
        """
        while True:
            try:
                msg = conn.recv(1024) # <-- blocking call
                if not msg:
                    raise ConnectionError
                print("\n<< " + msg.decode())  # print out the message
                self.new_message.set()
                self.broadcast(msg, conn)
            except (ConnectionError, OSError):
                print("\n>> " + addr[0] + " has disconnected.")
                self.sockets.remove(conn)
                self.edges.remove(addr[0])
                conn.close()  # remove the socket from the list
                break

    def accept_conns(self):
        """
        Accepts incoming connections

        :param self: reference to self
        """
        while True:
            try:
                conn, addr = self.server.accept()  # <-- blocking call
                print("\n" + addr[0] + " has connected.")
                self.sockets.append(conn)
                self.integrated.set()
                self.edges.add(addr[0])
                handler_thread = threading.Thread(
                    target=self.handler, name="Message Handler", args=(conn, addr), daemon=True)
                handler_thread.start()  # start the handler thread
            except OSError:
                pass
            except KeyboardInterrupt:
                self.disconnect()
                return

    def check_edges(self, ip):
        """
        Checks to see if there exists a connection to this ip

        :param self: reference to self
        :param ip: string that represents the ip address
        """
        print("Checking for edges...")
        for e in self.edges:
            if ip == e:
                return True
        return False

    def connect_to_peer(self, addr):
        """
        Connects to the peer at the address specified

        :param self: reference to self
        :param addr: string, int tuple representing the ip and port
        """
        if self.check_edges(addr[0]):
            print("Existing edge to %s" % (addr[0]))
            return
        try:
            conn = socket.socket()
            print("Attempting to connect to %s on port %d..." % (addr))
            conn.connect(addr)
            self.sockets.append(conn)
            self.integrated.set()
            self.edges.add(addr[0])
            handler_thread = threading.Thread(
                target=self.handler, name="Message Handler", args=(conn, addr), daemon=True)
            handler_thread.start()  # start the handler thread
        except ConnectionError:
            print("Failed to connect to %s" % (addr[0]))
            conn.close()

    def broadcast(self, message, exc=None):
        """
        Broadcasts a message to all connections, with one possibly excluded.

        :param self: reference to self
        :param message: byte string message to be sent
        :param exc: socket object defaulted to None, will not broadcast to it
        """
        [s.send(message) for s in self.sockets if not s == exc]

    def disconnect(self):
        """
        Shuts down all sockets.

        :param self: reference to self
        """
        [s.close() for s in self.sockets]
        self.server.close()
