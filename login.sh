#!/bin/bash -e
# $File: login.sh
# $Date: Fri Dec 14 22:33:13 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. config.sh

function ocr()
{
	tesseract $TD/captcha.jpg $TD/captcha 2>/dev/null
	cat $TD/captcha.txt
}

while true
do
	rm -rf $TD
	mkdir -p $TD

	wget --keep-session-cookies --save-cookies $TD/cookie_login.txt \
		$DM/xklogin.do -O $TD/login.html -o /dev/null

	wget --load-cookies $TD/cookie_login.txt \
		"$DM/login-jcaptcah.jpg?captchaflag=login1" \
		-O $TD/captcha.jpg -o /dev/null

	captcha=$(ocr)
	echo "captcha: $captcha"

	wget --keep-session-cookies --save-cookies $TD/cookie.txt \
		--load-cookies $TD/cookie_login.txt -O $TD/main.html \
		--post-data="j_username=$USERNAME&j_password=$PASSWORD&captchaflag=login1&_login_image_=$captcha" \
		"$DM/j_acegi_formlogin_xsxk.do"

	iconv -f gb2312 -t "utf-8" $TD/main.html | grep 验证码不正确> /dev/null || exit
	sleep 1
done
