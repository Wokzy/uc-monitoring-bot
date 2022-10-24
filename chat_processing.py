import os
import time
import queue
import random
import threading
import photographer

from util import *
from PIL import Image
from constants import *
from datetime import datetime
from work_with_uc import login
from work_with_uc import upload_file
from api.prew_image import prevImage
from crash_logging import crash_logging
from datetime import datetime, timedelta
from api.group_chat_method import ChatApi
from models.uc_api.uc_api_models import ChatEvent


global stats_queue
stats_queue = queue.Queue() # {"index":object_index, "string":some_string}

def make_image_and_send_it(object_index, session_id, my_user_id, chats, urls, ip, port, grafana=None):
    global stats_queue
    screenshot_filename = str(datetime.now().timestamp()).replace('.', '') + str(random.randint(1, 10**5)) + '.png'

    print_if_debug(f'Getting image from {urls}')
    photographer.make_screen(urls, screenshot_filename=screenshot_filename, grafana=grafana)
    print_if_debug('Image got. Sending...')

    if debug:
        filename = f"{'_'.join(time.asctime().split(' '))}{screenshot_filename}"
        Image.open(screenshot_filename).save(filename, 'PNG')

        result_rpeorting_string = f'{time.asctime()}   Image saved: {filename}'

        print_if_debug(result_rpeorting_string)

        os.remove(screenshot_filename)
        stats_queue.put({'index':object_index, 'string':result_rpeorting_string, 'type':'successes'})
        return {'status_code': 200}

    base64_preview_40, size_40, img_bytes_300, size_300, width_300, height_300, width_40, height_40, \
    wight, height = prevImage(filename=screenshot_filename)

    print_if_debug('made prevImage', 'full')

    img = Image.open(screenshot_filename).resize((width_300, height_300))
    thumbnail_filename = f"{time.asctime()}   {screenshot_filename.split('.')[0]}_thumbnail.png"
    img.save(thumbnail_filename, 'PNG')

    print_if_debug('thumbnail made', 'full')

    attachment_id, file_size = upload_file(session_id, file_path=f"{SCREENSHOTPATH}/{screenshot_filename}", filename=screenshot_filename, ip=ip, port=port)
    print_if_debug('image uploaded', 'full')
    upload_file(session_id, file_path=f"{SCREENSHOTPATH}/{thumbnail_filename}", filename=thumbnail_filename, ip=ip, port=port, mediasize='m',
                attachment_id=attachment_id)
    print_if_debug('thumbnail uploaded', 'full')

    for chat in chats:
        if 'plain_text' in chat:
            plain_text = chat['plain_text']
        else:
            plain_text = ''

        chat_id = int(chat['ID'])

        message = {"uuid": random.randint(1000, 99999), "sender_id": my_user_id, "chat_id": chat_id,
                   "chat_type": chat['type'], "type": "IMAGE", "plaintext": plain_text,
                   "options": {"images": [
                       {"attachment_id": attachment_id, "filename": screenshot_filename, "size": file_size, "width": wight,
                        "height": height, "mimetype": SCREENSHOTFILETYPE, "sizes": [{"size": "m", "width": width_300, "height": height_300}],
                        "thumbnail": {"source": f"data:image/png;base64,{base64_preview_40}", "width": width_40, "height": height_40}}]}}

        print_if_debug('message configured', 'full')

        send_message = [ChatEvent(**message)]
        print_if_debug('ChatEvent', 'full')
        url = None #TODO
        response = ChatApi(data=send_message, ip=ip, port=port, cookie=session_id).group_chat_event_send(url)
        print_if_debug('response made', 'full')
        stats_queue.put({'index':object_index, 'string':f'{time.asctime()}   {chat["ID"]} Image has been made and sent with status code {response.status_code}', 'type':'successes'})

    os.remove(screenshot_filename)

    return response


def process_chats_2(object_index, chat_config, session_id, my_user_id):
    global stats_queue
    try:
        if 'GRAFANA' in chat_config and chat_config['GRAFANA'] and type(chat_config['GRAFANA']) == int:
            grafana = {"LOGIN":chat_config['GRAFANA_LOGIN'], "PASSWORD":chat_config['GRAFANA_PASSWORD']}
        else:
            grafana = None
        res = make_image_and_send_it(object_index=object_index, session_id=session_id, my_user_id=my_user_id,
                                     chats=chat_config['CHATS'], urls=chat_config['URLS'], 
                                     ip=chat_config['IP_UC_ACCESS_LAYER_WEB'], port=chat_config['PORT_UC_ACCESS_LAYER_WEB'],
                                     grafana=grafana)['status_code']
        print_if_debug(f"{res} for {', '.join([str(i) for i in chat_config['URLS']])} {chat_config['CHATS']}", end='\n\n')
        return
    except Exception:
        crash_log = crash_logging(addition_string=str(chat_config['URLS'])+'\n'+str(chat_config['CHATS']))
        stats_queue.put({'index':object_index, 'string':f'{time.asctime()}   Crashed, log is saved in {crash_log}', 'type':'errors'})
        return


def process_chats(objects, first_iteration, db=False):
    global debug, stats_queue
    db = debug

    for i in range(len(objects)):
        if 'STATS' not in objects[i]:
            objects[i]['STATS'] = {"successes":[], "errors":[], 'stats':[]}

        obj = objects[i]
        ip = obj['IP_UC_ACCESS_LAYER_WEB']
        port = obj['PORT_UC_ACCESS_LAYER_WEB']
        user = obj['UC_USER']
        password = obj['UC_PASSWORD']

        if 'time' in obj or first_iteration:
            now = datetime.now()
            check = datetime_in_conditions(now, conditions=obj['time'])
            if check == True:
                session_id, my_user_id = login(ip, port, user, password, debug=debug)
                update_timers(now, obj['time'])
                threading.Thread(target=process_chats_2, args=(i, obj, session_id, my_user_id), daemon=True).start()

                #objects[i]['STATS']['stats'].append(f'{time.asctime()}   Began making image')
            elif check == False:
                update_conditions(now, obj['time'])

    while not stats_queue.empty():
        stat = stats_queue.get()
        while len(objects[stat['index']]['STATS']['stats']) >= STATS_LIMIT:

            string = objects[stat['index']]['STATS']['stats'][0]
            objects[stat['index']]['STATS']['stats'].remove(string)

            if string in objects[stat['index']]['STATS']['errors']:
                objects[stat['index']]['STATS']['errors'].remove(string)

            if string in objects[stat['index']]['STATS']['successes']:
                objects[stat['index']]['STATS']['successes'].remove(string)

        objects[stat['index']]['STATS'][stat['type']].append(stat['string'])
        objects[stat['index']]['STATS']['stats'].append(stat['string'])

    return objects
