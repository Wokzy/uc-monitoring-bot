import os
import sys
import json
import shutil

from datetime import datetime, timedelta
from util import set_time_conditions, weekdays, check_arg


#CONFIG_PATH = 'config.json'

#if CONFIG_PATH not in os.listdir():
CONFIG_FOLDER = '.' #'./'
CONFIG_PATH = f'{CONFIG_FOLDER}/config.json' # config.json
if not os.path.exists(CONFIG_PATH):
	if not os.path.exists(CONFIG_FOLDER):
		print(f'{CONFIG_PATH} not found, trying to load config from current directory(config.json)')
		CONFIG_PATH = 'config.json'
	else:
		shutil.copy(f'{CONFIG_FOLDER}/config_sample.json', CONFIG_PATH)

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
		file[i]['GRAFANA'] = int(file[i]['GRAFANA'])
except Exception as e:
	print(e)
	print(f'smth wrong with config, please check: {CONFIG_PATH}')
	sys.exit()

OBJECTS = list(file)


GRAFANA_LOGIN_FIELD_XPATH = '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
GRAFANA_PASSWORD_FIELD_XPATH = '//*[@id="current-password"]'
GRAFANA_LOGIN_BUTTON_XPATH = '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'


SCREENSHOTPATH = '.'
SCREENSHOTFILENAME = 'scrn.png'
SCREENSHOTFILETYPE = 'image/png'
CRASH_LOGS_DIRECTORY = 'crash_logs' #'crash_logs'
CRASH_LOGS_FILE_FORMAT = '.txt'
STATS_LIMIT = 5

STOP_PROGRAMM_AFTER_CRASH = check_arg(['--stop-after-crash'], sys.argv, return_result=False)

LOG_HTTP_TRAFFIC = False
