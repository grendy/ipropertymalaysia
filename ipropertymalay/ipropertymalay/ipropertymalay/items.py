# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IpropertymalayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class tcategory(scrapy.Item):
	nama_kategori = scrapy.Field()
	name = scrapy.Field()

class outjson(scrapy.Item):
	harga = scrapy.Field()
	nama = scrapy.Field()
	phone = scrapy.Field()
	title = scrapy.Field()
	desc = scrapy.Field()
	photo = scrapy.Field()

