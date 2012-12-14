#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: main.py
# $Date: Fri Dec 14 18:03:50 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from coursey.cmd import command

import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        for k, v in command.cmd_map.iteritems():
            print k, ':', v.doc
        sys.exit()
    command.cmd_map[sys.argv[1]].invoke(*sys.argv[2:])
