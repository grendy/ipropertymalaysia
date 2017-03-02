import scrapy
import json
import time
from scrapy.http import FormRequest
# from kafka import KafkaProducer
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy.http import TextResponse
import traceback
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
import MySQLdb

import time


class ProductSpider(scrapy.Spider):
    name = "coy"
    allowed_domains = ["https://bukalapak.com"]
    start_urls = ["https://www.bukalapak.com/products"]

    def __init__(self,conn):
        self.conn = conn
        # path_to_chromedriver = 'D://chromedriver'
        # self.driver = webdriver.Chrome(executable_path = path_to_chromedriver)
        self.driver = webdriver.PhantomJS()
        # display = Display(visible=0, size=(800,600))
        # display.start()
        # self.driver = webdriver.Firefox()

    @classmethod
    def from_crawler(cls, crawler):
        conn = MySQLdb.connect(
            host=crawler.settings['MYSQL_HOST'],
            port=crawler.settings['MYSQL_PORT'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASS'],
            db=crawler.settings['MYSQL_DB'])
        return cls(conn)

    def parse(self, response):
        cursor = self.conn.cursor()
        try:
            a = 0
            for tidur in range(0, 100):
                time.sleep(1)
                try:
                    sql = "select url from bukalapak_category"
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for ulang in range(0, 21):
                        a = results[ulang]
                        url = str(a).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
                        print "====================================="
                        print(url)
                        print "====================================="
                        self.driver.get(url)
                        # import pdb;pdb.set_trace()
                        try:
                            for halaman in range(0, 5000):
                                try:
                                    count = 0
                                    for i in range(0,61):

                                        response = TextResponse(url=response.url, body=self.driver.page_source,encoding='utf-8')
                                        # // *[ @ id = "mod-product-list-5"] / li[1] / div / article / div[3] / h3 / a
                                        product_url = response.xpath('//*[contains(@id,"mod-product-list")]/li[' + str(i) + ']/div/article/div[3]/h3/a/@href').extract_first()
                                        penjual_url = response.xpath('//*[contains(@id,"mod-product-list")]/li[' + str(i) + ']/div/article/div[3]/div[1]/div/h5/a/@href').extract_first()
                                        #//*[@id="mod-product-list-8"]/li[13]/div/article/div[3]/div[1]/div/h5/a
                                        count +=1
                                        if count == 77:
                                            import pdb;pdb.set_trace()
                                        else:
                                            print count
                                            try:
                                                if "https://www.bukalapak.com" in product_url:
                                                    status = ""
                                                    status_feed = ""
                                                    penjual_url = "https://www.bukalapak.com" + penjual_url + "?dtm_source=product_detail&dtm_section=sidebar&dtm_campaign=default"
                                                    product_url = product_url.encode('utf-8')
                                                    sql = "INSERT INTO `bukalapak_url`(`product_url`,`penjual_url`,`status`,`status_feed`) VALUES ('{}','{}','{}','{}') ".format(product_url,penjual_url,status,status_feed)
                                                    cursor.execute(sql)
                                                    self.conn.commit()
                                                    print "======================================="
                                                    print product_url
                                                    print "INSERT SUKSES"
                                                    print "======================================="
                                                else:
                                                    pass
                                            except:
                                                try:
                                                    if penjual_url != None:
                                                        sql = "UPDATE bukalapak_url SET penjual_url = '{}' WHERE product_url = '{}'".format(penjual_url, product_url)
                                                        cursor.execute(sql)
                                                        self.conn.commit()
                                                        print "============================="
                                                        print product_url
                                                        print penjual_url
                                                        print "UPDATE SUKSES"
                                                        print "============================="
                                                    else:pass
                                                except:
                                                    print "==============================================================================="
                                                    print "Data Duplicate"
                                                    print product_url
                                                    print "==============================================================================="
                                                    pass
                                except:
                                    pass
                                for lanjut in range(0, 100):
                                    time.sleep(1)
                                    self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
                                    time.sleep(1)
                                    self.driver.find_element_by_xpath('/html/body').send_keys(Keys.PAGE_UP)
                                    time.sleep(1)
                                    self.driver.find_element_by_xpath('/html/body').send_keys(Keys.PAGE_UP)
                                    time.sleep(1)
                                    try:
                                        self.driver.find_element_by_xpath('//*[@id="display_product_search"]/div[3]/div[1]/a[8]').click()
                                        # //*[@id="display_product_search"]/div[3]/div[1]/a[7]
                                        time.sleep(7)
                                        url = self.driver.current_url
                                        break
                                    except:
                                        self.driver.find_element_by_xpath('//*[@id="display_product_search"]/div[3]/div[1]/a[7]').click()
                                        time.sleep(7)
                                        url = self.driver.current_url
                                        break
                        except:
                            pass
                except:
                        pass

        except:
            pass
        db.close()
        try:
            self.driver.close()
        except:
            pass
