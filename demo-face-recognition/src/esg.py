import requests
from bs4 import BeautifulSoup

url = 'https://www.knowesg.com/company-esg-ratings?company-esg-ratings%5Bquery%5D=starbucks'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define the class string exactly as it appears in the HTML
    class_string = "table-container cursor-pointer border-t border-neutral-1 box-border hover:bg-primary-dark hover:bg-opacity-10 transition-colors duration-100 ease-linear py-5 font-normal w-full"

    # Find the div with the specified class string
    target_div = soup.find('div', class_=class_string)
    if target_div:
        print(target_div)
    else:
        print("Div with specified class string not found")
else:
    print(f"Failed to retrieve the webpage: Status code {response.status_code}")
