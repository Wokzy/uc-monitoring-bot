import os
import sys
import time
import traceback

from util import check_arg
from constants import CRASH_LOGS_DIRECTORY, STOP_PROGRAMM_AFTER_CRASH


def crash_logging(stop_the_programm=STOP_PROGRAMM_AFTER_CRASH):
    print('CRASH LOG CALLED')
    if check_arg(['--no-crash-log'], sys.argv, return_result=False):
        return

    if CRASH_LOGS_DIRECTORY not in os.listdir():
        os.mkdir(CRASH_LOGS_DIRECTORY)

    filename = '_'.join(time.asctime().split(' ')) + '.txt'

    with open(f"{CRASH_LOGS_DIRECTORY}/{filename}", 'w') as f:
        f.write(time.asctime() + ' : ' + ' '.join(sys.argv) + '\n\n')
        f.write(traceback.format_exc())
        f.close()

    print()
    print(traceback.format_exc())
    print()

    if stop_the_programm:
        sys.exit()

    time.sleep(5)
