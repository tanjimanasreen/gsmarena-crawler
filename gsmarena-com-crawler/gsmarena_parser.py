"""
selenium : https://selenium-python.readthedocs.io/


"""
import json
import os
import time

import concurrent.futures
import unicodedata

from os.path import join, dirname
from dotenv import load_dotenv
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CHROME_DRIVER_PATH = "driver/chromedriver.exe"

chrome_options = Options()

# set chrome driver args
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')

# Phone make URL
URL_GSMARENA = "https://www.gsmarena.com/makers.php3"

# DB configuration
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')

# test URL
# URL_GSMARENA = 'https://www.gsmarena.com/xiaomi_redmi_10-11060.php'

"""Parse all brand links"""


def parse_brand_links():
    chrome_driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH,
        options=chrome_options,
    )
    with chrome_driver as driver:
        """Parse brand segment"""
        # timeout
        wait = WebDriverWait(driver, 10)
        driver.get(url=URL_GSMARENA)
        print('init...')
        time.sleep(0.5)

        brand_links = []
        brand_info = {}
        try:
            # wait for visibility of brands section
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "st-text")))
        except TimeoutException as e:
            print("Wait Timed out")
            print(e)
        except NoSuchElementException as ne:
            print("No such element")
            print(ne)
        time.sleep(2)

        try:
            brand_link_rows = driver.find_element_by_class_name('st-text').find_elements_by_tag_name('td')
        except TimeoutException as e:
            print("Wait Timed out")
            print(e)
        except NoSuchElementException as ne:
            print("No such element")
            print(ne)

        try:
            for row in brand_link_rows:
                links = row.find_element_by_tag_name('a').get_attribute("href")
                info = row.find_element_by_tag_name('a').text.strip().split("\n")

                brand_name = info[0].lower()
                num_device = info[1]
                brand_info[brand_name] = num_device
                brand_links.append(links)

        except TimeoutException as e:
            print("Wait Timed out")
            print(e)
        except NoSuchElementException as ne:
            print("No such element")
            print(ne)
        print(brand_links, "\n", len(brand_links))
        print(brand_info, "\n", len(brand_info))
        time.sleep(1)
    return brand_links


"""Parse all product Links from a specific brand"""


def product_links_parser(link_brand):
    """
    :param link_brand:
    :return:
    """
    chrome_driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH,
        options=chrome_options,
    )
    products_link = []
    link_brand = link_brand
    with chrome_driver as driver:
        wait = WebDriverWait(driver, 10)
        while True:
            driver.get(url=link_brand)
            print('init...')
            time.sleep(0.5)
            try:
                # wait for visibility of brands section
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "makers")))
            except TimeoutException as e:
                print("Wait Timed out")
                print(e)
            except NoSuchElementException as ne:
                print("No such element")
                print(ne)
            time.sleep(2)
            # parse all phones' urls
            link_list = []
            try:
                links = driver.find_element_by_class_name('makers').find_elements_by_tag_name('li')
                for link in links:
                    l = link.find_element_by_tag_name('a').get_attribute('href')
                    link_list.append(l)
            except TimeoutException as e:
                print("Wait Timed out")
                print(e)
            except NoSuchElementException as ne:
                print("No such element")
                print(ne)

            products_link.extend(link_list)

            time.sleep(1)

            # Handle pagination
            if len(driver.find_elements_by_class_name('nav-pages')) > 0:
                if len(driver.find_elements_by_class_name('pages-next')) > 0:
                    pagination_element = driver.find_element_by_class_name('pages-next')
                    try:
                        link_brand = pagination_element.get_attribute('href')
                        pagination_element.click()
                        print("---------------------------------------")
                    except ElementClickInterceptedException as ce:
                        print("No such element")
                        break
                else:
                    print("No such element")
                    break
            else:
                break

    return products_link


"""Parse Specifications from all products"""


