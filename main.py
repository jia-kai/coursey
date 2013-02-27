#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: main.py
# $Date: Wed Feb 27 19:34:06 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from coursey.cmd import command

import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'usage: {0} <command>\nAvailable commands:\n'.format(sys.argv[0])
        for k, v in command.cmd_map.iteritems():
            print k + ':', v.doc
        sys.exit()
    command.cmd_map[sys.argv[1]].invoke(*sys.argv[2:])
