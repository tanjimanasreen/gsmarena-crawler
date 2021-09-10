# Gsmarena-crawler
This project is consisted of two crawlers built with different python webscraping libraries ( bs4,scrapy and selenium ) which extract data from [gsmarena](www.gsmarena.com) and and its Bangladeshi variant website [gsmarena-bd](www.gsmarena.com.bd) and store the data into a MongoDB Database.

| Website | Crawler |
|:----------:|----------|
| [gsmarena](www.gsmarena.com) | [**gsmareana-selenium**](#Gsmarena-selenium) |
| [gsmarena-bd](www.gsmarena.com.bd) | [**gsmareanabd-bs4**](#bs4) <br> [**gsmareanabd-scrapy**](#Scrapy)  |


## Gsmarenabd-crawler
---
### Scrapy:
This comes with an end to end pipeline that scrapes all the phones' specifications available on [gsmarena.com.bd](www.gsmarena.com.bd) and stores it into the database in a document format. In order to use this, just download the [Scrapy-project](https://github.com/tanjimanasreen/gsmarena-crawler/tree/main/gsmarena-com-bd-crawler/Scrapy-project) folder and run it on your pc.

**Built With:**
- [Scrapy Framework](https://docs.scrapy.org/en/latest/)
- [Pymongo](https://pymongo.readthedocs.io/en/stable/)

### bs4 
This parser can parse all the phones' specifications available on [gsmarena.com.bd](www.gsmarena.com.bd) using python's *bs4 package* and stores it into a json file. In order to use this, just download and run the notebook available [here](https://github.com/tanjimanasreen/gsmarena-crawler/tree/main/gsmarena-com-bd-crawler/Bs4-scraper) in your local pc using [jupyter notebook](https://jupyter.org/) or on [google colab](https://colab.research.google.com/).

**Built With:**
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## Gsmarena-selenium
---
This uses [Selenium](https://selenium-python.readthedocs.io/) webdriver for python to scrape all the phones' specifications available on [gsmarena.com](www.gsmarena.com) and stores it into the database in a document format. In order to use this, just download the [gsmarena-com-crawler](https://github.com/tanjimanasreen/gsmarena-crawler/tree/main/gsmarena-com-crawler) folder and run it on your pc. The environment variables are provided in .env.example file.

**Built With:**
- [Selenium](https://selenium-python.readthedocs.io/)
- [Pymongo](https://pymongo.readthedocs.io/en/stable/)
- [Concurreny](https://docs.python.org/3/library/concurrent.futures.html)

