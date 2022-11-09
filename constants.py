import os
import sys
import json

from datetime import datetime, timedelta
from util import set_time_conditions, weekdays, check_arg


CONFIG_PATH = 'config.json'

if CONFIG_PATH not in os.listdir():
	CONFIG_PATH = '/etc/uc_monitoring_bot_config.json'

try:
	with open(CONFIG_PATH, 'r') as f:
		file = json.load(f)
		f.close()

	CLI_IP = file['CLI']['CLI_IP']
	CLI_PORT = file['CLI']['CLI_PORT']

	ENCODING = 'utf-8'

	file = list(file['CHATS_OBJECTS'])

	for i in range(len(file)):
		file[i]['time_config'] = str(file[i]['time'])
		file[i]['time'] = set_time_conditions(file[i]['time'])
		file[i]['LABEL'] = file[i]['LABEL'].replace(' ', "_")
except:
	print(f'smth wrong with config, please check: {CONFIG_PATH}')
	sys.exit()

OBJECTS = list(file)

SCREENSHOTPATH = '.'
SCREENSHOTFILENAME = 'scrn.png'
SCREENSHOTFILETYPE = 'image/png'
CRASH_LOGS_DIRECTORY = 'crash_logs'
CRASH_LOGS_FILE_FORMAT = '.txt'
STATS_LIMIT = 5

STOP_PROGRAMM_AFTER_CRASH = check_arg(['--stop-after-crash'], sys.argv, return_result=False)

LOG_HTTP_TRAFFIC = False
