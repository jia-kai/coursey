# -*- coding: utf-8 -*-
# $File: select.py
# $Date: Tue Mar 05 13:01:35 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>


from coursey.config import SEMESTER, WEBPAGE_ENCODING, SLEEP_TIME, SLEEP_DELTA
from coursey.cmd import command
from coursey.cmd.info import get_course_info
from coursey.utils import fetch_page, Parser

from collections import namedtuple
from datetime import datetime
from random import random
import time
import sys

Descriptor = namedtuple('Descriptor', ['save', 'id_field'])

course_desc = {
    'bx': Descriptor('saveBxKc', 'p_bxk_id'),
    'xx': Descriptor('saveXxKc', 'p_xxk_id'),
    'rx': Descriptor('saveRxKc', 'p_rx_id')
}

def _get_token():
    return Parser(fetch_page()).get_input_val('token')


@command('select')
def select(type, csid, csnum):
    """args: type, course_id, course_num; type must be one of (bx, rx, xx)"""
    token = _get_token()
    desc = course_desc[type]
    rst = Parser(fetch_page({'m': desc.save,
        desc.id_field: '{0};{1};{2};'.format(SEMESTER, csid, csnum),
        'token': token
        }))
    rst = rst.get_func_arg('showMsg')
    print rst
    return rst


@command('try_select')
def try_select(*args):
    """:args: id, num, id, num, ... (only renxuan supported)"""
    assert args and len(args) % 2 == 0
    courses = [(args[i], args[i + 1]) for i in range(0, len(args), 2)]

    for i in courses:
        select('rx', i[0], i[1])

    while True:
        if not courses:
            print 'done, press anykey to exit'
            raw_input()
            sys.exit()

        remains = [0] * len(courses)
        names = [None] * len(courses)
        for i in get_course_info([i[0] for i in courses])[1]:
            for j in range(len(courses)):
                if i[u'课程号'] == courses[j][0] and \
                        i[u'课序号'] == courses[j][1]:
                    remains[j] = int(i[u'课余量'])
                    names[j] = i[u'课程名']
        print datetime.today(),
        for i in zip(courses, names):
            print u'({0}, {1}, {2})'.format(i[0][0], i[0][1], i[1]),
        print remains
        
        to_del = []
        for i in range(len(courses)):
            if remains[i]:
                rst = select('rx', courses[i][0], courses[i][1])
                if u'冲突' in rst:
                    to_del.append(i)

        to_del.reverse()
        for i in to_del:
            del courses[i]


        time.sleep(SLEEP_TIME + 2 * (random() - 0.5) * SLEEP_DELTA)


def _get_remains(courses):
    """:param courses: list of (id, num) pair"""
    return map(int, [i[u'课余量'] for i in val])
