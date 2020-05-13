#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    server
#
#    ----------------------------------------------------------------------
#    Copyright © 2020  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import keyboard
import sys
from getpass import getpass
from pprint import pprint
from select import select
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, SHUT_RDWR, error, socket
from sys import stdout
from threading import Thread
from time import sleep

from .config import Config

class Server:

    config = Config()
    char_queue = []

    def __init__(self, port, passphrase="", verbose=False):
        self.passphrase = passphrase
        self.verbose = verbose

        if verbose:
            print("Running on port {}".format(port))

        # Opening socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(('', port))
        self.socket.listen(5)

        # Running queue processing loop
        t = Thread(target=self.process_queue, args = ())
        t.daemon = True
        t.start()

        # Running socket loop
        self.loop()
    
    def loop(self):
        a = [self.socket]
    
        while True:
            selection = select(a, [], [])[0]
            for b in selection:
                if b is a[0]:
                    out = b.accept()
                    a.append(out[0])
                else:
                    try:
                        c = b.recv(1 << 12)
                        if c:
                            self.char_queue.append(c)
                        if not c:
                            b.shutdown(SHUT_RDWR)
                            a.remove(b)
                    except error:
                        print("exception")
                        b.shutdown(SHUT_RDWR)
                        b.close()
                        a.remove(b)

    def process_queue(self):
        while True:
            if self.char_queue:
                data = str(self.char_queue[0].decode('utf-8'))
                #print(data)
                try:
                    gpg = self.config.gpg_new()
                    #print(self.passphrase)
                    try:
                        decrypted_data = gpg.decrypt(data, passphrase=self.passphrase)
                    except Exception as e:
                        print(e)
                    if self.verbose:
                        print("decrypting")
                        #print(decrypted_data.status)
                        #print(decrypted_data.stderr)
                        print(decrypted_data)
                        #stdout.flush()
                    keyboard.write(decrypted_data.data.decode('utf-8'))
                    del self.char_queue[0]
                except ValueError as e:
                    #print(e)
                    pass
            if self.verbose:
                sleep(2)
            else:
                sleep(0.5)


if __name__ == '__main__':
    main()
