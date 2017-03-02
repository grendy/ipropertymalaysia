#author = grendy-PH
#date   = 9 Desember 2016
import scrapy
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy.http import TextResponse
from scrapy.http import Request
import traceback
import MySQLdb
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import urllib2
import urllib
from pyvirtualdisplay import Display
from ipropertymalay.items import outjson


class ProductSpider(scrapy.Spider):
    name = "iproper"
    allowed_domains = ["https://www.iproperty.com.my/"]
    start_urls = ["https://www.iproperty.com.my"]

    def __init__(self,conn):
        self.conn = conn
        global driver
	    display = Display(visible=0, size=(800,600))
        display.start()
        driver = webdriver.Firefox()
    @classmethod
    def from_crawler(cls,crawler):
        conn=MySQLdb.connect(
            host=crawler.settings['MYSQL_HOST'],
            port=crawler.settings['MYSQL_PORT'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASS'],
            db=crawler.settings['MYSQL_DB'])
        return cls(conn)

    def parse(self, response):
        import pdb;pdb.set_trace()
        cur = self.conn.cursor()
        url = 'https://www.iproperty.com.my'
        try:
            list = ["Apartment/Flat","Condo/Serviced Residence","Terrace/Link/Townhouse","Semi-D/Bungalow",
                    "Residential Land","Shop/Office/Retail Space","Hotel/Resort","Commercial Land","Factory/Warehouse",
                    "Industrial Land","Agricultural Land"]
            for e in range(0,11):
                box = list[e]
                driver.get(url)
                select = Select(driver.find_element_by_id('s_searchBoxPropertyGroupType'))
                select.select_by_visible_text(box)
                driver.find_element_by_id('s_imgBtnSearch').click()
                coy = ""
                while coy != 'done':
                    import pdb;pdb.set_trace
                    a = driver.current_url
                    response = TextResponse(driver.current_url, body=driver.page_source, encoding='utf-8')
                    for i in range(1,27):
                        if i != 5 or i != 10 or i != 16 or i !=21:
                            try:
                                #HARGA
                                harga = response.xpath('//*[contains(@id, "frmSaveListing")]/ul/li[' + str(i) + ']//*[contains(@class, "article-right")]/span/text()').extract_first()
                                harga = int(harga.replace("RM", "").replace(" ", "").replace(",", "").encode('utf-8'))
                                #NAMA
                                nama = response.xpath('//*[contains(@id, "frmSaveListing")]/ul/li[' + str(i) + ']//*[contains(@class, "article-right")]/p[1]/a/text()').extract_first()
                                #PHONE
                                phone = response.xpath('//*[contains(@id, "frmSaveListing")]/ul/li[' + str(i) + ']//*[contains(@class, "article-right")]/p[2]/a').extract()
                                phone = ''.join(phone)
                                phone = phone.split("PL\', \'")[1]
                                phone = phone.split("\'")[0].encode('utf-8').replace("-", "").replace(" ", "")
                                #Description
                                desc = response.xpath('//*[contains(@id, "frmSaveListing")]/ul/li[' + str(i) + ']//*[contains(@class, "article-left")]/p/following-sibling::*/descendant-or-self::text()').extract()
                                desc = ','.join(desc)
                                #Title
                                title = response.xpath('//*[contains(@id, "frmSaveListing")]/ul/li[' + str(i) + ']//*[contains(@class, "article-left")]/h2/a').extract()
                                title = ''.join(title)
                                title = title.split("title=")[1]
                                title = title.split(" onclick")[0].replace("\"", "").encode('utf-8')
                                #Picture
                                linkphoto = response.xpath('//*[contains(@id, "frmSaveListing")]/ul/li[' + str(i) + ']//*[contains(@class, "photo")]/p/a/img/@src').extract_first()
                                photo = linkphoto.split('/')[7]
                                direktori = '/root/scrapy/crawling/ipropertymalay/' + photo
                                urllib.urlretrieve(linkphoto, direktori)
                                #PRINT
                                print "===========++++++=================="
                                print harga
                                print nama
                                print phone
                                print "===========++++++==============="
                                print title
                                print desc
                                print "===========++++++=================="
                                item = outjson()
                                item['harga'] = harga
                                item['nama'] = nama
                                item['phone'] = phone
                                item['title'] = title
                                item['desc'] = desc
                                item['photo'] = photo
                                yield item
                                time.sleep(2)
                            except:pass
                    try:
                        pagination(response)
                        b = driver.current_url
                        if a == b:
                            coy = 'done'
                    except:
                        coy = 'done'
        except:
            print traceback.print_exc()
        cur.close()
        try:
            driver.close()
        except:
            pass
def pagination(response):
    try:
        driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
    except:
        try:
            driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
        except:
            try:
                driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
            except:
                try:
                    driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
                except:
                    try:
                        driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
                    except:
                        try:
                            driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
                        except:
                            driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
