import scrapy
from kindle_scraper.items import BookItem
from datetime import date

class KindleSpider(scrapy.Spider):
    name = "kindle_spider"

    start_urls = {
        ('https://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital'
            '-text/154606011/')
    }

    def parse(self, response):
        for book in response.xpath('//div[@class = "a-section a-spacing-none aok-relative"]'):
            next_book_url = book.xpath('./span/a/@href').get()

            if next_book_url is not None:
                yield scrapy.Request(response.urljoin(next_book_url),
                    callback = self.parse_book)

        next_page_url = response.xpath('//ul[@class = "a-pagination"]'
            '//li[@class = "a-last"]/a/@href').get()

        if next_page_url is not None:
            yield scrapy.Request(repsonse.urljoin(next_page_url))


    def parse_book(self, response):
        book_info = BookItem()
        categories = []

        book_info['date'] = date.today()
        book_info['title'] = response.xpath('//span[@id = "ebooksProductTitle"]/text()').get()

        for category in response.xpath('//li[@id = "SalesRank"]//li[@class = "zg_hrsr_item"]'):
            text = category.xpath('.//span[@class = "zg_hrsr_ladder"]/a/text()').get()
            categories.append(text)

        book_info['categories'] = categories

        yield book_info
