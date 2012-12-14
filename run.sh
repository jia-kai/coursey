#!/bin/zsh
while true
do
	./select.sh
	iconv -f gb2312 -t utf-8 /tmp/coursex/out.html | grep showMsg
	t=$(($RANDOM * 3.0 / 32767 + 2.8))
	echo $t
	sleep $t
done
