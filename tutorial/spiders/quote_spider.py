import scrapy
import time
from tutorial.items import TutorialItem


class NewSpider(scrapy.Spider):
    name = "news"
    start_urls = ['https://finance.sina.com.cn/']

    def parse(self, response):
        """解析首页"""
        for i in response.xpath("//*[@class='fin_tabs0_c0']/div[1]/*/a"):  # 要闻
            item = TutorialItem()
            item["title"] = "".join(i.xpath("text()").extract())
            item["link"] = "".join(i.xpath("@href").extract())
            item["page_url"] = response.url
            item["crawl_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["page_type"] = "要闻首页"
            yield scrapy.Request(response.urljoin(i.xpath("@href").extract()[0]), callback=self.page_parse)

        for i in response.xpath("//*[@class='fin_tabs0_c0']/div[2]/*/li/a"):  # 要闻分页
            item = TutorialItem()
            item["crawl_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["title"] = "".join(i.xpath("text()").extract())
            item["link"] = "".join(i.xpath("@href").extract())
            item["page_url"] = response.url
            item["page_type"] = "要闻分页"
            yield scrapy.Request(response.urljoin(i.xpath("@href").extract()[0]), callback=self.page_parse)

    def page_parse(self, response):
        """文章页面解析"""
        item = TutorialItem()
        item['page_url'] = response.url

        if "zt_d" in response.url:
            item['title'] = "".join(response.xpath("//*[@class='ellipsis']/text()").extract())
            item['content'] = "".join(response.xpath("//*[@class='title']/../p/text()").extract())

            item["page_type"] = "新闻专题页"

        else:
            item['title'] = "".join(response.xpath("//*[@class='main-title']/text()").extract())
            item['content'] = "".join(response.xpath("//*[@cms-style='font-L']/text()").extract())

            item['source'] = "".join(response.xpath("//*[@class='source ent-source']/text()").extract())
            item["page_type"] = "新闻详情页"

            # item['publish_time'] = "".join(response.xpath("//*[@class='date-source']/span/text()").extract())

        item["crawl_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        yield item
