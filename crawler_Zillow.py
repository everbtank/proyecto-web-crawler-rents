from scrapy.selector import Selector
from twisted.internet import reactor 
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd
from pandas import ExcelWriter

        
class RentaCrawler(CrawlSpider):
    name = 'RentaCrawlerZillow'
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20,
        'LOG_ENABLED': True
    }

 
    download_delay=1
 
    allowed_domains = ['zillow.com']
 
    start_urls=['https://www.zillow.com/homes/New-York,-NY_rb/','https://www.zillow.com/homes/Charlotte,-NC_rb/','https://www.zillow.com/homes/for_rent/']
 
    rules = (
      Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
         LinkExtractor(
            allow=r'/homes'
            # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
         ), follow=True),
      Rule(  # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
         LinkExtractor(
            allow=r'/homedetails'
         ), follow=True,
         callback='parse_renta'),
 
   )
    
 
    # EL RESPONSE ES EL DE LA URL SEMILLA
    def parse_start_url(self, response): 
        sel = Selector(response)
        rentas = sel.xpath('.//div[@class="search-page-list-header"]')
        print("Buscando resultados: ", len(rentas)," encontrado ")


    def parse_renta(self, response):
        
        sel = Selector(response)
       
        Property_Address=sel.xpath('//*[@id="ds-chip-property-address"]/span[1]/text()[1]').get()
        city=sel.xpath('//*[@id="ds-chip-property-address"]/span[2]/text()[2]').get()
        #state=sel.xpath('//*[@id="ds-chip-property-address"]/span[2]/text()[2]').get()
        #codezip=sel.xpath('//*[@id="ds-chip-property-address"]/span[2]/text()[3]').get()

        bed=sel.xpath('//div[@class="ds-bed-bath-living-area-header"]/span/span[1]/span[1]/text()').get()
        bath=sel.xpath('//div[@class="ds-bed-bath-living-area-header"]/span/span[3]/span[1]/text()').get()
        total_square= sel.xpath('//div[@class="ds-bed-bath-living-area-header"]/span/span[5]/span[1]/text()').get()
                               
        price= sel.xpath('//*[@id="ds-container"]/div[4]/div[1]/div/div[1]/div/div/span/span/span[1]/text()').get()
        year_build= sel.xpath('//*[@id="1624060800000"]/td[1]/span/text()').get()
        sales_price= sel.xpath('//*[@id="ds-home-values"]/div/div[1]/div[2]/div[3]/div/svg/g[2]/g[3]/text()').get()
        garage= sel.xpath('//*[@id="ds-data-view"]/ul/li[3]/div/div/div[1]/ul/li[6]/span[2]/text()').get()
          
        #price = price.replace('\n', '').replace('\r', '').strip()
        #sales_price = sales_price.replace('\n', '').replace('\r', '').strip()
        #garage = garage.replace('\n', '').replace('\r', '').strip()
    
    
        #Guardado de datos en un archivo
        f = open('./zillow_csv/renta03a.csv', 'a')
       
        
        #f.write(Property_Address + ","+","+city + ","+state +","+codezip +","+bed +","+bath +","+total_square + ","+price+","+sales_price+","+garage+"\n")
        f.write(Property_Address +","+city+"\n")
        f.close()
        
      
        
        print('Property_Address: '+Property_Address)

        print('city, state, zip : '+city)
        #print('state: '+state)
        #print('code zip: '+codezip)
        print('bed: '+bed)
        print('bath: '+bath)
        print('total square: '+total_square)
        print('year build: '+year_build)
        print('rent price: '+price)
        print('sales price:'+sales_price)
        print('parking: '+garage)
        
        print()

        # No necesito hacer yield. El yield me sirve cuando voy a guardar los datos
        # en un archivo, corriendo Scrapy desde Terminal

# Logica para correr una extraccion de Scrapy periodicamente. Es decir, automatizarla.

print("\n========== Crawler Renta ===========\n")
runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(RentaCrawler)) # Para Investigar: Funciones Anonimas en Python
task.start(2) # Tiempo en segundos desde la primera corrida del programa para repetir la extraccion
reactor.run()

df = pd.read_csv('./zillow_csv/renta03a.csv',
                 skiprows = 1,
                 names=['Property Address', 'Property Street', 'City', 'State', 'Code zip', 'Bed','Bath','Total square','Year build','Price min','Price max','Sales price','Contacto'])

df.to_excel("zillow_output.xlsx")  
print(df)
