# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LutherbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WillCoItem(scrapy.Item):
    PIN = scrapy.Field()
    PropClass = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    Zip = scrapy.Field()
    SaleDate = scrapy.Field()
    SaleAmt = scrapy.Field()
    TaxRate = scrapy.Field()
    ASL = scrapy.Field()
    ASFL = scrapy.Field()
    AI = scrapy.Field()
    ASB = scrapy.Field()
    ASFB = scrapy.Field()
    ASTotal = scrapy.Field()
    ASFTotal = scrapy.Field()
    Subdivision = scrapy.Field()
    FullBath = scrapy.Field()
    Style = scrapy.Field()
    HalfBath = scrapy.Field()
    LivingSqFt = scrapy.Field()
    CentralAir = scrapy.Field()
    BldgSqFt = scrapy.Field()
    Fireplace = scrapy.Field()
    YearBuilt = scrapy.Field()
    Porch = scrapy.Field()
    Basement = scrapy.Field()
    Attic = scrapy.Field()
    Garage = scrapy.Field()
    Lot = scrapy.Field()
    Block = scrapy.Field()
    Unit = scrapy.Field()
    Building = scrapy.Field()
    Area = scrapy.Field()
    Status = scrapy.Field()
