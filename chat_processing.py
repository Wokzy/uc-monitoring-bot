import time
import random
import threading
import photographer

from util import *
from PIL import Image
from work_with_uc import login
from api.prew_image import prevImage
from work_with_uc import upload_file
from models.uc_api.uc_api_models import ChatEvent
from api.group_chat_method import ChatApi
from crash_logging import crash_logging
from datetime import datetime, timedelta
from constants import *


def make_image_and_send_it(session_id, my_user_id, chats, urls, ip, port, grafana=None):
    print_if_debug(f'Getting image from {urls}')
    photographer.make_screen(urls, grafana=grafana)
    print_if_debug('Image got. Sending...')

    if debug:
        filename = f"{'_'.join(time.asctime().split(' '))}.png"
        Image.open(SCREENSHOTFILENAME).save(filename, 'PNG')

        print_if_debug(f'Image saved: {filename}')

        return {'status_code': 200}

    base64_preview_40, size_40, img_bytes_300, size_300, width_300, height_300, width_40, height_40, \
    wight, height = prevImage(filename=SCREENSHOTFILENAME)

    print_if_debug('made prevImage', 'full')

    img = Image.open(SCREENSHOTFILENAME).resize((width_300, height_300))
    thumbnail_filename = f"{SCREENSHOTFILENAME.split('.')[0]}_thumbnail.png"
    img.save(thumbnail_filename, 'PNG')

    print_if_debug('thumbnail made', 'full')

    attachment_id, file_size = upload_file(session_id, file_path=f"{SCREENSHOTPATH}/{SCREENSHOTFILENAME}", ip=ip, port=port)
    print_if_debug('image uploaded', 'full')
    upload_file(session_id, file_path=f"{SCREENSHOTPATH}/{thumbnail_filename}", ip=ip, port=port, mediasize='m',
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
                       {"attachment_id": attachment_id, "filename": SCREENSHOTFILENAME, "size": file_size, "width": wight,
                        "height": height, "mimetype": SCREENSHOTFILETYPE, "sizes": [{"size": "m", "width": width_300, "height": height_300}],
                        "thumbnail": {"source": f"data:image/png;base64,{base64_preview_40}", "width": width_40, "height": height_40}}]}}

    print_if_debug('message configured', 'full')

    send_message = [ChatEvent(**message)]
    print_if_debug('ChatEvent', 'full')
    url = None #TODO
    response = ChatApi(data=send_message, ip=ip, port=port, cookie=session_id).group_chat_event_send(url)
    print_if_debug('response made', 'full')

    return response


def process_chats_2(chat_config, session_id, my_user_id):
    try:
        if 'GRAFANA' in chat_config:
            grafana = {"LOGIN":chat_config['GRAFANA_LOGIN'], "PASSWORD":chat_config['GRAFANA_PASSWORD']}
        else:
            grafana = None
        res = make_image_and_send_it(session_id=session_id, my_user_id=my_user_id,
                                     chats=chat_config['CHATS'], urls=chat_config['URLS'], 
                                     ip=chat_config['IP_UC_ACCESS_LAYER_WEB'], port=chat_config['PORT_UC_ACCESS_LAYER_WEB'],
                                     grafana=grafana)['status_code']
        print_if_debug(f"{res} for {', '.join([str(i) for i in chat_config['URLS']])} {chat_config['CHATS']}", end='\n\n')
    except Exception:
        crash_logging()


def process_chats(objects, first_iteration, db=False):
    global debug
    db = debug

    for obj in objects:
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
                threading.Thread(target=process_chats_2, args=(obj, session_id, my_user_id)).start()
            elif check == False:
                update_conditions(now, obj['time'])

    return objects
