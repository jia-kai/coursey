#!/bin/bash
# $File: setcookie.sh
# $Date: Fri Dec 14 21:24:29 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. ./config.sh

cookie=''
while true
do
	read x x x x x name value || break
	[ -z "$cookie" ] || cookie="$cookie; "
	cookie="${cookie}${name}=${value}"
done < <(tail -n +5 $TD/cookie.txt)
echo $cookie
export coursey_cookie=$cookie

