import os
import openai
import requests
from bs4 import BeautifulSoup
import re

openai.api_key = os.environ['OPENAI_API_KEY']

def generate_suggestion(prompt: str)->str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text



def massage_response(response):
    pattern = r'Gift Suggestion (\d+)?\: ([^.]+)\. Explanation: ([^.]+)\.'
    matches = re.findall(pattern, response)
    return [{'Gift': match[1].strip(), 'Explanation': match[2].strip()}
            for match in matches]

def generate_amazonLink(gift):
    splicedGift = gift.split(' ')
    delimter = '+'
    amazonParams = delimter.join(splicedGift)
    return f'https://www.amazon.com/s?k={amazonParams}'


def fetch_amazonProduct(amazonLink):
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    response = requests.get(amazonLink, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    product = soup.select_one('[data-component-type="s-search-result"]')
    if not product:
        return {}

    title = product.select_one('h2').get_text(strip=True)
    price = product.select_one('.a-offscreen').get_text(strip=True)
    image_url = product.select_one('.s-image').attrs['src']

    return {'title': title, 'price': price, 'imageURL': image_url}


def get_gift_details(response):
    # extract gift details from the response
    gifts = massage_response(response)

    print(gifts)

    # Create an empty list to store the results
    results = []

    # Loop through each gift and generate its Amazon link and fetch its product
    for gift in gifts:
        amazonLink = generate_amazonLink(gift['Gift'])
        product = fetch_amazonProduct(amazonLink)

        # Append the gift details along with its Amazon link and product to the results list
        results.append({
            'gift': gift['Gift'],
            'explanation': gift['Explanation'],
            'amazonLink': amazonLink,
            'product': product
        })

    return results
