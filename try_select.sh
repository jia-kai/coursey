#!/bin/bash
# $File: try_select.sh
# $Date: Mon Mar 04 23:53:38 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

export PYTHONIOENCODING="utf-8"

while true
do
	./login.sh
	. ./setcookie.sh
	./main.py try_select $(cat data/csid)
	sleep 5
done 

