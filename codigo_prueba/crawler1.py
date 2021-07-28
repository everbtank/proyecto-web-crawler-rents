from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Habitacion(Item):
  price = Field()
  address = Field()
  descripcion = Field()
  


class AirbnbCrawlerVertical(CrawlSpider):
  name = "CrawlerVertical"
  custom_settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      
    }
  allowed_domains = ['realtor.com']
 
  start_urls = ['https://www.realtor.com/apartments/New-York_NY','https://www.realtor.com/rentals']



  download_delay = 1
  rules = (
    Rule(LinkExtractor(allow=r'/realestateandhomes-detail'), callback = 'parse_items'),
  )
  #handle_httpstatus_list = [403]

  
    # EL RESPONSE ES EL DE LA URL SEMILLA
  def parse_start_url(self, response): 
        sel = Selector(response)
        rentas = sel.xpath('.//div[@data-testid="property-card"]')
        print("Numero de Resultados", len(rentas))
        
        
  def parse_items(self, response):
    #sel = Selector(response)
    item = ItemLoader(Habitacion(), response)
    item.add_xpath('price', '//div[@class="ldp-header-price"]/div/span[1]/text()')
    item.add_xpath('address', '//div[@id="ldp-address"]/h1/span[1]/text()')
    item.add_xpath('descripcion', '//p[@id="ldp-detail-romance"]/text()')

    #item.add_xpath('huespedes', '//*[@id="site-content"]/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/section/div/div/div/div[1]/div[2]/span[1]/text()', MapCompose(self.procesarHuespedes))

    #item.add_xpath('caracteristicas', '//div[@data-plugin-in-point-id="AMENITIES_DEFAULT"]//div[@class="_1nlbjeu"]/div[1]/text()')
    yield item.load_item()
