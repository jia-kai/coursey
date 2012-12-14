# -*- coding: utf-8 -*-
# $File: utils.py
# $Date: Fri Dec 14 22:11:29 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

import urllib
import urllib2
import os
import re
import json
import unicodedata
from coursey.config import URL, WEBPAGE_ENCODING, SEMESTER

cookie = os.getenv('coursey_cookie')

if not cookie:
    raise ValueError('Please set the coursey_cookie environment variable')

def fetch_page(data, is_post = True):
    data['p_xnxq'] = SEMESTER
    data = urllib.urlencode(data)
    if is_post:
        request = urllib2.Request(URL, data)
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        request.add_header("Content-Length", str(len(data)))
    else:
        request = urllib2.Request(URL + '?' + data)
    request.add_header('Cookie', cookie)
    request.add_header('Origin', 'http://zhjwxk.cic.tsinghua.edu.cn')
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) ' +
            'AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 ' +
            'Safari/537.11')

    return urllib2.urlopen(request).read()


class Parser(object):
    def __init__(self, webpage):
        webpage = webpage.decode(WEBPAGE_ENCODING)
        if u'用户登录超时' in webpage:
            raise RuntimeError('login timed out')
        self.lines = webpage.split('\n')

    def get_input_val(self, name):
        r = re.compile(r"""<input.*name=['"]{}['"].*value=['"]([^'"]*)['"]""".
                format(name))
        for l in lines:
            m = r.search(l)
            if m:
                return m.group(1)

    def get_js_var(self, name):
        rstart = re.compile(r"""var.*{}.*=.*\[""".format(name))
        rend = re.compile(r"""\];\s*""", flags = re.UNICODE)
        matched = None
        start = None
        end = None
        for i in range(len(self.lines)):
            if start is None:
                if rstart.search(self.lines[i]):
                    start = i
            elif rend.search(self.lines[i]):
                end = i
                break
        if start is None or end is None:
            return

        data = ''.join(self.lines[start:end + 1])
        data = data[data.find('=') + 1:]
        data = data[:data.rfind(';')]

        return json.loads(data)


def print_table(rows):
    def get_len(s):
        if isinstance(s, str):
            return len(s)
        ret = 0
        for i in s:
            cat = unicodedata.category(i)
            if cat[1] == 'o' and len(i.encode('utf-8')) > 1:
                ret += 2
            else:
                ret += 1
        return ret

    def print_row(r, sep = '|'):
        p = list()
        for i in zip(r, lens):
            l = get_len(i[0])
            m = i[0]
            if isinstance(m, unicode):
                m = m.encode('utf-8')
            p.append(m + ' ' * (i[1] - l))
        print sep.join(p)

    lens = [0] * len(rows[0])
    for r in rows:
        lens = map(max, zip(lens, map(get_len, r)))

    lens = [i + 1 for i in lens]
    print_row(rows[0])
    print_row(['-' * i for i in lens], sep = '+')
    map(print_row, rows[1:])

