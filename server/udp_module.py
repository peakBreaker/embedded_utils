#!/usr/bin/python3

import socket
from datetime import datetime
socket.setdefaulttimeout(1)


class udp_handler():
    "Class for the udp handler"
    def __init__(self, **kw):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the port
        self.server_address = ('0.0.0.0', kw['port'])
        self.sock.bind(self.server_address)
        self.start_time = "Started at :: " + datetime.now().isoformat(' ')
        self.last_incoming = None

        self.echo = input("Should I echo UDP requests? [Y/N] > ")
        self.echo = True if self.echo == 'Y' else False
        print("Echo is set to %s" % self.echo)
        print("Running UDP Handler with port %s" % str(kw['port']))

    def __repr__(self):
        return ("udp_handler module with server address: " +
                str(self.server_address) + " || echo is " + str(self.echo))

    def status_cb(self):
        "Gets the status of the module"
        if self.last_incoming is None:
            self.last_incoming = "No messages yet"
        return ("Up and running - " + self.start_time +
                " || Last msg :: " + self.last_incoming)

    def get_incoming(self):
        "Returns the first incoming udp msg"
        while True:
            # return "0000001"
            try:
                data, address = self.sock.recvfrom(4096)
                print(data)
                if data:
                    self.last_incoming = datetime.now().isoformat(' ')
                    if self.echo:
                        sent = self.sock.sendto(data, address)
                        sent = self.sock.sendto(data + "2", address)
                        sent = self.sock.sendto(data + "33", address)
                        print('echo %s bytes to %s thrice!' % (sent, address))
                    return str(data)
            except socket.timeout:
                return None
