from pathlib import Path
import scrapy

class LinkedInSpider(scrapy.Spider):
    name = 'LinkedIn'

    def start_requests(self):
        start_urls=['https://www.linkedin.com/jobs/collections/recommended/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f"linkedinjobs.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
