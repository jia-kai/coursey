# -*- coding: utf-8 -*-
# $File: select.py
# $Date: Wed Feb 27 19:59:03 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>


from coursey.config import SEMESTER, WEBPAGE_ENCODING
from coursey.cmd import command
from coursey.utils import fetch_page, Parser

from collections import namedtuple

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
    print rst.get_func_arg('showMsg')

