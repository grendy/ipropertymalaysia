import scrapy
from logging import exception
import datetime
from kafka import KafkaProducer, KafkaConsumer
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy.http import TextResponse
from pyvirtualdisplay import Display
from impala.dbapi import connect
from selenium.webdriver.common.proxy import *
import traceback
import setting
import MySQLdb
import sys
import json
import demjson

import time


class feedback:
    def __init__(self):
        self.conn = MySQLdb.connect(
            host=setting.host,
            port=setting.port,
            user=setting.user,
            passwd=setting.passwd,
            db=setting.db)
        self.connect = self.conn
        # path_to_chromedriver = 'D://chromedriver'
        # self.driver = webdriver.Chrome(executable_path = path_to_chromedriver)
        # self.driver = webdriver.Chrome()
        # service_args = [setting.proxy]
        # self.driver = webdriver.PhantomJS()#service_args=service_args)
        # myProxy = setting.firefox_proxy
        # proxy = Proxy({
        #     'proxyType': ProxyType.MANUAL,
        #     'httpProxy': myProxy,
        #     'ftpProxy': myProxy,
        #     'sslProxy': myProxy,
        # })
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.driver = webdriver.Firefox()

    def parse(self):
        cur = self.conn.cursor()
        cou = self.conn.cursor()
        try:
            # import pdb;pdb.set_trace()
            count = "select count(*)from bukalapak_url where status_feed = ''"
            sql = "select product_url from bukalapak_url where status_feed = ''"
            cur.execute(sql)
            cou.execute(count)
            results = cur.fetchall()
            b = cou.fetchall()
            terus = str(b).replace(",", "").replace("'", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("L", "")
            print (terus)
            terus = int(terus)
            print (terus)
            count = 0
            for ulang in range(0, terus):
                try:
                    print (ulang)
                    count += 1
                    a = results[ulang]
                    url = str(a).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
                    print "========================"
                    print url
                    self.driver.get(url)
                    response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')
                    # if count == 4:
                    # import pdb;pdb.set_trace()
                    # self.driver.save_screenshot('SCEEN1.png')
                    penjual_url = MySQLdb.escape_string(response.xpath('//*[contains(@id,"mod-product-detail")]/aside/div/article/div[2]/h5/a/@href').extract_first())
                    #//*[@id="mod-product-detail-1"]/aside/div/article/div[2]/h5/a
                    # self.driver.save_screenshot('SCEEN1.png')
                    cek = "select status_feed from bukalapak_url where penjual_url = '{}' limit 1".format(penjual_url)
                    if cek != 'done':
                        status_feed = "done"
                        sql = "UPDATE bukalapak_url SET status_feed = '{}' WHERE penjual_url = '{}'".format(status_feed,penjual_url)
                        cur.execute(sql)
                        self.conn.commit()
                        url = penjual_url.replace("?dtm_source=product_detail&dtm_section=sidebar&dtm_campaign=default","/feedback?feedback_as=as_seller&filter_by=all")
                        print "========================="
                        print url
                        self.driver.get(url)

                        for halaman in range(1, 500):
                            for loop in range(1, 21):
                                response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')
                                nama = response.xpath('/html/body/div[1]/section/div/div[2]/section/ul/li[' + str(loop) + ']/article/div[1]/div/div[2]/div[1]/a/text()').extract_first()
                                if nama == None:
                                    try:
                                        nama = response.xpath('// *[contains(@id,"reskinned_page")]/section/div/div[2]/section[1]/div/ul/li[' + str(loop) + ']/article/div[2]/div/a/text()').extract_first()
                                        nama = nama.encode('utf-8')
                                    except:
                                        nama = "Tanpa Nama"
                                        # // *[contains(@id,"reskinned_page")]/section/div/div[2]/section[1]/div/ul/li[1]/article/div[2]/div/a

                                pesan = response.xpath('/html/body/div[1]/section/div/div[2]/section/ul/li[' + str(loop) + ']/article/div[2]/div/blockquote/p/text()').extract_first()
                                tanggal = response.xpath('/html/body/div[1]/section/div/div[2]/section/ul/li[' + str(loop) + ']/article/div[1]/div/div[2]/div[3]/time/text()').extract_first()
                                try:
                                    tanggal = tanggal.replace("\n","")
                                except:
                                    try:
                                        tanggal = response.xpath('*[contains(@id,"reskinned_page")] / section / div / div[2] / section[1] / div / ul / li[' + str(loop) + '] / article / div[2] / div / time/text()').extract_first()
                                        tanggal = tanggal.encode('utf-8').replace("\n", "")
                                    except:
                                        try:
                                            tanggal = response.xpath('// *[ @ id = "feedback_list"] / ul / li[' + str(loop) + '] / article / div[2] / div / time/text()').extract_first()
                                            tanggal = tanggal.encode('utf-8').replace("\n", "")
                                        except:
                                            try:
                                                tanggal = response.xpath('//*[@id="reskinned_page"]/section/div/div[2]/section[1]/div/ul/li[' + str(loop) + ']/article/div[2]/div/time/text()').extract_first()
                                                tanggal = tanggal.encode('utf-8').replace("\n", "")
                                            except:
                                                tanggal = None
                                try:
                                    tanggal = tanggal.encode('utf-8').replace("\n","")
                                except:
                                    pass
                                if pesan == None:
                                    try:
                                        pesan = response.xpath('// *[ contains(@ id , "reskinned_page")] / section / div / div[2] / section[1] / div[2] / ul / li[' + str(loop) + '] / article / div[2] / p/text()').extract_first()
                                        pesan = pesan.encode('utf-8')
                                    except:pass
                                if pesan == None:
                                    try:
                                        pesan = response.xpath('// *[contains( @ id , "reskinned_page")] / section / div / div[2] / section[1] / div / ul / li[' + str(loop) + '] / article / div[2] / p/text()').extract_first()
                                        #//*[@id="reskinned_page"]/section/div/div[2]/section[1]/div/ul/li[1]/article/div[2]/p
                                        pesan = pesan.encode('utf-8')
                                    except:break
                                akhir = json.dumps(
                                    {'type': 'bukalapak_feedback', 'penjual_url': penjual_url,
                                     'nama': nama, 'pesan': pesan, 'tanggal': tanggal,})
                                try:
                                    for kaf in range(0, 20):
                                        try:
                                            prod = KafkaProducer(bootstrap_servers=setting.broker)
                                            prod.send(setting.kafka_topic, b"{}".format(akhir))
                                            print "=================================================="
                                            print "SUKSES SEND TO KAFKA"
                                            print "=================================================="
                                            print akhir

                                            kaf = 1
                                        except:
                                            pass
                                        if kaf == 1:
                                            break
                                except Exception, e:
                                    print e
                            time.sleep(5)
                            try:
                                coy = url + "&page=" + str(halaman + 1)
                                self.driver.get(coy)
                            except:
                                pass
                            if pesan == None:
                                break
                            # try:
                            #     self.driver.find_element_by_xpath('//a[@class="next_page"]').click()
                            #     time.sleep(3)
                            # except:
                            #     break
                    else:pass
                except Exception, e:
                    print e
                    # prod.send('tokopedia_penjual', b"{}".format(url))
                    # prod.send('tokopedia_feedback', b"{}".format(url))
        except Exception, e:
            print e
        cur.close()
        try:
            self.driver.close()
        except Exception, e:
            print e


if __name__ == '__main__':
    p = feedback()
    p.parse()
