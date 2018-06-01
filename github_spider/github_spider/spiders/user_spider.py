# coding=utf-8

from scrapy import Spider, Request
import json

prices = {}
prices_divide = {}
prices_list = []
count = 0
step = 10000


class UserSpider(Spider):
    name = "user"

    start_urls = [
        'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=%E5%89%8D%E7%AB%AF&sg=589dd5bfdcd44c3eb1d08d6be750cf41&p=1'
    ]

    def parse(self, response):
        global prices
        global count
        nextPageUrl = response.css('li.pagesDown-pos a::attr(href)').extract_first()

        for p in response.css('td.zwyx::text').extract():
            count += 1
            price = str.split(p, '-')[0]
            price = str.replace(price, '01', '00')
            price = str.replace(price, '02', '00')
            price = str.replace(price, '元以上', '')
            price = str.replace(price, '元以下', '')
            price = str.replace(price, '面议', '%s' % -step)

            if prices.get(price) is None:
                prices[price] = 1
            else:
                prices[price] += 1

            base = ''
            if int(int(price)/step) * step < 0:
                base = '面议'
            else:
                base = '%s - %s' % (int(int(price)/step) * step, (int(int(price)/step)+1) * step)

            if prices_divide.get(base) is None:
                prices_divide[base] = 1
            else:
                prices_divide[base] += 1

        if nextPageUrl is not None:
            yield Request(nextPageUrl, self.parse)
        else:
            file_write_base(prices)

            file_write_sort(prices)

            file_write_divide(prices_divide)

        # resp = json.loads(response.body.decode('utf-8'))
        # filename = '%s.json' % int(random.random() * 1000000000)
        # with open(filename, 'w') as f:
        #     f.write(json.dumps(resp))
        #
        # try:
        #     with open('log.txt', 'w') as f:
        #         f.write('request: %s' % resp['followers_url'])
        #     yield Request(resp['followers_url'], self.parse)
        # except TypeError:
        #     logging.error('crawl end!')
        #     for user in resp:
        #         logging.info('user:%s' % user)
        #         with open('log.txt', 'w') as f:
        #             f.write('request: %s' % user['url'])
        #         yield Request(user['url'], self.parse)


def format_list(prices_dict):
    arr = []
    for ps in prices_dict:
        arr.append({
            'price_min': ps,
            'num': prices_dict[ps]
        })

    return arr


def file_write_sort(p):
    sort_list = sorted(format_list(p), key=lambda x: x['num'], reverse=True)
    content = json.dumps(sort_list, ensure_ascii=False)
    filename = 'prices-sort.json'
    with open(filename, 'w') as f:
        f.write(content)


def file_write_base(p):
    content = json.dumps(p, ensure_ascii=False)
    filename = 'prices.json'
    with open(filename, 'w') as f:
        f.write(content)


def file_write_divide(p):
    sort_list = sorted(format_list(p), key=lambda x: x['num'], reverse=True)
    content = json.dumps(sort_list, ensure_ascii=False)
    filename = 'prices-divide-sort.json'
    with open(filename, 'w') as f:
        f.write(content)
