import json
import requests


class PicMaker:
    url = ""

    def __init__(self, url):
        self.url = url

    def generate_image_from_prompt(self, prompt):

        payload = json.dumps({
            "prompt": prompt
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)

        # with open("response.png", "wb") as f:
        #     f.write(response.content)
        return response.content
