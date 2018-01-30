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
        self.queries = pd.read_csv('w2.csv')
        self.queries.fillna('',inplace=True)
        #yield scrapy.Request('%s/%s' % (site_url,'prop_card.aspx?pin=1202192050330000'))

        self.driver = webdriver.Chrome(self.chromedriver)

        # TODO: Remove this later since it should be unnecessary later
        self.headers_printed = False
        
        self.addresses = {}

        for index,row in self.queries.iterrows():
            self.driver.get(self.site_url)
            # Execute a search
            self.doSearch(row)
            # Process the results
            while True:
                pins = self.doResults()
                for pin in pins:
                    #print('OUTPUT %s' % self.pin2address(pin))
                    #print('TYPE %s' % type(self.pin2address(pin)))
                    p2a = self.pin2address(pin)
                    self.addresses[pin]=p2a[0]
                # Fire off the PIN requests
                #print(JavascriptExecutorpins)
                #print(self.pin_adr)
                for pin in pins:
                    yield scrapy.Request(
                        'http://www.willcountysoa.com/prop_card.aspx?pin=%s' % pin
                    )
                # More?
                next = None
                try:
                    next = self.driver.find_element_by_xpath('//*[@id="ctl00_BC_gvParcels_ctl34_lbNext"]')
                except:
                    pass
                if next:
                    next.click()
                else:
                    break
        #yield []
    
    '''
    The thing to do here seems to be to pass in to AJAX a callback.  I need to have that callback set a
    variable I can just call at the end of this call to execute_script.
    '''
    def pin2address(self,pin):
        ''' Use the web site's AJAX to get the address without creating a popup or async issues. '''
        
        return self.driver.execute_script ('''
            pin = "''' + pin + '''";
            p2a_data = undefined;
            $.ajax({
                type: "GET",
                async: false,
                contentType: "application/json; charset=utf-8;",
                url: "/WebServices/Utils.asmx/GetAddresses",
                data: { pin: "'" + pin + "'" },
                cache: false,
                dataType: "json", // back from server
                success: (function() {
                    return function(data){
                        var json = jQuery.parseJSON(data.d);
                        p2a_data = json;    
                    }
                })()
            });
            return p2a_data;
        ''')

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
        '''
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
        '''
        return(pins)

    fields_of_interest = [
        'PIN', 'PropClass', 'Address', 'City', 'Zip', 'SaleDate', 'SaleAmt',
        'TaxRate', 'ASL', 'ASFL', 'AI', 'ASB', 'ASFB', 'ASTotal', 'ASFTotal',
        'Subdivision', 'FullBath', 'Style', 'HalfBath', 'LivingSqFt', 'CentralAir',
        'BldgSqFt', 'Fireplace', 'YearBuilt', 'Porch', 'Basement', 'Attic',
        'Garage', 'Lot', 'Block', 'Unit', 'Building', 'Area', 'Status'
    ]
    # Fields available but being ignored:
    # LegalDesc

    #fields_of_interest = [
    #    'PIN', 'PropClass', 'SaleDate', 'SaleAmt', 'TaxRate'
    #]


    def parse(self, response):
        ''' Digest a page '''
        #print(response.body)
        x = scrapy.Selector(response)

        # TODO - pass this to an item and a proper pipeline
        data = []
        if not self.headers_printed:
            print ('\t'.join(self.fields_of_interest))
            self.headers_printed = True

        for field in self.fields_of_interest:
            # TODO - wrap this in a try or something to output N/A, not err
            location = x.xpath(
                '//*[@id="ctl00_BC_lb%s"]//text()' % field
            )
            texts = location.extract()
            data.append(texts[0] if len(texts) else 'N/A')

        # PIN
        pin = data[0].replace('-','')
        # Address Data
        data[2] = self.addresses[pin]['address']
        data[3] = self.addresses[pin]['city']
        data[4] = self.addresses[pin]['zip']


        # TODO - get rid of this ugliness of dumping right here
        # Create a proper pipeline for serialization
        print('\t'.join(data))
        pass

'''
    WillCo2 - changing the front-end up a bit...
'''
class WillCo2Spider(WillCoSpider):
    name = 'WillCo2'

    def start_requests(self):
        self.driver = webdriver.Chrome(self.chromedriver)

        # TODO: Remove this later since it should be unnecessary later
        self.headers_printed = False
        
        self.addresses = {}
        self.driver.get(self.site_url)
        self.doSearch(['1','','a'])
        
        townships = [
            '0701',        #Wheatland
            '1202',        #Dupage
            '0603',        #Plainfield
            '1104',        #Lockport
            '1605',        #Homer
            '0506',        #Troy
            '3007',        #Joliet
            '1508',        #New Lenox
            '1909',        #Frankfort
            '0410',        #Channahon
            '1011',        #Jackson
            '1412',        #Manhattan
            '1813',        #Green Garden
            '2114',        #Monee
            '2315',        #Crete
            '2316',        #Crete
            '0317',        #Wilmington
            '0918',        #Florence
            '1319',        #Wilton
            '1720',        #Peotone
            '2021',        #Will
            '2222',        #Washington
            '2223',        #Washington
            '0224',        #Reed
            '0124',        #Custer
            '0125',        #Custer
            '0824',        #Wesley
            '0825',        #Wesley
        ]
        sections = ["%02d" % (1+x) for x in range(36)]
        for township in townships[:1]:
            for section in sections[:1]:
                for block in range(100,1000):
                    if block > 101:
                        break
                    for lot in range(1,1000):
                        if lot > 2:
                            break
                        pin = "%s%s%d%02d0000" % (township,section,block,lot)
                        print(pin)
                        
        yield []
