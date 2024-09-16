import scrapy

class AiforeducationSpider(scrapy.Spider):
    name = "aiforeducation"
    start_urls = [
        'https://www.aiforeducation.io/prompt-library-all-prompts',
    ]

    def parse(self, response):
        for prompt in response.xpath('//main[@id="page"]/ARTICLE[1]/SECTION[8]/DIV[2]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV'):
            link = prompt.xpath('descendant-or-self::a[contains(@class, "summary-thumbnail-container sqs-gallery-image-container")]/@href').get()
            if link:
                yield response.follow(link, self.parse_detail, meta={
                    'title': prompt.xpath('descendant-or-self::p/text()').get(),
                    'image': prompt.xpath('descendant-or-self::IMG[contains(@class,"summary-thumbnail-image loaded")]/@src').get()
                })

    def parse_detail(self, response):
        yield {
            'title': response.meta['title'],
            'image': response.meta['image'],
            'detail_title': response.xpath('//h1[contains(@class, "entry-title entry-title--large p-name")]/text()').get(),
            'content': response.xpath('//div[contains(@class, "sqs-block-content")]//text()').getall(),
        }

# To run the spider, save this code in a file (e.g., aiforeducation_spider.py) and run it using the Scrapy command line tool:
# scrapy runspider aiforeducation_spider.py -o output.json
