import scrapy
import time
from newscollecter.items import NewsItem
from scrapy_splash import SplashRequest


class NewSpider(scrapy.Spider):
    name = "news"
    start_urls = ['https://finance.sina.com.cn/']

    def parse(self, response):
        """解析首页"""
        splash_args = {
            'wait': 0.5,
        }
        for i in response.xpath("//*[@class='fin_tabs0_c0']/div[1]/*/a"):  # 要闻
            item = NewsItem()
            item["title"] = "".join(i.xpath("text()").extract())
            item["link"] = "".join(i.xpath("@href").extract())
            item["page_url"] = response.url
            item["crawl_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["page_type"] = "要闻首页"

            if "imeeting" in i.xpath("@href").extract()[0]:
                yield SplashRequest(i.xpath("@href").extract()[0], self.parse_result, endpoint='render.html', args=splash_args)
            else:
                yield scrapy.Request(response.urljoin(i.xpath("@href").extract()[0]), callback=self.parse_result)

        for i in response.xpath("//*[@class='fin_tabs0_c0']/div[2]/*/li/a"):  # 要闻分页
            item = NewsItem()
            item["crawl_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["title"] = "".join(i.xpath("text()").extract())
            item["link"] = "".join(i.xpath("@href").extract())
            item["page_url"] = response.url
            item["page_type"] = "要闻分页"

            if "imeeting" in i.xpath("@href").extract()[0]:
                yield SplashRequest(i.xpath("@href").extract()[0], self.parse_result, endpoint='render.html', args=splash_args)
            else:
                yield scrapy.Request(response.urljoin(i.xpath("@href").extract()[0]), callback=self.parse_result)

    def parse_result(self, response):
        """文章页面解析"""
        item = NewsItem()
        item['page_url'] = response.url

        if "zt_d" in response.url:
            item['title'] = "".join(response.xpath("//*[@class='ellipsis']/text()").extract())
            item['content'] = "".join(response.xpath("//*[@class='CM-summary-text']/text()").extract())

            item["page_type"] = "专题"

        elif "stock" in response.url:
            item['title'] = "".join(response.xpath("//*[@class='main-title']/text()").extract())
            item['content'] = "".join(response.xpath("//*[@class='article']/p/text()").extract())

            item['source'] = "".join(response.xpath("//*[@class='source ent-source']/text()").extract())
            item["page_type"] = "股票"

        elif "imeeting" in response.url:
            item['title'] = "#".join(response.xpath("//*[@class='item-title ellipsis-lines']/text()").extract())

            item["page_type"] = "直播预告"

        elif "jinrong" in response.url:
            item['title'] = "".join(response.xpath("//*[@class='m-atc-title']/text()").extract())
            item['content'] = "".join(response.xpath("//*[@class='m-atc-body']/div/p/text()").extract())
            item['keyword'] = "#".join(response.xpath("//*[@class='m-atc-keyword']/a/text()").extract())

            item['source'] = "".join(response.xpath("//*[@class='a-text']/h2/text()").extract())
            item["page_type"] = "新浪金融研究院"

        else:
            item['title'] = "".join(response.xpath("//*[@class='main-title']/text()").extract())
            item['content'] = "".join(response.xpath("//*[@cms-style='font-L']/text()").extract())

            item['source'] = "".join(response.xpath("//*[@class='source ent-source']/text()").extract())
            item["page_type"] = "新闻详情"

            # item['publish_time'] = "".join(response.xpath("//*[@class='date-source']/span/text()").extract())

        item["crawl_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        yield item
