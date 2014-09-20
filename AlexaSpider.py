# -*- coding: utf-8 -*-
#
#To run this spider, from command line type 'scrapy crawl AlexaSpider -o <output_file_name>.json'
#

#This spider uses the scrapy framework to crawl sites
import scrapy
from alexa1m.items import Alexa1MItem

#Below methods used to put Alexa 1M in format that can be used by scrapy
from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from csv import DictReader
from chardet import detect


class AlexaSpider(scrapy.Spider):
    name = "AlexaSpider"
 
    #scrapy requires a start URL, so why not a top 10 university
    start_urls = ( 'http://gatech.edu',)

    #
    # This parse function gets the current Alexa Top 1M from Amazon, asks how many you want to crawl, and store info in a dictionary
    # The dictionary keys are 'rank', 'url', 'content' where content is string of raw source code
    #
    def parse(self, response):   
        #Asks for number of sites to get. Any random input returns 10 sites
        try:
            numsites = int(input("Enter number of sites you would like to get (Default is 10): "))
        except:
            numsites = 10

        #Set a counter to 0 (used to control how sites we get during development) 
        count=0

        #Get the current list of Alexa 1M and store as a string in memory
        alexaurl = urlopen("http://s3.amazonaws.com/alexa-static/top-1m.csv.zip")
        alexa_zip = ZipFile(StringIO(alexaurl.read()))

        #put the Alexa 1M in a dictionary with keys 'rank' and 'url'
        fieldnames=('rank','url')
        reader = DictReader(alexa_zip.open("top-1m.csv"), fieldnames)

        #Iterate over the Alexa 1M and store them as a list of dictionaries
        for row in reader:
            site = Alexa1MItem()
            site['rank'] = row['rank']
            site['url'] = "http://"+row['url']
            
            # execute method to parse the current URL
            yield scrapy.Request(site['url'], self.parse_Alexa1M, meta={'item': site})
           
            #Exit the loop based on how many sites we want to get during development
            count = count + 1
            if (count==numsites):
                break

    # This method stores the content of the input URL as a string
    def parse_Alexa1M(self, response):
        site = response.meta['item']
        site['encoding'] = detect(response.body)['encoding']

        # this if..else used to store website content as a unicode string (added this due to some issues with chinese sites)
        if (site['encoding'] == 'GB2312'):
            # some sites come back as deprecated GB2312, so use current charset
            site['encoding'] = 'GB18030'
            site['content'] = response.body.decode(site['encoding'])             
        else:
            site['content'] = response.body.decode(site['encoding'])

        yield site
        