import json
import cv2
import base64
import numpy as np

from local_query import postMethod

# 读取图像
image = cv2.imread('imgs/event1.jpg')

# 将图像转换为Base64格式
retval, buffer = cv2.imencode('.jpg', image)
image_base64 = base64.b64encode(buffer).decode()

result = postMethod("http://127.0.0.1:8000/api/device/allevents", {})
result = json.loads(result)
# 在网页上显示图像
html_ori = f'<img src="data:image/jpeg;base64,{image_base64}">'
image = result[0]['image']
html = f'<img src="data:image/jpeg;base64,{image}">'
with open('index.html', 'w') as file:
    file.write(html)

with open('index_ori.html', 'w') as file:
    file.write(html_ori)