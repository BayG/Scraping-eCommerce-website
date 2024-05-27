import aiohttp  # Added for asynchronous requests
import asyncio  # Added for asynchronous requests
import async_timeout  # Add this import
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import random  # Add this import

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    # Add more user agents
]

proxies = [
    'http://20.235.47.207:3128',
    'http://20.235.159.154:80',
    'http://37.120.192.154:8080',
    'http://178.128.113.118:23128',
    'http://189.240.60.169:9090',
    'http://71.86.129.168:8080',
    'http://71.86.129.137:8080',
    'http://71.86.129.152:8080',
    'http://71.86.129.162:8080',
    'http://71.86.129.160:8080',
    'http://154.127.240.120:64002',
    'http://154.127.240.118:64001',
    'http://71.86.129.131:8080',
    'http://114.129.2.82:8081',
    'http://49.12.150.91:8080',
    'http://20.37.207.8:8080',
    'http://209.15.113.71:80',
    'http://117.250.3.58:8080',
    'http://35.185.196.38:3128',
    'http://200.174.198.86:8888',
    'http://13.56.81.94:3128',
    'http://71.86.129.180:8080',
    'http://223.135.156.183:8080',
    'http://154.236.179.229:1981',
    'http://144.217.131.61:3148',
    'http://144.76.64.184:3128',
    'http://144.76.225.182:3128',
    'http://109.123.230.171:3128',
    'http://85.214.158.184:18123',
    'http://71.86.129.153:8080',
    'http://71.86.129.130:8080',
    'http://71.86.129.167:8080',
    'http://185.217.136.67:1337',
    'http://45.61.163.2:80',
    'http://144.217.119.85:3207'
]


async def fetch(session, url):  # Added asynchronous fetch function
    for _ in range(len(proxies)):  # Try all proxies
        proxy = random.choice(proxies)  # Add proxy of random choices
        try:
            async with async_timeout.timeout(10):  # Correct usage of timeout
                async with session.get(url, headers={'User-Agent': random.choice(user_agents)}, proxy=proxy) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(f"Non-200 status code: {response.status} from proxy {proxy}")
        except (asyncio.TimeoutError, aiohttp.client_exceptions.ClientProxyConnectionError, aiohttp.client_exceptions.ClientHttpProxyError, aiohttp.ClientError) as e:
            print(f"Proxy error: {e}. Retrying with a different proxy...")
    print(f"Failed to fetch {url} with all proxies.")
    return None

async def scrape_tokopedia(url, product_limit):  # Changed to async function
    print(f"Scraping Tokopedia URL: {url}")
    products = []
    page_count = 0
    async with aiohttp.ClientSession() as session:  # Added aiohttp ClientSession
        while len(products) < product_limit and url:
            start_time = time.time()
            html = await fetch(session, url)  # Changed to use asynchronous fetch
            if html is None:
                break  # Exit if there was a timeout

            await asyncio.sleep(random.uniform(1, 5))  # Random delay between requests

            page_load_time = time.time() - start_time
            print(f"Page {page_count + 1} loaded in {page_load_time:.2f} seconds")

            soup = BeautifulSoup(html, 'html.parser')
            start_time = time.time()
            items = soup.select('.css-1asz3by')  # Update this selector
            for item in items:
                name = item.select_one('.css-3um8ox').get_text(strip=True)  # Update this selector
                price = item.select_one('.css-1asz3by').get_text(strip=True)  # Update this selector
                products.append({'Name': name, 'Price': price})
                print(f"Scraped product: {name} - {price}")
                if len(products) >= product_limit:
                    break
            scraping_time = time.time() - start_time
            print(f"Scraping page {page_count + 1} took {scraping_time:.2f} seconds")

            page_count += 1
            next_page = soup.select_one('.css-gvoll6')  # Update this selector for the "Next" button/link
            url = next_page['href'] if next_page else None
    print(f"Found {len(products)} products on Tokopedia.")
    return products[:product_limit]

async def scrape_shopee(url, product_limit):  # Changed to async function
    print(f"Scraping Shopee URL: {url}")
    products = []
    page_count = 0
    async with aiohttp.ClientSession() as session:  # Added aiohttp ClientSession
        while len(products) < product_limit and url:
            start_time = time.time()
            html = await fetch(session, url)  # Changed to use asynchronous fetch
            if html is None:
                break  # Exit if there was a timeout

            await asyncio.sleep(random.uniform(1, 5))  # Random delay between requests

            page_load_time = time.time() - start_time
            print(f"Page {page_count + 1} loaded in {page_load_time:.2f} seconds")

            soup = BeautifulSoup(html, 'html.parser')
            start_time = time.time()
            items = soup.select('.p-2.flex-1.flex.flex-col.justify-between')  # Update this selector
            for item in items:
                name = item.select_one('.space-y-1.mb-1.flex-1.flex.flex-col.justify-between.min-h-\[4rem\]').get_text(strip=True)  # Update this selector
                price = item.select_one('.p-2.flex-1.flex.flex-col.justify-between').get_text(strip=True)  # Update this selector
                products.append({'Name': name, 'Price': price})
                print(f"Scraped product: {name} - {price}")
                if len(products) >= product_limit:
                    break
            scraping_time = time.time() - start_time
            print(f"Scraping page {page_count + 1} took {scraping_time:.2f} seconds")

            page_count += 1
            next_page = soup.select_one('.shopee-icon-button.shopee-icon-button--right')  # Update this selector for the "Next" button/link
            url = next_page['href'] if next_page else None
    print(f"Found {len(products)} products on Shopee.")
    return products[:product_limit]

async def main():  # Changed to async function
    tokopedia_url = 'https://www.tokopedia.com/search?st=&q=snack%20jepang&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='
    shopee_url = 'https://shopee.co.id/search?keyword=snack%20jepang'
    product_limit = 50  # Adjust as needed to reach a total of 100 products combined

    print("Starting scraping process...")
    start_time = time.time()

    tokopedia_products = await scrape_tokopedia(tokopedia_url, product_limit)  # Added await
    shopee_products = await scrape_shopee(shopee_url, product_limit)  # Added await

    all_products = tokopedia_products + shopee_products
    df = pd.DataFrame(all_products)

    os.makedirs('data', exist_ok=True)
    df.to_csv('data/products.csv', index=False)

    end_time = time.time()
    print(f"Data scraping complete. Products saved to data/products.csv")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

# Run the main function
asyncio.run(main())
