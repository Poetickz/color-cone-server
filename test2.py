import requests
import json
import base64
import numpy as np
import cv2
import time
url = "https://color-cone-server.herokuapp.com/"
fake_request = json.loads(open('image2.json', 'r').read())


headers= {}

response = requests.request("POST", url, headers=headers, json=fake_request)


job_id = response.json()['job_id']

print(job_id)


time.sleep(2)

response = requests.request("GET", f'{url}results/{job_id}', headers=headers)


string = response.json()['img']
jpg_original = base64.b64decode(string)
jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
img = cv2.imdecode(jpg_as_np, flags=1)

cv2.imshow( "Display window", img )
cv2.waitKey(0)