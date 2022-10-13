import sys
import json

from datetime import datetime, timedelta
from util import set_time_conditions, weekdays, check_arg

with open('config.json', 'r') as f:
	file = json.load(f)
	f.close()

CLI_IP = file['CLI']['CLI_IP']
CLI_PORT = file['CLI']['CLI_PORT']

ENCODING = 'ascii'

file = list(file['CHATS_OBJECTS'])

for i in range(len(file)):
	file[i]['time_config'] = str(file[i]['time'])
	file[i]['time'] = set_time_conditions(file[i]['time'])

OBJECTS = list(file)

SCREENSHOTPATH = '.'
SCREENSHOTFILENAME = 'scrn.png'
SCREENSHOTFILETYPE = 'image/png'
CRASH_LOGS_DIRECTORY = 'crash_logs'
CRASH_LOGS_FILE_FORMAT = '.txt'

STOP_PROGRAMM_AFTER_CRASH = check_arg(['--stop-after-crash'], sys.argv, return_result=False)

LOG_HTTP_TRAFFIC = False
