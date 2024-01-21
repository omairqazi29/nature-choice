import base64
import requests

image_path = "./test.jpg"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)


def get_brand():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer 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"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "max_tokens": 50,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"

                        }
                    }
                ]
            }
        ],
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code != 200:
        print(f"HTTP error {response.status_code}: {response.text}")
    else:
        print(response.json())


get_brand()