# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Fri Dec 14 17:13:14 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from pkgutil import walk_packages

class command(object):
    cmd_map = dict()

    name = None
    func = None
    doc = None

    def __init__(self, name, doc = None):
        self.name = name
        self.cmd_map[name] = self
        self.doc = doc

    def __call__(self, func):
        self.func = func
        if self.doc is None:
            self.doc = func.__doc__

    def invoke(self, *args, **kargs):
        return self.func(*args, **kargs)


for loader, module_name, is_pkg in walk_packages(__path__, __name__ + '.'):
    __import__(module_name, globals(), locals(), [], -1)