def product_specs_parser(product_links):
    """

    :param product_links:
    :return:
    """
    # DB init
    client = MongoClient(str(DB_HOST), int(DB_PORT))
    db = client[str(DB_NAME)]
    products_collection = db[str(COLLECTION_NAME)]
    print('db connection init...')
    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH,
        options=chrome_options,
    )
    products_spec = []
    expandable = None
    for url in product_links:
        wait = WebDriverWait(driver, 10)
        time.sleep(2)
        driver.get(url=url)
        print('scraping init...')
        time.sleep(2)
        spec_list = {}
        try:
            # wait for visibility of brands section
            wait.until(EC.presence_of_element_located((By.ID, "specs-list")))
        except TimeoutException as e:
            print("Wait Timed out")
            print(e)
        except NoSuchElementException as ne:
            print("No such element")
            print(ne)
        time.sleep(1)

        # Expand network section
        if expandable is None:
            try:
                expandable = driver.find_element_by_xpath('//*[@id="specs-list"]/table[1]/tbody/tr[1]/td[2]/a')
                expandable.click()
            except ElementClickInterceptedException as ce:
                print("No such element")
            time.sleep(1)
        else:
            pass

        try:
            # parse all specs
            device_spec_tables_rows = driver.find_element_by_id('specs-list').find_elements_by_tag_name('tr')
            extra = " "
            for row in device_spec_tables_rows:
                head = row.find_element_by_class_name('ttl').text
                head = unicodedata.normalize('NFKD', head)
                head = head.strip().lower()

                body = row.find_element_by_class_name('nfo').text
                body = unicodedata.normalize('NFKD', body).strip()

                if len(row.find_elements_by_tag_name('th')) > 0:
                    extra = row.find_element_by_tag_name('th').text
                    extra = unicodedata.normalize('NFKD', extra).strip().lower()
                    extra = extra.replace(" ", "_")

                if len(head) == 0 and not extra.isspace():
                    head = extra
                    spec_list[head] = body
                elif head.replace(" ", "_") in list(spec_list.keys()) and not extra.isspace():
                    new_head = extra + "_" + head.replace(" ", "_")
                    spec_list[new_head] = body
                else:
                    head = head.replace(" ", "_")
                    spec_list[head] = body
        except TimeoutException as e:
            print("Wait Timed out")
            print(e)
        except NoSuchElementException as ne:
            print("No such element")
            print(ne)

        time.sleep(1)
        spec_list['url'] = url
        products_spec.append(spec_list)

    # insert phone specs into mongodb collection
    product_ids = products_collection.insert_many(products_spec).inserted_ids
    print(len(product_ids), "inserted...")
    client.close()
    driver.close()
    driver.quit()


"""Collecting all the products' links from all brands"""


def collect_phone_links():
    all_products_links = []
    brand_links = parse_brand_links()
    for brand_link in brand_links:
        product_links = product_links_parser(brand_link)
        all_products_links.extend(product_links)

    with open('data/all_product_links_01_09_21.json', 'w') as outfile:
        json.dump(all_products_links, outfile, indent=4)


"""Removing Watches' Links"""


def remove_watch_links():
    watch_links = []
    with open('data/all_product_links_01_09_21.json', 'r') as outfile:
        links = json.load(outfile)

    for link in links:
        if 'watch' in link:
            watch_links.append(link)
        else:
            pass

    phone_links = list(set(links) - set(watch_links))

    with open('data/all_phone_links_02_09_21.json', 'w') as outfile:
        json.dump(phone_links, outfile, indent=4)
    print("Done Dumping Phones")

    with open('data/all_watch_links_02_09_21.json', 'w') as outfile:
        json.dump(watch_links, outfile, indent=4)
    print("Done Dumping Watches")


# Split all phone links into a list with 10 chunks for concurrent operation
with open('all_phone_links_02_09_21.json', 'r') as outfile:
    phone_links = json.load(outfile)

list_chunked_phone_links = [phone_links[x:x + 1000] for x in range(0, len(phone_links) - 2, 1000)]
print(len(list_chunked_phone_links), len(list_chunked_phone_links[10]))


# run 10 drivers concurrently
def run_all(phone_links):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(product_specs_parser, phone_links)


def main_func():
    start_time = time.time()
    t_start = time.localtime()
    run_all(list_chunked_phone_links)
    duration = time.time() - start_time
    print(f"start time : {time.strftime('%H:%M:%S', t_start)}, \n End Time : {time.strftime('%H:%M:%S')} ")
    print(f"Scraped {len(phone_links)} in {duration} seconds")


# collect_phone_links() # to collect and dump all products links
# remove_watch_links() # remove watch links from all product links
main_func()  # to crawl phones' specs and dump to mongodb
