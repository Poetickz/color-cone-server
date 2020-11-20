import base64
import cv2
import os
import json
import numpy as np

from enchanter import processImage


def fake_algorithm(img_json):

    response = img_json
    string = response['img']
    level = 1.025
    sensitive = 0.5
    if '!level' in response:
        level = response['level']

    if '!sensitive' in response:
        sensitive = response['sensitive']
    jpg_original = base64.b64decode(string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    gray = processImage(img, level, sensitive)

    string = base64.b64encode(cv2.imencode('.png', gray)[1]).decode()
    dict = {
        'img': string
    }

    # Test json
    # print(json.dumps(dict, ensure_ascii=False, indent=4))
    # with open('image.json', 'w+') as outfile:
    #     json.dump(dict, outfile, ensure_ascii=False, indent=4)

    return json.dumps(dict, ensure_ascii=False, indent=4)


# fake_request = json.loads(open('image2.json', 'r').read())

# fake_algorithm(fake_request)
