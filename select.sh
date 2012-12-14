#!/bin/bash
# $File: select.sh
# $Date: Fri Dec 14 13:31:01 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. config.sh

wget "$DM/xkBks.vxkBksXkbBs.do?m=rxSearch&p_xnxq=2012-2013-2&tokenPriFlag=rx&is_zyrxk=1" \
	--load-cookies $TD/cookie.txt \
	-O $TD/main.html

wget "$DM/xkBks.vxkBksXkbBs.do" \
	--load-cookies $TD/cookie.txt \
	--post-data="$(./parse_select.py $TD/main.html)" \
	-O $TD/out.html
