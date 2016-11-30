import scrapy

class NewsSpider(scrapy.Spider):
  name = "news"
  start_urls = [
    "https://en.wikipedia.org/wiki/Portal:Current_events",
  ]

  def parse(self, response):
    for description in response.xpath("//td[@class='description']/dl/dt/text()").extract():
      yield {
        'headline': description
      }
