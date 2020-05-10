# -*- coding: utf-8 -*-

#    util.py
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

#from ast import literal_eval
from copy import deepcopy as cp
from os import makedirs, umask
from pickle import dump
from pickle import load as pickle_load
from re import IGNORECASE, compile, escape, sub
from threading import BoundedSemaphore, Thread

threadLimiter = BoundedSemaphore(4)

class MyThread(Thread):

    def run(self):
        threadLimiter.acquire()
        try:
            super(MyThread, self).run()
        finally:
            threadLimiter.release()

class EntitySet(list):
    def __init__(self, triplet=False):
        self.triplet = triplet

    def add(self, element):
        if element['URI']:
            same_URI = element['URI'] in (v['URI'] for v in self)
            if not same_URI:
                self.append(element)
        else:
            if not element["Label"] in (v["Label"] for v in self):
                self.append(element)
            else:
                for v in self:
                    if element["Label"] == v["Label"]:
                        v = element

def save(variable, path):
    """Save variable on given path using Pickle

    Args:
        variable: what to save
        path (str): path of the output
    """
    with open(path, 'wb') as f:
        dump(variable, f)

def load(path):
    """Load variable from Pickle file

    Args:
        path (str): path of the file to load

    Returns:
        variable read from path
    """
    with open(path, 'rb') as f:
        variable = pickle_load(f)
    return variable

def chmod_recursively(path, mode=0o755):
    from os import chmod, walk
    from os.path import join
    chmod(path, mode)
    for root, dirs, files in walk(path):  
      for d in dirs:  
        current_path = join(root, d)
        print(current_path)
        chmod(current_path, mode)
      for f in files:
        current_path = join(root, f)
        print(current_path)
        chmod(current_path, mode)

def mkdirs(newdir, mode=0o755):
    try:
        original_umask = umask(0)
        makedirs(newdir, mode)
    except OSError:
        pass
    finally:
        umask(original_umask)
