
from scrapy.item import Field, Item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.loader import ItemLoader


class RentaItem(Item):
    address=Field()
    price=Field()
    city=Field()
    
    
class RentaCrawler(CrawlSpider):
    name='RentaCrawler'
    custom_settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      
    }
    
    allowed_domains = ['realtor.com']
 
    start_urls = ['https://www.realtor.com/rentals','https://www.realtor.com/apartments/New-York_NY','https://www.realtor.com/apartments/Miami_FL']
        
    download_delay = 1
    rules = (
        Rule(LinkExtractor(allow=r'/realestateandhomes-detail'), callback = 'parse_items'),
      )
    
    base_url = 'https://www.realtor.com/'
    DOWNLOADER_MIDDLEWARES = {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,}
    handle_httpstatus_list = [403]
    
    def parse_items(self,response):
        item=ItemLoader(RentaCrawler(),response)
        item.add_xpath('price','//span/text()')
        #item.add_xpath('price','//*[@id="site-content"]/div/div[1]/div[3]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/span[1]/text()')
        #item.add_xpath('city','//*[@id="site-content"]/div/div[1]/div[2]/div[2]/div/div/div/div/section/div[1]/span/h1/text()')
        yield item.load_item()
        
    
    
    
   