import base64
import requests
import re

from openai import OpenAI

client = OpenAI(api_key='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')

# Set your OpenAI API key here
image_path = "./test.jpg"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# def get_brand_from_description(description):
#     try:
#         with open('test.jpg', 'rb') as file1:
#             response = client.chat.completions.create(model="gpt-4-vision-preview",# Replace with the appropriate model, such as GPT-4 if available
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user",
#                  "content": f"What brand is most likely associated with this image: {description}?"}
#             ])
#             return response.choices[0].message.content.strip()
#     except Exception as e:
#         print(f"Error: {e}")
#         return "Error in brand identification"


def get_esg_score(brand):
    try:
        response = client.chat.completions.create(model="gpt-4-vision-preview", max_tokens = 100,  # Replace with the appropriate model, such as GPT-4 if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Find the ESG score of {brand} and return the best score in the format [brand (string), esg category (Good/Average/Bad) (string), esg score out of 100 (integer)]. in case of you error in finding, return error in finding the esg"}
        ])
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error in getting ESG score"

def get_brand():
    base64_image = encode_image("test.jpg")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer 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"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "From the image identify the brand. return only the brand"
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
        return response.json()['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    description = "https://pbs.twimg.com/media/FLhJVtSXoAY2x-q.jpg:large"
    brand = get_brand()
    esg_score = get_esg_score(brand) if brand else "Brand not identified"
    #esg_score = get_brand()

    print(f"Brand: {brand}, ESG Score: {esg_score}")
    esg_match = re.search(r'\[.*?\]', esg_score)

    if esg_match:
        esg_score_str = match.group(0)
        # Convert the matched string to a list
        # This involves removing the square brackets and splitting the string by comma
        esg_score_array = esg_score_str.strip('[]').split(', ')
        print(esg_score_array)
    else:
        print("No ESG score array found in the text.")
