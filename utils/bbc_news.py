import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.theguardian.com/world']

    def parse(self, response):
        for href in response.css("h2.fc-item__title a::attr(href)").extract():
            yield {'link': href}
