# -*- coding: utf-8 -*-
import scrapy
import re

class IcrawlerSpider(scrapy.Spider):
    name = 'icrawler'
    start_url = 'https://imgur.com/new/time'
    regex = "[A-Z0-9?!]{5}-[A-Z0-9?!]{5}-[A-Z0-9?!]{5}"

    def start_requests(self):
        url = self.start_url
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        if "new/time" in response.url:
            urls = response.css('a.image-list-link ::attr(href)').extract()
            for url in urls:
                yield scrapy.Request(url='https://imgur.com' + url, callback=self.parse)
            yield scrapy.Request(url=self.start_url, callback=self.parse, dont_filter=True)
        else:
            description = "\n".join(list(filter(None, map(str.strip, response.xpath('//div[contains(@class, "post-image-meta")]//text()').extract()))))
            images = ", ".join(response.xpath('//div[contains(@class, "image")]//@src').extract())

            #Find all Steam keys from the post description
            keys = re.findall(self.regex, description)
            for key in keys:
                yield {"SteamKey": key}

            #Post data
            yield {'url': response.url,
                   'title': response.css('h1.post-title ::text').extract_first(),
                   'description': description,
                   'image_urls': images,
                   'op': response.css('a.post-account ::attr(href)').extract_first()}
