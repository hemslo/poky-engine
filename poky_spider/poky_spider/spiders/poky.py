from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from poky_spider.items import PokySpiderItem
from scrapy.http import Request
import redis


class PokySpider(BaseSpider):
    name = "PokySpider"
    allowed_domains = []
    start_urls = ['http://www.seu.edu.cn']
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    link_extractor = SgmlLinkExtractor()

    def parse(self, response):
        # parse items
        hxs = HtmlXPathSelector(response)
        item = PokySpiderItem()
        item['url'] = response.url
        item['body'] = response.body
        item['text'] = {}
        tags = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'area', 'p',
                'b', 'strong', 'i', 'em', 'li', 'th', 'td', 'span', 'button']
        for tag in tags:
            item['text'][tag] = hxs.select('//%s/text()' % tag).extract()

        item['text']['description'] = hxs.select('//meta[translate(@name, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="description"]/@content').extract()
        item['text']['keywords'] = hxs.select('//meta[translate(@name, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="keywords"]/@content').extract()

        # extract links
        links = self.link_extractor.extract_links(response)
        item['links'] = [link.url for link in links]

        # filter links
        r = redis.Redis(connection_pool=self.pool)
        filtered_links = []
        for link in links:
            if not r.sismember('urls', link.url):
                r.sadd('urls', link.url)
                filtered_links.append(link.url)

        # yield items
        yield item

        # yield links
        for link in filtered_links:
            yield Request(url=link, callback=self.parse)
