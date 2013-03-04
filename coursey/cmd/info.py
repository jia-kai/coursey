# -*- coding: utf-8 -*-
# $File: info.py
# $Date: Mon Mar 04 23:09:48 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

import gevent

from coursey.cmd import command
from coursey.utils import fetch_page, Parser, print_table

def get_course_info(id_list):
    """:return: title, list(dict:field -> val)"""

    title = list()
    def get_onecourse(csid):
        rst = Parser(fetch_page({'m': 'rxSearch', 'p_kch': csid}))
        if not title:
            title.extend(rst.get_js_var('gridColumns'))
            del title[0]
            del title[-4:]
        ret = rst.get_js_var('gridData')
        for i in ret:
            del i[0]
            del i[-4:]
            for j in range(len(i)):
                if '<' in i[j]:
                    i[j] = i[j][i[j].find('>') + 1:]
                    i[j] = i[j][:i[j].find('<')]
        return ret

    rst = get_onecourse(id_list[0])
    greenlets = [gevent.spawn(get_onecourse, i) for i in id_list[1:]]
    for i in greenlets:
        i.join()
        rst.extend(i.value)

    return title, [{title[i]: val[i] for i in range(len(title))}
            for val in rst]


@command('info')
def get_course_info_by_file(csid_fin):
    """search for ren xuan ke; Arg: the path to the file containing the ids"""
    with open(csid_fin) as fin:
        csid = [i.strip() for i in fin.readlines()]
        csid = filter(bool, csid)

    title, val = get_course_info(csid)
    val = [[j[i] for i in title] for j in val]
    print_table([title] + val)
    
