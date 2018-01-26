# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.support import ui
import os
import time
import pandas as pd

class WillCoSpider(scrapy.Spider):
    name = 'WillCo'
    allowed_domains = ['www.willcountysoa.com']
    #start_urls = ['http://willco.com/']
    site_url = 'http://www.willcountysoa.com/search_address.aspx'
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver

    def start_requests(self):
        self.queries = pd.read_csv('will.csv')
        self.queries.fillna('',inplace=True)
        #yield scrapy.Request('%s/%s' % (site_url,'prop_card.aspx?pin=1202192050330000'))

        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.get(self.site_url)

        for index,row in self.queries.iterrows():
            # Execute a search
            self.doSearch(row)
            # Process the results
            pins = self.doResults()
            # Fire off the PIN requests
            #print(pins)
            #print(self.pin_adr)
            for pin in pins:
                yield scrapy.Request(
                    'http://www.willcountysoa.com/prop_card.aspx?pin=%s' % pin
                )

                pass

        return []

    def doSearch(self,row):
        ''' Prep and Execute a single search '''
        if (row['from']):
            location = self.driver.find_element_by_xpath('//*[@id="ctl00_BC_txStreetFrom"]')
            location.click()
            location.send_keys(row['from'])
        if (row['to']):
            location = self.driver.find_element_by_xpath('//*[@id="ctl00_BC_txStreetTo"]')
            location.click()
            location.send_keys(row['to'])
        if (row['street']):
            location = self.driver.find_element_by_xpath('//*[@id="ctl00_BC_txStreetName"]')
            location.click()
            location.send_keys(row['street'])
        location = self.driver.find_element_by_xpath('//*[@id="ctl00_BC_btnSearch"]')
        location.click()

    def doResults(self):
        ''' Process results '''
        # First get the PINs so we can query these directly
        pins = [td.text for td in
            self.driver.find_elements_by_xpath('//*[@id="ctl00_BC_gvParcels"]/tbody/tr/td[1]/a')
        ]
        # TODO: get the addresses
        pds = []
        for a  in self.driver.find_elements_by_xpath('//*[@id="ctl00_BC_gvParcels"]/tbody/tr/td[2]/a'):
            a.click()
            time.sleep(0.25)
            pds.append(pd.read_html(
                self.driver.find_elements_by_xpath('//*[@id="address-list"]')[0].get_attribute("outerHTML")
            )[0].head(1))
            location = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/button/span[1]')
            location.click()

        self.pin_adr = pd.concat(pds)

        return(pins)




    def parse(self, response):
        ''' Digest a page '''
        #print(response.body)
        x = scrapy.Selector(response)

        # TODO - pass this to an item and a proper pipeline
        data = []

        # PIN
        data.append(
            x.xpath('//*[@id="ctl00_BC_lbPIN"]//text()').extract()[0]
        )

        # Sales Date
        data.append(
            x.xpath('//*[@id="ctl00_BC_lbSaleDate"]//text()').extract()[0]
        )

        # Sales Amount
        data.append(
            x.xpath('//*[@id="ctl00_BC_lbSaleAmt"]//text()').extract()[0]
        )

        # Tax rate
        data.append(
            x.xpath('//*[@id="ctl00_BC_lbTaxRate"]//text()').extract()[0]
        )

        # TODO - get rid of this ugliness of dumping right here
        print(','.join(data))
        pass
