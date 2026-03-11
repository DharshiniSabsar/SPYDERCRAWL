import scrapy

class MarketItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    vendor = scrapy.Field()
    url = scrapy.Field()
