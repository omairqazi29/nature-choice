#Jfrom pathlib import Path
#Jimport scrapy
#J
#J
#Jclass ESG(scrapy.Spider):
#J    name = 'myspider'
#J
#J    def start_requests(self):
#J        with open('links.txt', 'rt') as file:
#J            urls = [url.strip() for url in file.readlines()]
#J        
#J        # Remove whitespace and newline characters from each URL
#J        with open('links.txt_', 'a') as file:
#J            file.write(urls)
#J
#J        for url in urls:
#J            yield scrapy.Request(url=url, callback=self.parse)
#J
#J    def parse(self, response):
#J        filename = response.url.split("/")[-2]
#J        open(filename, 'wb').write(response.body)
#J    
#J
#J    #def parse(self, response):
#J    #    # Define the XPath selector for the value you want to extract
#J    #    i = response.xpath('/html/body/div/div[1]/main/main/div[3]/div[2]/div[1]/div/div[1]/div[2]/div/div/text()').getall()
#J
#J    #    with open("extracted_values.txt", "a") as f:
#J    #        f.write(f"URL: {response.url}\n")
#J    #        f.write(f"Extracted Value: {i}\n\n")
#J
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        with open('links.txt', 'rt') as file:
            urls = [url.strip() for url in file.readlines()]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #i = response.xpath('/html/body/div/div[2]/div[1]/div[1]/span[2]/small/text()').getall()
        i = response.xpath('/html/body/div/div[1]/main/main/div[4]/div[2]/div[1]/div/div[1]/div[2]/div/div/text()').getall()
        print(i)
        #page = response.url.split("/")[-2]
