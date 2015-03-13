#!/bin/bash -e
# $File: login.sh
# $Date: Sun Mar 08 10:34:12 2015 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. config.sh

function ocr()
{
	#tesseract $TD/captcha.jpg $TD/captcha 2>/dev/null
	#cat $TD/captcha.txt
    feh $TD/captcha.jpg &
    feh_pid=$!
    zenity --entry
    kill $feh_pid
}

rm -rf $TD
mkdir -p $TD

WGET_OPT="--keep-session-cookies --load-cookies $TD/cookie.txt \
    --save-cookies $TD/cookie.txt"

while true
do
	wget --keep-session-cookies --save-cookies $TD/cookie.txt \
		$DM/xklogin.do -O $TD/login.html -o /dev/null

	wget $WGET_OPT \
		"$DM/login-jcaptcah.jpg?captchaflag=login1" \
        -O $TD/captcha.jpg -o /dev/null

	captcha=$(ocr)
	echo "captcha: $captcha"

    wget $WGET_OPT -O $TD/main.html \
		--post-data="j_username=$USERNAME&j_password=$PASSWORD&captchaflag=login1&_login_image_=$captcha" \
		"$DM/j_acegi_formlogin_xsxk.do"

	iconv -f gb2312 -t "utf-8" $TD/main.html | grep 验证码不正确> /dev/null || exit
	sleep 1
done
