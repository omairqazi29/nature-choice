import os.path

from openai import OpenAI

client = OpenAI(api_key='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')

# Set your OpenAI API key here

def get_brand_from_description(description):
    try:
        with open('test.jpg', 'rb') as file1:
            response = client.chat.completions.create(model="gpt-4-vision-preview",# Replace with the appropriate model, such as GPT-4 if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": f"What brand is most likely associated with this image: {description}?"}
            ])
            return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error in brand identification"


def get_esg_score(brand):
    try:
        response = client.chat.completions.create(model="gpt-4-vision-preview",  # Replace with the appropriate model, such as GPT-4 if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"What is the ESG score of {brand}? return in the format [brand (string), esg category (Good/Average/Bad) (string), esg score out of 100 (integer)] give the best score"}
        ])
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error in getting ESG score"


# Example usage
if __name__ == "__main__":
    description = "https://pbs.twimg.com/media/FLhJVtSXoAY2x-q.jpg:large"
    brand = get_brand_from_description(description)
    esg_score = get_esg_score(brand) if brand else "Brand not identified"

    print(f"Brand: {brand}, ESG Score: {esg_score}")