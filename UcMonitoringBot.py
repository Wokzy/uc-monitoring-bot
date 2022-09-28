import os
import sys

if '/'.join(sys.argv[0].split('/')[:-1:]):
    os.chdir('/'.join(sys.argv[0].split('/')[:-1:]))

import time
import util

from constants import *
from datetime import datetime
from crash_logging import crash_logging
from chat_processing import process_chats


__author__ = "Yegor Yershov"


def main():
    first_iteration = True

    objects = list(OBJECTS)

    while True:
        try:
            if objects:
                objects = process_chats(OBJECTS, first_iteration, util.debug)
        except Exception:
            crash_logging()

        now = datetime.now()
        first_iteration = False
        time.sleep((now.replace(minute=now.minute+1, second=0) - now).total_seconds()+1)


if util.check_arg(['--help', '-h'], sys.argv, return_result=False):
    string = \
        '-h   --help             | show this message\n' + \
        '     --debug            | turn on debug mode (no login to uc, screenshots are saving)\n' + \
        '     --debug-printing   | none, short (default) (additional info), full (all info), ultra\n' + \
        '     --no-crash-log     | Disable crash logging\n' + \
        '     --stop-after-crash | Stop the programm after executing Exception\n'

    print(string)
    sys.exit()

if util.debug:
    util.print_if_debug('Debug mode on')
print(f'debug_print_mode: {util.debug_print_mode}')

try:
    main()
except Exception:
    crash_logging()
