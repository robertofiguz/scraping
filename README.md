# Scraping
## Tools:
  - [scrapy](https://scrapy.org/)
  - [zyte](https://www.zyte.com/) - Paid crawling hub - runs scrapy spiders

## Sugested reads:
- [Crawl the web politely](https://www.zyte.com/blog/how-to-crawl-the-web-politely-with-scrapy/)
- [5 useful tips to use scrapy](https://medium.com/geekculture/5-useful-tips-while-working-with-python-scrapy-6beb59119188)

## Sample:
  - ## Crawler like:
    - This code will crawl all pages in the worten website by entering every link on every page as long as its domain is "worten.pt" - how deep the crawling goes can be defined in the ```settings.py``` (will be explained ahead)

```python
import scrapy
import logging
import re
class Worten(scrapy.Spider):
    name = 'worten'
    allowed_domains = ['worten.pt']
    start_urls = ["https://www.worten.pt/"]
    urls = []
    merchants = []
    logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response):
        self.log("Started")
        yield scrapy.Request(url="https://www.worten.pt/diretorio-de-categorias", callback=self.parse_cat)


    def parse_cat(self, response):
        urls = response.css('.header__submenu-third-level-sitemap::attr(href)').extract()
        for url in urls:
            self.log("going for cat: " + str(url))

            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        urls = (response.css('.w-product__title::attr(href)').extract())
        for url in urls:
            url = response.urljoin(url)
            self.log("Going to product " + url)
            yield scrapy.Request(url=url, callback=self.parse_merchants)


    def parse_merchants(self, response):


            yield {
                'old-price': response.css(".w-product__price__old"),
                'price': response.css('.w-product__price'),
                'title': response.css('.pdp-product__title'),
                'about': response.css('.w-product-about'),
                'details': response.css('.w-product-details'),

            }
```

  - ## Scraping:
    - For more specific websites (smaller websites or where we can get a more defined list of pages) we can more actively specify the scraping behaviour and steps by defining all the links it's going to.

```python

import scrapy
import logging
import re
class futah(scrapy.Spider):
    name = 'futah'
    allowed_domains = ['futah.world']
    product_urls = ['
    https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/match-no-futuro-pack-2-toalhas',
'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/match-na-floresta-pack-2-toalhas', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/match-no-cafe-pack-2-toalhas', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/match-no-oceano-pack-2-toalhas', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/cangas/wwf-hippocampus-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/cangas/wwf-lynx-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/cangas/guadiana-castanha-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/cangas/formosa-mocha-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/cangas/formosa-violeta-e-verde-agua-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/cangas/formosa-coral-e-pessego-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/cangas/barra-cinza-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/cangas/barra-amarela-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/pareo/supertubos-coral-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/pareo/supertubos-mostarda-toalha-individual', 'https://www.futah.world/pt/toalhas-de-praia/toalhas-de-praia-individuais/pareo/supertubos-violeta-toalha-individual',
    [...] 
    ,'vestuario-e-acessorios/mochilas/mochila-preta-graphite'
]

    start_urls = product_urls
    urls = []
    merchants = []
    logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response):

        allContent =response.css('.accordion .accordion-navigation .content .accordion-titulo').xpath('text()').extract()
        allDescs = response.css('[class*="column"] + [class*="column"]:last-child').xpath('text()').extract()
        imagesFinal = []
        allContentFinal = []
        allDescsFinal = []
        for i in allContent:
            allContentFinal.append(i.replace("\r\n","").strip())
        for i in allDescs:
            allDescsFinal.append(i.replace("\r\n","").strip())

        specs = dict(zip(allContentFinal, allDescsFinal))

        images = response.xpath('/html/body/div[2]/div[1]/div[2]/div/div/div/div/section/div[1]/div/div[2]/div[1]/div[1]/div//img/@src').extract()

        yield {
            "Title":response.css('#main-container #area-produto .produto-top-wrapper .produto-detalhes-wrapper .produto-detalhes-inner-wrapper h1, #dialog-quick-buy #area-produto .produto-top-wrapper .produto-detalhes-wrapper .produto-detalhes-inner-wrapper h1::text').xpath('text()').extract_first(),
            "Price":response.css('.price::text').extract_first(),
            "Description": response.xpath('/html/body/div[2]/div[1]/div[2]/div/div/div/div/section/div[1]/div/div[2]/div[2]/div/div[5]/p//text()').extract_first(),
            "Specifications": specs,
            "images": images
        }
```
    
# Obtaining urls:
  - website map
  - getting all categories and heading from there
  - getting all products:
    -  [futtah.world]('https://www.futah.world/en/all')
        
        Futtah has an "all products page" even though, its content is dynamically loaded therefore my strategy was manually loading the page fully and download its HTML. Afterwards, I loaded the local page into scrapy shell(instructions ahead) and extracted the links as seen in the example above.
  - In other cases small details such as the query in the URL allow us to increment the number of items per page indefinitely making the job much easier.
  
  - For websites with pagination we can detect the "next page" url and scrape it using recursion.
  
# Using scrapy shell details extraction:
  - scrapy shell is a shell command that runs in python and can be used to debug and build the spiders. To start scrapy you can use the command:
    ``` 
    scrapy shell website_url
    ```
    This will download the webpage. Now we can access the website properties and the request details.

    There are 2 ways to access the page's elements, using XPath and CSS. This can be copied or found by using the browser developer tools. The most common way I use is using the elements CSS class. CSS and XPath can be used together in sequence as well. After getting to the element we can access its properties example: 
    
    Text:
    ``` 
    ::text
    ``` 
    Images:
    ```  
    ::attr(src)
    ```
    URLs:
    ```
    ::attr(href)
    ```
    We can then extract the information using the method: 
    ``` 
    .extract()
    ```
    If we only want the first occurrence or there is only one occurrence we can use:
    ``` 
    .extract_first()
    ```

# Running a spider
  To run a spider and save the results as a JSON navigate to its path and run:
    
    scrapy crawl script_name -o filename.json
  To save as a CSV:
    
    scrapy crawl script_name -o filename.csv

# Scrapy settings
- Inside the spiders folder exists a settings.py
- Suggested modifications:
    - ``` ROBOTSTXT_OBEY = False ```
    - Setting the ```USER_AGENT``` either manualy or if necessary randomly
    - ```FEED_EXPORT_ENCODING = 'utf-8'```
    - ```AUTOTHROTTLE_ENABLED = True```
    - If doing a crawl where it follows all the links setting ```DEPTH_LIMIT = 3``` or any other adequate value
- In the settings file middlewares can also be configures example: Proxy managers(ex: [crawlera](https://www.zyte.com/smart-proxy-manager/), zyte's paid proxy manager), [download_middlewares](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html) etc.

