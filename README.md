# Gsmarena-crawler
This project is consisted of two crawlers built with different python webscraping libraries ( bs4,scrapy and selenium ) which extract data from [gsmarena](www.gsmarena.com) and and its Bangladeshi variant website [gsmarena-bd](www.gsmarena.com.bd) and store the data into a MongoDB Database.

| Website | Crawler |
|:----------:|----------|
| [gsmarena](www.gsmarena.com) | [**gsmareana-selenium**](#Gsmarena-selenium) |
| [gsmarena-bd](www.gsmarena.com.bd) | [**gsmareanabd-bs4**](#bs4) <br> [**gsmareanabd-scrapy**](#Scrapy)  |

### Prerequisites

```
python , MongoDB database
```

## Download 

* [**Download source code**](https://github.com/tanjimanasreen/gsmarena-crawler/archive/refs/heads/main.zip "Gsmarena Crawlers source code")
* Clone the repository
  ```
  git clone https://github.com/tanjimanasreen/gsmarena-crawler.git
  ```

## Gsmarenabd-crawler
---
### Scrapy:
This comes with an end to end pipeline that scrapes all the phones' specifications available on [gsmarena.com.bd](www.gsmarena.com.bd) and stores it into a MongoDB database. 

Open the [Scrapy-project](https://github.com/tanjimanasreen/gsmarena-crawler/tree/main/gsmarena-com-bd-crawler/Scrapy-project) folder and run it using scrapy crawl command. Set the Database configuration variables on the scrapy `settings.py` file.

**Built With:**
- [Scrapy Framework](https://docs.scrapy.org/en/latest/) -
- [Pymongo](https://pymongo.readthedocs.io/en/stable/) - 

### bs4 
This parser can parse all the phones' specifications available on [gsmarena.com.bd](www.gsmarena.com.bd) using python's *bs4 package* and stores it into a json file. 

Download and run the notebook available [here](https://github.com/tanjimanasreen/gsmarena-crawler/blob/main/gsmarena-com-bd-crawler/Bs4-scraper/gsmarena_bs4_scraper.ipynb) in your local pc using [jupyter notebook](https://jupyter.org/) or on [google colab](https://colab.research.google.com/).

**Built With:**
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) - 

## Gsmarena-selenium
---
This uses [Selenium](https://selenium-python.readthedocs.io/) package for python to scrape all the phones' specifications available on [gsmarena.com](www.gsmarena.com) and stores it into a MongoDB database. 

Open the [gsmarena-com-crawler](https://github.com/tanjimanasreen/gsmarena-crawler/tree/main/gsmarena-com-crawler) folder and run the `gsmarena_parser.py` file on your pc. The environment variables are provided in `.env.example` file. Set the Database configuration variables.

**Built With:**
- [Selenium](https://selenium-python.readthedocs.io/) - 
- [Pymongo](https://pymongo.readthedocs.io/en/stable/) - 
