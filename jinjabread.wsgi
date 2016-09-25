#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/jinjabread/")

from jinjabread import app as application
application.secret_key = '908s7dfklj3n4509sd8f'