import requests
from bs4 import BeautifulSoup
import sys

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'

# Number of pages to scrape (each page contains 48 products)
num_pages = 20

for page in range(1, num_pages + 1):
    url = base_url + str(page)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting product details
    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in product_list:
        # Extracting product URL
        product_link = product.find('a', {'class': 'a-link-normal a-text-normal'})
        if product_link is not None:
            product_url = 'https://www.amazon.in' + product_link['href']
        else:
            product_url = 'URL not available'

        # Extracting product name
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        if product_name is not None:
            product_name = product_name.text.strip()
        else:
            product_name = 'Product name not available'

        # Extracting product price
        product_price = product.find('span', {'class': 'a-offscreen'})
        if product_price is not None:
            product_price = product_price.text.strip()
        else:
            product_price = 'Price not available'

        # Extracting product rating
        product_rating = product.find('span', {'class': 'a-icon-alt'})
        if product_rating is not None:
            product_rating = product_rating.text.split(' ')[0]
        else:
            product_rating = 'Rating not available'

        # Extracting number of reviews
        num_reviews = product.find('span', {'class': 'a-size-base'})
        if num_reviews is not None:
            num_reviews = num_reviews.text.split(' ')[0]
        else:
            num_reviews = 'Number of reviews not available'

        # Printing the scraped details
        print('Product URL:', product_url)
        print('Product Name:', product_name)
        try:
            print('Product Price:', product_price)
        except UnicodeEncodeError:
            print('Product Price: (Price contains unsupported characters)')
        print('Rating:', product_rating)
        print('Number of Reviews:', num_reviews)
        print('----------------------------------')