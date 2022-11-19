import os
import sys
import time

from PIL import Image
from datetime import datetime, timedelta

__author__ = "Yegor Yershov"

weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


def check_arg(vrs:list, args:list, necessary=False, return_result=True):
    for arg in vrs:
        if arg in args:
            if return_result:
                return args[args.index(arg)+1]
            return True
    if necessary:
        raise RuntimeError(f'Arg {vrs} is necessary, see --help to get more info')
    return False

global debug_print_mode, debug
able_printing_modes = ['none', 'short', 'full', None]
debug = check_arg(['--debug'], sys.argv, return_result=False)

debug_print_mode = check_arg(['--debug-printing'], sys.argv, return_result=True) or 'short'
if debug_print_mode not in able_printing_modes:
    debug_print_mode = 'short'


def print_if_debug(string, mode='short', end='\n'):
    # print(debug_print_mode)
    if debug_print_mode in ['full', 'ultra'] or debug_print_mode == mode:
        print(string, end=end)


def datetime_in_timerange(time, timerange):
    hour = time.hour
    minute = time.minute
    if timerange['using_next_day']:
        if hour > timerange['begin']['hour']:
            return True
        elif hour == timerange['begin']['hour'] and minute >= timerange['begin']['minute']:
            return True
        elif hour < timerange['end']['hour']:
            return True
        elif hour == timerange['end']['hour'] and minute <= timerange['end']['minute']:
            return True
    else:
        if hour > timerange['begin']['hour'] or (hour == timerange['begin']['hour'] and minute >= timerange['begin']['minute']):
            if hour < timerange['end']['hour'] or (hour == timerange['end']['hour'] and minute <= timerange['end']['minute']):
                return True

    return False


def datatime_is_sertain(dtm, time):
    return (dtm.minute == time['minute'] and dtm.hour == time['hour'])


def update_timers(now, conditions):
    if 'minutes' in conditions:
        conditions['range_timer'] = now + conditions['minutes']

    return conditions


def datetime_in_conditions(time, conditions): # Time means current time
    if 'weekdays' in conditions and time.weekday() not in conditions['weekdays']:
        return False
    elif 'day' in conditions:
        if time < conditions['day']:
            return False

    if 'schedule' in conditions:
        for tm in conditions['schedule']:
            if tm['type'] == 'range':
                if datetime_in_timerange(time, tm):
                    if 'range_timer' in conditions and time < conditions['range_timer']:
                        print_if_debug(conditions['range_timer'] - time, "full")
                        return 'range_timer'
                    return True
            elif tm['type'] == 'certain':
                return datatime_is_sertain(time, tm)


def update_conditions(now, conditions):
    if 'range_timer' in conditions:
        del conditions['range_timer']

    if 'weekdays' in conditions:
        return conditions

    if now.day > conditions['day'].day:
        conditions['day'] += conditions['every_days']

    return conditions


def to_hours(hour_string):
    return min(23, max(0, int(hour_string)))


def to_minutes(minute_string):
    return min(59, max(0, int(minute_string)))


def set_time_conditions(time_string):
    conditions = {}
    time = time_string.split(' ')
    schedule = []
    for tm in time[0].split(','):
        if '-' in tm:
            time_range = {'type':'range', 'using_next_day':False}
            tm_range = tm.split('-')
            tm_range[0] = tm_range[0].split(':')
            tm_range[1] = tm_range[1].split(':')
            time_range['begin'] = {}
            time_range['end'] = {}
            time_range['begin']['hour'] = to_hours(tm_range[0][0])
            time_range['begin']['minute'] = to_minutes(tm_range[0][1])
            time_range['end']['hour'] = to_hours(tm_range[1][0])
            time_range['end']['minute'] = to_minutes(tm_range[1][1])

            if time_range['begin']['hour'] > time_range['end']['hour']:
                time_range['using_next_day'] = True
            elif time_range['begin']['hour'] == time_range['end']['hour'] and time_range['begin']['minute'] > time_range['end']['minute']:
                time_range['using_next_day'] = True

            schedule.append(time_range)
        else:
            certain_time = {'type':'certain'}
            certain_time['hour'] = to_hours(tm.split(':')[0])
            certain_time['minute'] = to_minutes(tm.split(':')[1])
            schedule.append(certain_time)

    if time[1] != '*':
        conditions['minutes'] = timedelta(minutes=int(time[1]))

    if time[2] == '*' and time[3] != '*':
        conditions['weekdays'] = [i-1 for i in list(map(int, time[3].split(',')))]
    else:
        if time[2] == '*':
            time[2] = 1
        conditions['every_days'] = timedelta(days=int(time[2]))
        conditions['day'] = datetime.now().replace(hour=0, minute=0, second=0)

    conditions['schedule'] = schedule

    return conditions


def prepare_object_to_sending(encoding, obj, split_data=False):
    if split_data:
        string = str(obj) + '\n'
    else:
        string = str(obj)
    return string.replace("'", '"').encode(encoding)
