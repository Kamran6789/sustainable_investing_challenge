from datetime import datetime
import scrapy
from scrapy.crawler import CrawlerProcess


class InvestingWinnersSpider(scrapy.Spider):
    name = "investing_winners"
    start_urls = ["https://www.sustainableinvestingchallenge.org/past-winners"]

    def parse(self, response):
        items = {}
        items["competition"] = 'Kellogg-Morgan Stanley Sustainable Investing Challenge'
        items['lastupdate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        year_elements = response.css('.color_16 .wixui-rich-text__text::text').extract()
        items['year'] = year_elements[0].replace('Winner', '') if year_elements else None

        items['winner_business'] = response.css('.font_7 .wixui-rich-text__text .wixui-rich-text__text::text')[0].extract() + ':' + response.css('div.wixui-rich-text h6 span::text')[1].extract()
        items['2nd place business'] =response.css('.font_7 .wixui-rich-text__text .wixui-rich-text__text::text')[1].extract() + ':' + response.css('div.wixui-rich-text h6 span::text')[3].extract()
        items['3rd place business'] = response.css('.font_7 .wixui-rich-text__text .wixui-rich-text__text::text')[2].extract() + ':' + response.css('div.wixui-rich-text h6 span::text')[5].extract()
        items['4th place business'] = response.css('.font_7 .wixui-rich-text__text .wixui-rich-text__text::text')[3].extract() + ':' + response.css('div.wixui-rich-text h6 span::text')[7].extract()

        # Extracting links to all remaining pages
        remaining_pages_links = response.css('span.wixui-rich-text__text span a::attr(href)').extract()
        # Some links may not be related to remaining pages, so let's exclude them
        remaining_pages_links = [link for link in remaining_pages_links if 'past-winners' in link]

        yield items

        # Follow links to remaining pages
        for link in remaining_pages_links:
            yield response.follow(link, callback=self.parse_remaining_pages)
    #
    def parse_remaining_pages(self, response):
        items = {}
        items["competition"] = 'Kellogg-Morgan Stanley Sustainable Investing Challenge'
        items['lastupdate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        year_elements = response.css('.color_16 .wixui-rich-text__text::text').extract()
        items['year'] = year_elements[0].replace('Winner', '') if year_elements else None

        items['winner_business'] = response.css('.font_7 .wixui-rich-text__text .wixui-rich-text__text::text')[0].extract() + ':' + response.css('div.wixui-rich-text h6 span::text')[1].extract()
        items['2nd place business'] = response.css('.font_7 .wixui-rich-text__text .wixui-rich-text__text::text')[1].extract() + ':' + response.css('div.wixui-rich-text h6 span::text')[3].extract()
        items['3rd place business'] = response.css('.font_7 .wixui-rich-text__text .wixui-rich-text__text::text')[2].extract() + ':' + response.css('div.wixui-rich-text h6 span::text')[5].extract()
        items['4th place business'] = response.css('.font_7 .wixui-rich-text__text .wixui-rich-text__text::text')[3].extract() + ':' + response.css('div.wixui-rich-text h6 span::text')[7].extract()

        yield items


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(InvestingWinnersSpider)
    process.start()
