# GSMARENA-CRAWLER
Here is a collection of crawlers which can crawl [gsmarena](www.gsmarena.com) and [gsmarena.com.bd](www.gsmarena.com.bd). After crawling the data is storedPymongo into a [Mongodb](https://www.mongodb.com/) database.

## GSMARENA.COM.BD-CRAWLER
---
### With Scrapy Framework:
This comes with an end to end pipeline that scrapes all the phones' specifications available on [gsmarena.com.bd](www.gsmarena.com.bd) and stores it into the database in a document format. In order to use this, just download the [Scrapy-project](https://github.com/tanjimanasreen/gsmarena-crawler/tree/main/gsmarena-com-bd-crawler/Scrapy-project) folder and run it on your pc.

**Built With:**
- [Scrapy Framework](https://docs.scrapy.org/en/latest/)
- [Pymongo](https://pymongo.readthedocs.io/en/stable/)

### With BeautifulSoup4:
This parser can parse all the phones' specifications available on [gsmarena.com.bd](www.gsmarena.com.bd) using python's *bs4 package* and stores it into a json file. In order to use this, just download and run the notebook **gsmarena_bs4_scraper.ipynb** in your local pc using [jupyter notebook](https://jupyter.org/) or on [google colab](https://colab.research.google.com/).

**Built With:**
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## GSMARENA.COM-CRAWLER
---
This uses [Selenium](https://selenium-python.readthedocs.io/) webdriver for python to scrape all the phones' specifications available on [gsmarena.com](www.gsmarena.com) and stores it into the database in a document format. In order to use this, just download the [gsmarena-com-crawler](https://github.com/tanjimanasreen/gsmarena-crawler/tree/main/gsmarena-com-crawler) folder and run it on your pc. The environment variables are provided in .env.example file.

**Built With:**
- [Selenium](https://selenium-python.readthedocs.io/)
- [Pymongo](https://pymongo.readthedocs.io/en/stable/)
- [Concurreny](https://docs.python.org/3/library/concurrent.futures.html)

