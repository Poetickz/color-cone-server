import requests
import json
import base64
import numpy as np
import cv2
import time

fake_request = json.loads(open('image2.json', 'r').read())

url = 'https://color-cone-server.herokuapp.com'

# # string = fake_request['img']
# # jpg_original = base64.b64decode(string)
# # jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
# # img = cv2.imdecode(jpg_as_np, flags=1)


# response = requests.post(f'{url}', json=fake_request)


# # print("Status code: ", response.status_code)
# # print("Printing Entire Post Request")
# # print(response.json())

# job_id = response.json()['job_id']

# print(job_id)

response = requests.get(f'{url}/results/71036543-432e-4c16-a574-948d4956789f')
print(response.json())


string = response.json()['img']
jpg_original = base64.b64decode(string)
jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
img = cv2.imdecode(jpg_as_np, flags=1)

cv2.imshow("Display window", img)
cv2.waitKey(0)
