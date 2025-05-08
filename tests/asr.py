# from fastapi.testclient import TestClient
# from src.open_llm_vtuber.asr import app  # 替换为你的 app 实例所在模块

# client = TestClient(app)

# def test_asr_upload():
#     with open("tests/audio.wav", "rb") as f:
#         response = client.post("/asr", files={"file": ("audio.wav", f, "audio/wav")})
#     assert response.status_code == 200
#     print(response.json())

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://10.8.123.4:9604/asr"
files = {"file": ("audio.wav", open("media/audio.wav", "rb"), "audio/wav")}

# response = requests.post(url, files=files)
response = requests.post(url, files=files, verify=False)
# response = requests.post(url, files=files, verify="ssl/cert.pem")
print(response.status_code)
print(response.text)

'''
curl -X POST "https://10.8.123.4:9604/asr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@media/audio.wav" \
  --insecure
'''