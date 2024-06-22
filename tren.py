import requests
from pathlib import Path

file_to_send = Path(__file__).parent / "tests" / "index.png"

url = "http://localhost:8000/post_memes"


def post_memes():
    response = requests.post(url, files={"file": open(file_to_send, 'rb')})
    response = response.json()
    print(response)
    # print(response['description'])
    # print(response['src'])
    # print(response['id'])


post_memes()
