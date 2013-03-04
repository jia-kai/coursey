#!/bin/bash
# $File: try_select.sh
# $Date: Mon Mar 04 23:43:30 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

rm -f data/try_select.log
while true
do
	./main.py try_select $(cat data/csid)
	sleep 5
	./login.sh
	. ./setcookie.sh
done  | tee data/try_select.log

