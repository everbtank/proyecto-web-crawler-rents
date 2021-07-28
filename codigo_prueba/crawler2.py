
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Hotel(Item):
   
    Property_Street = Field()
    Property_Address = Field()
    city = Field()
    state=Field()
    codezip = Field()
    bed = Field() 
    bath= Field()
    total_square=Field()
    #days_market=Field()
    #date_sold=Field()
    #garage=Field()
    #data_source=Field()
    year_build=Field()
    sales_price = Field()
    rent_price=Field()
    contacto=Field()
    


class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      
    }


    allowed_domains = ['realtor.com']
 
    start_urls = ['https://www.realtor.com/rentals','https://www.realtor.com/apartments/New-York_NY','https://www.realtor.com/apartments/Miami_FL']
    #handle_httpstatus_list = [403]

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 1
    base_url = 'https://www.realtor.com/'
    DOWNLOADER_MIDDLEWARES = {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,}

   
    rules = (
        Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/realestateandhomes-detail' # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_renta"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

   

    # EL RESPONSE ES EL DE LA URL SEMILLA
    def parse_start_url(self, response): 
        sel = Selector(response)
        hoteles = sel.xpath('.//div[@data-testid="property-card"]')
        print("Numero de Resultados", len(hoteles))

    # Callback de la regla
    def parse_renta(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        
        item.add_xpath('Property_Address', '//*[@id="ldp-address"]/h1/span[1]/text()')
        item.add_xpath('Property_Street', '//*[@id="ldp-address"]/h1/span[2]/text()')
        item.add_xpath('city', '//*[@id="ldp-address"]/h1/span[3]/text()')
        item.add_xpath('state', '//*[@id="ldp-address"]/h1/span[4]/text()')
        item.add_xpath('codezip', '//*[@id="ldp-address"]/h1/span[5]/text()')
        #item.add_xpath('days_market', '//*[@id="ldp-property-meta"]/ul/li[1]/span/text()')
        #item.add_xpath('date_sold', '//div[@id="ldp-property-meta"]/ul/li[1]/span/text()')
        item.add_xpath('bed', '//*[@id="ldp-property-meta"]/ul/li[1]/span/text()')
        item.add_xpath('bath', '//*[@id="ldp-property-meta"]/ul/li[2]/span/text()')
        #item.add_xpath('garage', '//div[@id="ldp-property-meta"]/ul/li[2]/span/text()')
        item.add_xpath('total_square', '//*[@id="ldp-property-meta"]/ul/li[3]/span/text()')
        #item.add_xpath('data_source', '//div[@id="ldp-property-meta"]/ul/li[2]/span/text()')
        
        item.add_xpath('year_build', '//*[@id="key-fact-carousel"]/ul/div[1]/div/div[2]/li/div[2]/text()')
        item.add_xpath('rent_price', '//*[@id="ldp-neighborhood-section"]/div[2]/div/div[1]/p/text()')
        item.add_xpath('sales_price', '//*[@id="ldp-neighborhood-section"]/div[2]/div/div[2]/p/text()')
        item.add_xpath('contacto', '//*[@id="primary_request_more_details"]/h3/span/text()')
        
 
        
        # 
        yield item.load_item()