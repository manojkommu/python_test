import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
num_pages = 4

data = []

for page in range(1, num_pages + 1):
    url = base_url + str(page)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in product_list:
        product_link = product.find('a', {'class': 'a-link-normal a-text-normal'})
        if product_link is not None:
            product_url = 'https://www.amazon.in' + product_link['href']
        else:
            product_url = 'URL not available'
            continue  # Skip this iteration if URL is not available

        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        if product_name is not None:
            product_name = product_name.text.strip()
        else:
            product_name = 'Product name not available'

        product_price = product.find('span', {'class': 'a-offscreen'})
        if product_price is not None:
            product_price = product_price.text.strip()
        else:
            product_price = 'Price not available'

        product_rating = product.find('span', {'class': 'a-icon-alt'})
        if product_rating is not None:
            product_rating = product_rating.text.split(' ')[0]
        else:
            product_rating = 'Rating not available'

        num_reviews = product.find('span', {'class': 'a-size-base'})
        if num_reviews is not None:
            num_reviews = num_reviews.text.split(' ')[0]
        else:
            num_reviews = 'Number of reviews not available'

        if product_url != 'URL not available':  # Check if URL is valid
            product_response = requests.get(product_url)
            product_soup = BeautifulSoup(product_response.content, 'html.parser')

            product_description = product_soup.find('div', {'id': 'productDescription'})
            if product_description is not None:
                product_description = product_description.text.strip()
            else:
                product_description = 'Product description not available'

            asin = product_soup.find('th', text='ASIN')
            if asin is not None:
                asin = asin.find_next('td').text.strip()
            else:
                asin = 'ASIN not available'

            manufacturer = product_soup.find('th', text='Manufacturer')
            if manufacturer is not None:
                manufacturer = manufacturer.find_next('td').text.strip()
            else:
                manufacturer = 'Manufacturer not available'

        data.append({
            'Product URL': product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': product_rating,
            'Number of Reviews': num_reviews,
            'Description': product_description,
            'ASIN': asin,
            'Manufacturer': manufacturer
        })

        print('Scraped:', product_url)

# Export the data to a CSV file
filename = 'product_data.csv'
fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN',
              'Manufacturer']

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print('Data exported to', filename)