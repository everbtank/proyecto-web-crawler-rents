from scrapy.selector import Selector
from twisted.internet import reactor 
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd
from pandas import ExcelWriter

    
    
class RentaCrawler(CrawlSpider):
    name = 'RentaCrawler'
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20,
        'LOG_ENABLED': True
    }

    
    allowed_domains = ['realtor.com']
 
    #start_urls = ['https://www.realtor.com/rentals','https://www.realtor.com/apartments/New-York_NY','https://www.realtor.com/apartments/Miami_FL','https://www.realtor.com/apartments/Chicago_IL']
    start_urls = ['https://www.realtor.com/rentals']
    handle_httpstatus_list = [403]

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
        rentas = sel.xpath('.//div[@data-testid="property-card"]')
        print("Buscando resultados:   ", len(rentas)," encontrados ")


    def parse_renta(self, response):
        
        sel = Selector(response)
       
        Property_Address=sel.xpath('//*[@id="ldp-address"]/h1/span[1]/text()').get()
        Property_Street=sel.xpath('//*[@id="ldp-address"]/h1/span[2]/text()').get()
        city=sel.xpath('//*[@id="ldp-address"]/h1/span[3]/text()').get()
        state=sel.xpath('//*[@id="ldp-address"]/h1/span[4]/text()').get()
        codezip=sel.xpath('//*[@id="ldp-address"]/h1/span[5]/text()').get()
        bed=sel.xpath('//*[@id="ldp-property-meta"]/ul/li[1]/span/text()').get()
        bath=sel.xpath('//*[@id="ldp-property-meta"]/ul/li[2]/span/text()').get()
        total_square= sel.xpath('//*[@id="ldp-property-meta"]/ul/li[3]/span/text()').get()
                               
        #year_build= sel.xpath('//div[@class="owl-stage"]/div[2]/li/div[2]/text()').get()
        price_min= sel.xpath('//*[@id="ldp-pricewrap"]/div/div/span[1]/text()').get()
        price_max= sel.xpath('//*[@id="ldp-pricewrap"]/div/div/span[2]/text()').get()
        sales_price= sel.xpath('//*[@id="ldp-neighborhood-section"]/div[2]/div/div[2]/p/text()').get()
        contacto= sel.xpath('//*[@id="primary_request_more_details"]/h3/span/text()').get()
          
        price_min = price_min.replace('\n', '').replace('\r', '').strip()
        price_max = price_max.replace('\n', '').replace('\r', '').strip()
        sales_price = sales_price.replace('\n', '').replace('\r', '').strip()
        contacto = contacto.replace('\n', '').replace('\r', '').strip()
    
    
        # Guardado de datos en un archivo
        f = open('./realtor_csv/excel1b.csv', 'a')
       
        #f.write(Property_Address + ","+ Property_Street+","+city + ","+state +","+codezip +","+bed +","+bath +","+total_square +","+ year_build +","+rent_price+","+ sales_price+","+contacto+"\n")
        f.write(Property_Address + ","+ Property_Street+","+city + ","+state +","+codezip +","+bed +","+bath +","+total_square + ","+price_min+","+price_max+","+sales_price+","+contacto+"\n")
        f.close()
        
      
        
        print('Property_Address: '+Property_Address)
        print('Property_Street: '+Property_Street)
        print('city: '+city)
        print('state: '+state)
        print('code zip: '+codezip)
        print('bed'+bed)
        print('bath'+bath)
        print('total square:'+total_square)
        #print('year build: '+year_build)
        print('rent price min: '+price_min)
        print('rent price max: '+price_max)
        print('sales price:'+sales_price)
        print('contacto: '+contacto)
        
        print()

        # No necesito hacer yield. El yield me sirve cuando voy a guardar los datos
        # en un archivo, corriendo Scrapy desde Terminal

# Logica para correr una extraccion de Scrapy periodicamente. Es decir, automatizarla.

print("\n========== Crawler Renta ===========\n")
runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(RentaCrawler)) # Para Investigar: Funciones Anonimas en Python
task.start(2) # Tiempo en segundos desde la primera corrida del programa para repetir la extraccion
reactor.run()

df = pd.read_csv('./realtor_csv/excel1b.csv',
                 skiprows = 1,
                 names=['Property Address', 'Property Street', 'City', 'State', 'Code zip', 'Bed','Bath','Total square','Year build','Price min','Price max','Sales price','Contacto'])

df.to_excel("realtor_output.xlsx")  
print(df)


