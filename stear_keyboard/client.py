#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    client
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

from socket import create_connection, error, gaierror
from time import sleep
from getpass import getpass
from gnupg import GPG
from os.path import join as path_join
from threading import Thread
from sys import exit as sys_exit
import sys

from .config import Config
from .getch import Getch

class Client:
    
    config = Config()
    getch = Getch()
    #gpg = GPG()
    char_queue = []

    def __init__(self, email, host='127.0.0.1', port=15400, verbose=False, debug=True):

        self.gpg = self.config.gpg

        self.debug = debug
        self.email = self.config.get_fingerprint()
        self.host = host
        self.port = port
        self.verbose = verbose

        # Connecting to the server
        #self.connect()

        # Running queue processing loop
        t = Thread(target=self.process_queue, args = ())
        t.daemon = True
        t.start()

        # Running getch loop
        self.loop()

    def send(self, data):
        try:
            remote = create_connection((self.host, self.port))
            remote.sendall(str(data).encode())
            return remote
        except gaierror:
            print('Could not find host {}'.format(self.host))
        except error:
            print('Could not connect to host {}'.format(self.host))


    def process_queue(self):
        while True:
            if self.char_queue:

                # Eventually group chars
                if len(self.char_queue) > 1:
                    self.char_queue = ["".join(self.char_queue)]
                
                payload = self.char_queue[0]

                # Encrypt data
                encrypted_data = self.gpg.encrypt(payload, self.email)

                # Send
                try:
                    if self.verbose:
                        print("sending {}".format(payload))
                        print(encrypted_data)
                        sys.stdout.flush()
                    if self.debug:
                        print(encrypted_data)
                        sys.stdout.flush()
                    connection = self.send(encrypted_data)
                    #connection.sendall(str(encrypted_data).encode())
                    del self.char_queue[0]
                    del connection
                except Exception as e:
                    print(e)
                    sys.stdout.flush()
                    #self.connect()
            sleep(1)

    def loop(self):
        while True:
            try:
                char = self.getch()
                self.char_queue.append(char)
            except KeyboardInterrupt as e:
                print("keyboardinterrupt")
                sys_exit(1)

if __name__ == "__main__":
    print("Install the package.")
