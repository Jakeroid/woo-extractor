import sys
import requests
from bs4 import BeautifulSoup
import csv
import html

# check url argument
url = ''
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input('Please, specify URL of WooCommerce shop: ')

if len(url) == 0:
    sys.exit('Wrong shop URL!')

# set up headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
}

# get shop page
shop_url = url.rstrip('/') + '/shop/'
shop_r = requests.get(shop_url, headers=headers)
shop_page_html = shop_r.text

# find all products links
shop_soup = BeautifulSoup(shop_page_html, 'html.parser')
print('Shop title: ' + str(shop_soup.title))
print('Searching products...')
links = []
for product_tag in shop_soup.select('li.product a.woocommerce-loop-product__link'):
    link_val = product_tag['href']
    links.append(link_val)

# scrape products data
f = open('./output.csv', 'w')
writer = csv.writer(f)
writer.writerow(['title', 'description', 'price', 'img'])
try:
    for link in links:
        product_r = requests.get(link, headers=headers)
        product_soup = BeautifulSoup(product_r.text, 'html.parser')

        product_title = None
        product_title_tag = product_soup.select('.product_title')
        if len(product_title_tag) > 0:
            product_title = product_title_tag[0].text

        product_description = None
        product_description_tag = product_soup.select('.woocommerce-product-details__short-description')
        if len(product_description_tag) > 0:
            product_description = product_description_tag[0].text.strip().replace(' ', '')

        product_price = None
        product_price_tag = product_soup.select('.price')
        if len(product_price_tag) > 0:
            product_price = product_price_tag[0].text.strip()

        product_img = None
        product_img_tag = product_soup.select('.woocommerce-product-gallery img')
        if len(product_img_tag) > 0:
            product_img = product_img_tag[0]['src']

        writer.writerow([product_title, product_description, product_price, product_img])

        print('Found: ' + product_title)
except Exception as e:
    print(e)
finally:
    f.close()
