import scrapy
import logging

class NewsSpider(scrapy.Spider):
  name = "news"
  start_urls = [
    "https://en.wikipedia.org/wiki/Portal:Current_events",
  ]

  logging.basicConfig(filename='news_spider.log', level=logging.INFO)

  def parse(self, response):
    summaries = response.xpath("//table[@class='vevent']")

    portal = {}
    for summary in summaries:
      # TODO: parse date
      date = summary.xpath(".//span[@class='summary']").extract()

      descriptions = summary.xpath("descendant::td[@class='description']")
      for desc in descriptions.xpath("descendant::dl"):
        subject = desc.xpath(".//dt").extract_first()

        headlines = []
        for headline in desc.xpath("following-sibling::ul"):
          situ = headline.xpath(".//li").extract_first()
          headlines.append(situ)

        portal[subject] = headlines
    yield portal
