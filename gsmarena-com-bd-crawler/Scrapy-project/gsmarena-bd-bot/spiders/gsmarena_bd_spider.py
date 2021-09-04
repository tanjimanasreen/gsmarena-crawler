import scrapy
from ..items import PhoneItem
import unicodedata


class GsmarenaBDSpider(scrapy.Spider):
    name = "gsmbd"
    allowed_domains = ['gsmarena.com.bd']

    def start_requests(self):
        url = 'https://www.gsmarena.com.bd/brands/'

        yield scrapy.Request(url=url, callback=self.parse_brands)

    def parse_brands(self, response):
        urls = response.css('div.product-thumb div.image a ::attr("href")').getall()
        # print(len(urls), urls)
        for url in urls:
            # url = 'https://www.gsmarena.com.bd' + str(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # get all products' links
        product_page_links = response.css('div.product-thumb a ::attr("href")').getall()
        yield from response.follow_all(product_page_links, self.parse_product)

        """ pagination """
        try:
            pagination_links = response.css('ul.pagination li a ::attr("href")').getall()[-1]
            yield response.follow(pagination_links, self.parse)
        except IndexError as ie:
            # logging.info(ie, logging.WARN)
            print(ie)
        except TypeError as te:
            # logging.info(te, logging.WARN)
            print(te)
        except ValueError as ve:
            print(ve)

    def parse_product(self, response):
        product_details = dict()
        product_details['phone_url'] = response.url
        spec_tables = response.css('div.panel-box table.table-striped')
        for table in spec_tables:
            temp = ''
            for t in (table.css('tr')):
                # normalize text
                head = unicodedata.normalize("NFKD", t.css('th ::text').get())
                body = unicodedata.normalize("NFKD", t.css('td ::text').get())

                if head.isspace():
                    head = temp
                    if isinstance(product_details[temp], list):
                        product_details[head].append(body)
                    else:
                        product_details[temp] = [product_details[temp]]
                        product_details[head].append(body)
                else:
                    head = head.strip().lower()
                    head = head.replace(" ", "_")
                    if head[0].isdigit():
                        head = 'headphone_jack'  # mapping item key
                    if not (head == 'category' and body.lower() == 'smart watch'):
                        product_details[head] = body
                temp = head

        # filter out smart watches and feature phones
        if product_details['category'].lower() == 'smart watch':
            pass
        elif product_details['category'].lower() == 'feature phone':
            pass
        else:
            item = PhoneItem()
            key_list = list(item.fields.keys())
            # mapping according to item fields
            for key, val in product_details.items():
                if key in key_list:
                    item[key] = val
            yield item
