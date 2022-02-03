#!/bin/bash
set -e
if [ trend_app_protect.ini ]
then
	cp trend_app_protect.ini.template trend_app_protect.ini
	echo "Please edit trend_app_protect.ini to put key and sercret parameters correct values"
	echo "https://cloudone.trendmicro.com/docs/application-security/python/#install-the-agent"
	exit 1
fi
pip install -r requirements.txt
source venv/bin/activate
export FLASK_APP=f
flask run -h 0.0.0.0 -p 5000
