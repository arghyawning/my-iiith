import scrapy
import unidecode
import csv

class TempSpider(scrapy.Spider):
    name = "scraping"
    allowed_domains = ["myneta.info"]
    # with open("urls.txt", "r") as f:
    #     start_urls = f.read().splitlines()
    start_urls = [
        "https://myneta.info/westbengal2011/index.php?action=summary&subAction=winner_women&sort=candidate#summary"
    ]

    def parse(self, response):
        DELIM = ","

        def clean_row(row):
            return [item.strip().replace(DELIM, "") if item else "" for item in row]

        rows = response.css("tr")
        with open(f"wb2011F.csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=DELIM)
            for row in rows:
                data = [
                    unidecode.unidecode(word) for word in row.css("td *::text").getall()
                    #word for word in row.css("td *::text").getall()
                ]
                if len(data) == 11:
                    writer.writerow(clean_row(data[:-1]))