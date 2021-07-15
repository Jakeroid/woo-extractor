import sys
import requests
from bs4 import BeautifulSoup
import csv


# function scrape products links from beautiful soup
def find_product_links(beautiful_soup):
    result = []
    for product_tag in beautiful_soup.select('li.product a.woocommerce-loop-product__link'):
        link_val = product_tag['href']
        result.append(link_val)
    return result


# get next page if it exist from beautiful soup
def find_next_page_url(beautiful_soup):
    next_page_link = None
    next_page_el = beautiful_soup.select('.page-numbers a.next')
    if len(next_page_el) > 0:
        if next_page_el[0]['href'] is not None:
            next_page_link = next_page_el[0]['href']
    return next_page_link


# get product data from beautiful soup
def get_product_data(beautiful_soup):

    product_title = None
    product_title_tag = beautiful_soup.select('.product_title')
    if len(product_title_tag) > 0:
        product_title = product_title_tag[0].text

    product_description = None
    product_description_tag = beautiful_soup.select('.woocommerce-product-details__short-description')
    if len(product_description_tag) > 0:
        product_description = product_description_tag[0].text.strip().replace(' ', '')

    product_price = None
    product_price_tag = beautiful_soup.select('.price')
    if len(product_price_tag) > 0:
        product_price = product_price_tag[0].text.strip()

    product_img = None
    product_img_tag = beautiful_soup.select('.woocommerce-product-gallery img')
    if len(product_img_tag) > 0:
        product_img = product_img_tag[0]['src']

    return [product_title, product_description, product_price, product_img]


def main():

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
    soup = BeautifulSoup(shop_page_html, 'html.parser')

    # find all products links
    print('Searching products URLs...')
    links = []
    links.extend(find_product_links(soup))
    next_page_url = find_next_page_url(soup)
    while next_page_url is not None:
        print('Found page: ' + next_page_url)
        shop_r = requests.get(next_page_url, headers=headers)
        shop_page_html = shop_r.text
        soup = BeautifulSoup(shop_page_html, 'html.parser')
        links.extend(find_product_links(soup))
        next_page_url = find_next_page_url(soup)
    print('Founded ' + str(len(links)) + ' product URLs!')

    # scrape products data
    f = open('./output.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['title', 'description', 'price', 'img'])
    try:
        for link in links:
            product_r = requests.get(link, headers=headers)
            product_soup = BeautifulSoup(product_r.text, 'html.parser')

            result = get_product_data(product_soup)
            writer.writerow(result)

            print('Found PRODUCT: ' + result[0])
    except Exception as e:
        print(e)
    finally:
        f.close()


# call main function
main()
