import sys
import json

from datetime import datetime, timedelta
from util import set_time_conditions, weekdays, check_arg

with open('config.json', 'r') as f:
	file = json.load(f)
	f.close()

for obj in file:
	obj['time'] = set_time_conditions(obj['time'])

	if 'GRAFANA' in obj:
		if 'GRAFANA_LOGIN' not in obj:
			obj['GRAFANA_LOGIN'] = file['DEFAULT_GRAFANA_LOGIN']
		if 'GRAFANA_PASSWORD' not in obj:
			obj['GRAFANA_PASSWORD'] = file['DEFAULT_GRAFANA_PASSWORD']

OBJECTS = list(file)

SCREENSHOTPATH = '.'
SCREENSHOTFILENAME = 'scrn.png'
SCREENSHOTFILETYPE = 'image/png'
CRASH_LOGS_DIRECTORY = 'crash_logs'

STOP_PROGRAMM_AFTER_CRASH = check_arg(['--stop-after-crash'], sys.argv, return_result=False)

LOG_HTTP_TRAFFIC = False
