#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    stear-keyboard
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

from argparse import ArgumentParser
from setproctitle import setproctitle

from .client import Client
from .server import Server

name = "stear-keyboard"
version = "0.1"

setproctitle(name)

def main():

    parser = ArgumentParser(description="Remote keybord for the DIY Stear Prime smartphone")

    # Parser args
    verbose = {'args': ['--verbose'],
               'kwargs': {'dest': 'verbose',
                          'action': 'store_true',
                          'default': False,
                          'help': 'extended output'}}

    version = {'args': ['--version'],
               'kwargs': {'dest': 'version',
                          'action': 'store_true',
                          'default': False,
                          'help': 'print version'}}

    parser.add_argument(*verbose['args'], **verbose['kwargs'])
    parser.add_argument(*version['args'], **version['kwargs'])

    command = parser.add_subparsers(dest="command")

    client = command.add_parser('client', help="Client mode (to be run on the device sharing the keyboard)")

    # Client args

    email = {'args': ['email'],
             'kwargs': {'nargs': 1,
                        'action': 'store',
                        'help': "email whose PGP decryption key is present on server device"}}

    host = {'args': ['host'],
            'kwargs': {'nargs': '?',
                       'action': 'store',
                       'default': '127.0.0.1',
                       'help': "address of the server"}}

    port = {'args': ['--port'],
            'kwargs': {'nargs': 1,
                       'action': 'store',
                       'default': [15400],
                       'help': "port on which the server is listening (default: 15400)"}}


    client.add_argument(*email['args'], **email['kwargs'])
    client.add_argument(*host['args'], **host['kwargs'])
    client.add_argument(*port['args'], **port['kwargs'])

    server = command.add_parser('server', help="Server mode (to be run on the device receiving input")

    # Server args

    passphrase = {'args': ['passphrase'],
                  'kwargs': {'nargs': '?',
                             'action': 'store',
                             'default': '',
                             'help': ("passphrase of the PGP key for the email selected"
                                      "by the client")}}

    server.add_argument(*passphrase['args'], **passphrase['kwargs'])
    server.add_argument(*port['args'], **port['kwargs'])

    args = parser.parse_args()

    if args.verbose:
        print(args)

    if args.version:
        print(version)

    if args.command == "client":
        client = Client(email=args.email[0],
                        host=args.host,
                        port=args.port[0],
                        verbose=args.verbose)
        
    elif args.command == "server":
        server = Server(port=args.port[0],
                        passphrase=args.passphrase,
                        verbose=args.verbose)
        print(server)

    else:
        parser.print_usage()
