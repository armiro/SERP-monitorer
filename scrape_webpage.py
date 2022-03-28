# scrape webpage
import scrapy
from scrapy.crawler import CrawlerProcess
# text cleaning
import re

class serp_to_csv(scrapy.Spider):
    name = "SERPToCsv"
    start_urls = ['https://www.godaddy.com/domainsearch/find?checkAvail=1&domainToCheck=goaheadboys']
    custom_settings = {
        'ITEM_PIPELINES': {
            '__main__.ExtractFirstLine': 1
        },
        'FEEDS': {
            'serp.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }
    

    def parse(self, response):
        """parse data from urls"""
        yield response.xpath('//div[@class="d-inline-flex flex-grow-1 flex-column justify-content-center"]/text()').extract()
        
#         for quote in response.css('div.d-inline-flex flex-grow-1 flex-column justify-content-center > span > span > span'):
#             yield {'quote': quote.extract()}

class ExtractFirstLine(object):
    def process_item(self, item, spider):
        """text processing"""
        lines = dict(item)["quote"].splitlines()
        first_line = self.__remove_html_tags__(lines[0])

        return {'quote': first_line}

    def __remove_html_tags__(self, text):
        """remove html tags from string"""
        html_tags = re.compile('<.*?>')
        return re.sub(html_tags, '', text)

process = CrawlerProcess()
process.crawl(serp_to_csv)
process.start()