import requests
import json
import base64
import numpy as np
import cv2

response = requests.get(f'http://localhost:5000/results/a0f9b76f-82e1-4ddd-bfa4-51dadbab6e07')
print(response.json())


string = response.json()['img']
jpg_original = base64.b64decode(string)
jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
img = cv2.imdecode(jpg_as_np, flags=1)

cv2.imshow( "Display window", img )
cv2.waitKey(0)