import requests
import json
import base64
import numpy as np
import cv2
import time

fake_request = json.loads(open('image2.json', 'r').read())

url = 'https://color-cone-server.herokuapp.com/ '

# string = fake_request['img']
# jpg_original = base64.b64decode(string)
# jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
# img = cv2.imdecode(jpg_as_np, flags=1)

# cv2.imshow( "Display window", img )
# cv2.waitKey(0)

response = requests.post(f'{url}', json=fake_request)


print("Status code: ", response.status_code)
print("Printing Entire Post Request")
print(response.json())

job_id = response.json()['job_id']

time.sleep(3)

response = requests.get(f'{url}/results/{job_id}')
print(response.json())


string = response.json()['img']
jpg_original = base64.b64decode(string)
jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
img = cv2.imdecode(jpg_as_np, flags=1)

cv2.imshow( "Display window", img )
cv2.waitKey(0)