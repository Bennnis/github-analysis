import scrapy
import logging
import json

user_url = 'https://api.github.com/users/Bennnis'

headers = {
    'Accept': 'application / vnd.github.v3 + json'
}


class UserSpider(scrapy.Spider):
    name = "user"

    def start_requests(self):
        urls = [
            user_url
        ]

        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        resp = json.loads(response.body.decode('utf-8'))
        logging.info(resp)