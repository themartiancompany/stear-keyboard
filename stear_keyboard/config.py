# -*- coding: utf-8 -*-

#    Config
#
#    ----------------------------------------------------------------------
#    Copyright © 2018,2019,2020  Pellegrino Prevete
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


from appdirs import *
from os import chmod, environ, mkdir, sep
from os.path import abspath, dirname, exists, join
from re import sub
from shutil import rmtree as rm
import gnupg

from .util import mkdirs

class Config:
    """Configuration class.

    Attributes:
        exec_path (str): path where the class resides;
        appname (str): name of the app (stear_keyboard).
        dirs (dict): paths of cache, data, config directories
    """

    exec_path = dirname(abspath(__file__))

    appname = "stear-keyboard"
    appauthor = "Pellegrino Prevete"
    dirs = {'data':user_data_dir(appname, appauthor),
            'config':user_config_dir(appname, appauthor),
            'cache':user_cache_dir(appname, appauthor)}

    debug = False

    def __init__(self, debug=True):
        self.debug = debug
        self.set_dirs()
        self.set_gpg()
        if not exists(join(self.dirs['config'], "config.pkl")):
            self.data = {}
        else:
            self.data = load(str(join(self.dirs['config'], "config.pkl")))

    def set_dirs(self):
        """Make user dirs for stear_keyboard
        """
        for dir_type, path in self.dirs.items():
            mkdirs(path)
            if dir_type == 'config': #and not exists(join(path, 'pywikibot')):
                mkdirs(join(path, 'gnupg'), mode=0o700)

    def gpg_new(self):
        return gnupg.GPG(gnupghome=join(self.dirs['config'], 'gnupg'), use_agent=True)

    def set_gpg(self):
        self.gpg = self.gpg_new()

        if not self.gpg.list_keys():
            key_input = { 'name_email': 'stearkeyboard@arcipelago.ml',
                          'expire_date': '2022-04-01',
                          'key_type': 'RSA',
                          'key_length': 1024,
                          'key_usage': 'encrypt,sign,auth',
                          'passphrase': 'test'}
            gnupg_key_input = self.gpg.gen_key_input(**key_input)
            key = self.gpg.gen_key(gnupg_key_input)
            ascii_armored_public_keys = self.gpg.export_keys(key.fingerprint)
            ascii_armored_private_keys = self.gpg.export_keys(
                keyids=key.fingerprint,
                secret=True,
                passphrase='test',
            )
            import_result = self.gpg.import_keys(ascii_armored_public_keys + ascii_armored_private_keys)
            for k in import_result.results:
                print(k)
            print(("Remember to copy the GPG configuration directory"
                   "(~/.config/stear-keyboard/gnupg) on server, too"))

    def get_fingerprint(self):
        return self.gpg.list_keys()[0]['fingerprint']

    def save(self):
        save(self.data, join(self.dirs['config'], 'config.pkl'))

