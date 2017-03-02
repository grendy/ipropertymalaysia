import scrapy
from logging import exception
import datetime
from kafka import KafkaProducer, KafkaConsumer
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
from scrapy.http import TextResponse
from pyvirtualdisplay import Display
from scrapy.utils.project import get_project_settings
from impala.dbapi import connect
import setting
import traceback
import MySQLdb
import sys
import json
import demjson

import time


class producer:
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
        # driver.get("http://www.google.com")
        # service_args = [setting.proxy]
        # self.driver = webdriver.PhantomJS(service_args = service_args)
        myProxy = setting.firefox_proxy
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'ftpProxy': myProxy,
            'sslProxy': myProxy,
        })
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.driver = webdriver.Firefox(proxy=proxy)
    def parse(self):
        cur = self.conn.cursor()
        cou = self.conn.cursor()
        try:
            # import pdb;pdb.set_trace()
            count = "select count(*)from bukalapak_url where status = ''"
            sql = "select product_url from bukalapak_url where status = ''"
            cur.execute(sql)
            cou.execute(count)
            results = cur.fetchall()
            b = cou.fetchall()
            terus = str(b).replace(",", "").replace("'", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("L", "")
            print (terus)
            terus = int(terus)
            print "============================================"
            print (terus)
            # import pdb;pdb.set_trace()
            count = 0
            for ulang in range(0, terus):
                try:
                    print (ulang)
                    count += 1
                    a = results[ulang]
                    url = str(a).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
                    try:
                        self.driver.get(url)
                        time.sleep(5)
                        response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')
                        # import pdb;pdb.set_trace()
                        try:
                            #ambil detail product dan penjual
                            # self.driver.save_screenshot('SCEEN1.png')
                            # import pdb;pdb.set_trace()
                            product_url = url
                            penjual_url = MySQLdb.escape_string(response.xpath(
                                '//*[contains(@id,"mod-product-detail")]/aside/div/article/div[2]/h5/a/@href').extract_first())
                            penjual = MySQLdb.escape_string(response.xpath(
                                '///*[contains(@id,"mod-product-detail")]/aside/div/article/div[2]/h5/a/text()').extract_first())
                            # // *[ @ id = "mod-product-detail-1"] / aside / div / article / div[5] / div / text()
                            try:
                                lokasi = MySQLdb.escape_string(response.xpath(
                                    '//*[contains(@id,"mod-product-detail")]/aside/div/article/div[6]/div/text()').extract_first())
                            except:
                                lokasi = MySQLdb.escape_string(response.xpath(
                                    '// *[ contains(@ id , "mod-product-detail")] / aside / div / article / div[5] / div/text()').extract_first())
                            try:
                                product = MySQLdb.escape_string(response.xpath(
                                    '// *[ contains (@ id , "mod-product-detail-")] / div / div[1] / div / div[2] / h1/text()').extract_first())
                            except:
                                product = MySQLdb.escape_string(response.xpath(
                                    '// *[contains (@ id , "mod-product-detail-")] / div / div[1] / div[2] / div[2] / h1/text()').extract_first())
                            try:
                                harga = response.xpath(
                                    '//*[contains(@id,"mod-product-detail")]/div/div[1]/div[2]/div[2]/div[2]/div/span[2]/span[2]/text()').extract_first()
                                harga = harga.replace(".", "")
                            except:
                                try:
                                    harga = response.xpath(
                                        '//*[contains(@id,"mod-product-detail")]/div/div[1]/div/div[2]/div[2]/div/span/span[2]/text()').extract_first()
                                    harga = harga.replace(".", "")
                                except:
                                    try:
                                        harga = response.xpath(
                                            '// *[contains(@id,"mod-product-detail")] / div / div[1] / div / div[2] / div[3] / div / span / span[2]/text()').extract_first()
                                        harga = harga.replace(".", "")
                                    except:
                                        harga = response.xpath(
                                            '// *[contains(@id, "mod-product-detail")] / div / div[1] / div / div[2] / div[4] / div / span / span[2]/text()').extract_first()
                                        harga = harga.replace(".", "")
                            berat = response.xpath(
                                '//*[ contains(@ id , "product_spec")] / dl / dd[3]/text()').extract_first()
                            kondisi = response.xpath(
                                '//*[contains(@id,"product_spec_")]/dl/dd[2]/span/text()').extract()
                            kategori = response.xpath('//*[contains(@id,"product_spec_")]/dl/dd[1]/text()').extract()
                            dilihat = response.xpath('//dd[@title="Dilihat"]/strong/text()').extract_first()
                            try:
                                terjual = response.xpath('//dd[@title="Terjual"]/strong/text()').extract()
                            except:
                                terjual = 0
                            update_terakhir =response.xpath('//dd[@title="Update Terakhir"]/strong/text()').extract_first()
                            deskripsi = response.xpath('//*[@id="rmjs-1"]/p/text()').extract()
                            if "Pesan sebelum" in lokasi:
                                lokasi = response.xpath('//*[@id="mod-product-detail-1"]/aside/div/article/div[5]/div/text()').extract_first()
                            kondisi = ''.join(kondisi)
                            kategori = ''.join(kategori)
                            try:
                                terjual = ''.join(terjual)
                            except:
                                pass
                            product = ''.join(product)
                            try:
                                dilihat = ''.join(dilihat)
                            except:
                                pass
                            try:
                                dilihat = int(dilihat)
                            except:
                                dilihat = None
                            try:
                                terjual = int(terjual)
                            except:
                                terjual = 0
                            update_terakhir = ''.join(update_terakhir)
                            lokasi = lokasi.replace("\\n", "").replace("\n","")
                            berat = berat.replace("gram", "").replace(" kilo", "000").replace("  kg", "000").replace(".", "").strip()
                            product = product.replace("\\n", "").replace("\\\"", "").replace("\\", "")
                            kategori = kategori.replace("\n", "")
                            if "\n" in deskripsi:
                                deskripsi = None
                            update_terakhir = update_terakhir.replace("<strong>","").replace("</strong>","")
                            #ganti yang hari lalu jadi tanggal terupdate
                            if "hari lalu" in update_terakhir:
                                now = datetime.datetime.now()
                                hari = update_terakhir.split(" ")
                                hari = ''.join(hari[0])
                                hari = hari.encode('utf-8')
                                coy = now.strftime("%Y-%m-%d %H:%M").split("-")
                                tanggal = coy[1]
                                tanggal_fix = int(tanggal) - int(hari)
                                tanggal_fix = coy[0] +"-"+ str(abs(tanggal_fix)) +"-"+ coy[2]
                                update_terakhir = tanggal_fix
                            elif "Hari ini," in update_terakhir:
                                hari = update_terakhir.split(",")
                                hari = hari[1]
                                now = datetime.datetime.now()
                                coy = now.strftime("%Y-%m-%d")
                                update_terakhir = coy + hari
                            print "=================================================="
                            akhir = json.dumps(
                                {'type': 'bukalapak', 'product_url': product_url, 'penjual_url': penjual_url,'kategori': kategori,
                                 'product_name': product, 'harga': int(harga),'update_terakhir':update_terakhir, 'berat': int(berat),
                                 'kondisi': kondisi,'dilihat':dilihat,'terjual':terjual,'deskripsi':deskripsi,'penjual': penjual,
                                 'lokasi': lokasi})
                            try:
                                for kaf in range(0, 20):
                                    try:
                                        prod = KafkaProducer(bootstrap_servers=setting.broker)
                                        prod.send(setting.kafka_topic, b"{}".format(akhir))
                                        print "=================================================="
                                        print "SUKSES SEND TO KAFKA"
                                        print "=================================================="
                                        print akhir
                                        status = "done"
                                        sql = "UPDATE bukalapak_url SET status = '{}' WHERE product_url = '{}'".format(status, url)
                                        cur.execute(sql)
                                        self.conn.commit()
                                        kaf = 1
                                    except:
                                        pass
                                    if kaf == 1:
                                        break
                            except Exception, e:
                                print e
                        except Exception, e:
                            print e
                    except:
                        pass
                except Exception, e:
                    print e
        except Exception, e:
            print e
        cur.close()
        try:
            self.driver.close()
        except Exception, e:
            print e


if __name__ == '__main__':
    p = producer()
    p.parse()