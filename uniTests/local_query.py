import requests
import json

def postMethod(url, data):
    headers = {'Content-Type': 'application/json'}
    post_json = json.dumps(data)

    r = requests.post(url, headers=headers, data=post_json)
    print(r.text)


if __name__ == "__main__":
    postMethod("http://127.0.0.1:8000/api/device/cameras", {})