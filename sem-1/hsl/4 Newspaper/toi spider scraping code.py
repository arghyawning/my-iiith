import scrapy
import csv

class ToiSpider(scrapy.Spider):
    name  = 'toispi'
    allowed_domains = ['timesofindia.indiatimes.com']
    #domains that are allowed to scrape
    with open("urls.txt","r") as f:
        start_urls = [url.strip() for url in f.read().split("\n")]
    #start_urls = ['https://timesofindia.indiatimes.com/topic/Winter-Olympics']
    #urls it will visit
    #name, allowed_domains, start_urls 
    print(start_urls)

    #parse function: gets html of the page or css
    #we are using css
    def parse(self, response):
        url = response.url
        title = response.css("h1 span::text").get()
        #urls = response.css("div.row a::attr(href)").getall()

        date = response.css("div.byline span::text").get()
        text = response.css("div._3YYSt::text").getall()
        text = [x.strip() for x in text]
        text = " ".join(text)

        DELIM = "~"

        csv_row = [url,title,date,text]

        def clean_row(row):
            return [item.strip().replace(DELIM," ")if item else " " for item in row]

        with open("toiscraperesults.csv","a",newline="") as f:
            writer = csv.writer(f,delimiter = DELIM)
            writer.writerow(clean_row(csv_row)) 


        #print("\n\n")
        #print(url,title,date,text)