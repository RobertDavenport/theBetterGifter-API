import os
import openai
import requests
from bs4 import BeautifulSoup
import re
import json
from fake_useragent import UserAgent

openai.api_key = os.environ['OPENAI_API_KEY']


def generate_suggestion(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    message_content = response.choices[0].message['content']
    return message_content


def massage_response(response):
    pattern = r'Gift (\d+)?\: ([^.]+)\. Explanation: ([^.]+)\.'
    matches = re.findall(pattern, response)
    return [{'Gift': match[1].strip(), 'Explanation': match[2].strip()}
            for match in matches]


def generate_amazonLink(gift):
    splicedGift = gift.split(' ')
    delimter = '+'
    amazonParams = delimter.join(splicedGift)
    return f'https://www.amazon.com/s?k={amazonParams}'


def fetch_amazonProduct(amazonLink):
    ua = UserAgent()
    headers = {'User-Agent': ua.random, 'Accept-Language': 'en-US, en;q=0.5'}
    response = requests.get(amazonLink, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    product = soup.select_one('[data-component-type="s-search-result"]')
    if not product:
        return {}

    title = product.select_one('h2').get_text(strip=True)
    price = product.select_one('.a-offscreen').get_text(strip=True)
    image_url = product.select_one('.s-image').attrs['src']
    link = product.select_one('a.a-link-normal.s-no-outline')['href']
    rating = product.select_one('span.a-size-base').get_text(strip=True)

    return {'title': title, 'price': price, 'imageURL': image_url, 'link': link, 'rating': rating}


def get_gift_details(response):
    # Parse the response string as a list of dictionaries
    gifts = json.loads(response)

    # Create an empty list to store the results
    results = []

    # Loop through each gift and generate its Amazon link and fetch its product
    for gift in gifts:
        amazonLink = generate_amazonLink(gift['gift'])
        product = fetch_amazonProduct(amazonLink)

        # Append the gift details along with its Amazon link and product to the results list
        results.append({
            'gift': gift['gift'],
            'explanation': gift['explanation'],
            'amazonLink': amazonLink,
            'product': product
        })

    return results
