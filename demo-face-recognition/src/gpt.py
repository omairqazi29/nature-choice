import base64
import os

import requests
from openai import OpenAI

# from dotenv import load_dotenv

# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")
api_key = '<api key here>'
client = OpenAI(api_key=api_key)

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



# def get_esg_score(brand):
#     try:
#         response = client.chat.completions.create(model="gpt-4-vision-preview", max_tokens = 100,  # Replace with the appropriate model, such as GPT-4 if available
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f"What is ESG score of the {brand}'s parent company using sustainalytics"}
#         ])
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         print(f"Error: {e}")
#         return "Error in getting ESG score"

def get_brand(image_path):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
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
                        "text": "From the image identify the brand. return only the name"
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
# if __name__ == "__main__":
#     description = "https://pbs.twimg.com/media/FLhJVtSXoAY2x-q.jpg:large"
#     brand = get_brand()
#     try:
#         esg_score = find_esg_value_by_name(brand)
#     except:
#         esg_score = random.randint(0, 100)
#         add_entry_to_collection(brand, esg_score)
#     #esg_score = get_brand()
#
#     # print(get_esg(brand))
#
#     print(f"Brand: {brand}, ESG Score: {esg_score}")
#     # esg_match = re.search(r'\[.*?\]', esg_score)
#     #
#     # if esg_match:
#     #     esg_score_str = match.group(0)
#     #     # Convert the matched string to a list
#     #     # This involves removing the square brackets and splitting the string by comma
#     #     esg_score_array = esg_score_str.strip('[]').split(', ')
#     #     print(esg_score_array)
#     # else:
#     #     print("No ESG score array found in the text.")
