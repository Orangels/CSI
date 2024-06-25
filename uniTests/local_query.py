import time
import requests
import json
import random
import cv2
import base64
from utils.config_utils import yaml_config


def postMethod(url, data):
    headers = {'Content-Type': 'application/json'}
    post_json = json.dumps(data)

    r = requests.post(url, headers=headers, data=post_json)
    return r.text


def creatEvents():
    y_config = yaml_config().config

    img = cv2.imread('./imgs/event1.jpg')
    retval, buffer = cv2.imencode('.jpg', img)
    image_base64 = base64.b64encode(buffer).decode("utf-8")
    for i in range(10):

        upload_event = dict(Camera_id=random.randint(1, 4), area="随便生成",
                            event=y_config["event_type"]['EVENT_TYPE'][
                                random.randint(0, 9)]['NAME'],
                            time=int(time.time()) - i*10,
                            image="data:image/jpeg;base64,"+image_base64, is_upload=False)

        postMethod("http://127.0.0.1:8000/api/device/CreatEvents", upload_event)


if __name__ == "__main__":
    # postMethod("http://127.0.0.1:8000/api/device/cameras", {})
    creatEvents()
