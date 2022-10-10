
from api.prew_image import prevImage
from models.uc_api.uc_api_models import LoginRequest
from api.p2p_chat_method import AttachmentAPI
from api.user_method import UserApi as uc_UserApi
from constants import *


def login(ip, port, user, password, debug):
    if debug:
        return None, None

    new_user = LoginRequest(login=user, password=password)
    response = uc_UserApi(data=new_user, ip=ip, port=port).login()

    try:
        return response.headers['protei-uc-sessionid'], int(response.data.payload['user_id'])
    except:
        raise RuntimeError(f'Cannot login to UC, smth wrong\n{response.headers} {response.status_code}')


def upload_file(session_id, file_path, ip, port, mediasize=None, attachment_id=None):
    response = AttachmentAPI(cookie=session_id, ip=ip, port=port).upload_file(files=file_path, filename=SCREENSHOTFILENAME,
                                                            file_type=SCREENSHOTFILETYPE, mediasize=mediasize,
                                                            attachment_id=attachment_id)

    try:
        attachment_id = response[0].headers["protei-uc-attachmentid"]
        file_size = response[1]

        return attachment_id, file_size
    except:
        return None