#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: main.py
# $Date: Mon Mar 04 23:52:05 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from gevent import monkey
monkey.patch_all()

from coursey.cmd import command

import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'usage: {0} <command>\nAvailable commands:\n'.format(sys.argv[0])
        for k, v in command.cmd_map.iteritems():
            print k + ':', v.doc
        sys.exit()
    command.cmd_map[sys.argv[1]].invoke(*sys.argv[2:])
