import requests

sub_id = "37f471e4-cc80-4dd0-97b7-49489f79a8d5"
search_url = "https://api.bing.microsoft.com/v7.0/search"

def get_esg(brand):
    search_term = f"What is the ESG score of {brand}"
    headers = {"Ocp-Apim-Subscription-Key": sub_id}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results