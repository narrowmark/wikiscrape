import scrapy
import logging
import re

class NewsSpider(scrapy.Spider):
  name = "news"
  start_urls = [
    "https://en.wikipedia.org/wiki/Portal:Current_events",
  ]

  logging.basicConfig(filename='news_spider.log', level=logging.INFO)

  def date_parse(self, date):
    date_list = date.xpath(".//text()").extract()

    date_list = re.findall(r'(?u)\w+', date_list[1])
    date_list = [x.encode('utf-8') for x in date_list]
    month, day, year = date_list[0], date_list[1], date_list[2]

    #return str(month) + " " + str(day) + ", " + str(year)
    return month + " " + day + ", " + year

  def event_parse(self, event):
    exclude_external = ".//a[not(contains(@class, 'external text'))]"
    plain = ""
    for line in event.xpath(exclude_external + "/text()|text()"):
      plain += line.extract()
    return plain

  def parse(self, response):
    summaries = response.xpath("//table[@class='vevent']")

    portal = {}
    for summary in summaries:
      # Getting the constellation of date elements; compartmentalizes changes
      # to date_parse()
      date = summary.xpath(".//span[@class='summary']")[0]
      # logging.info("DATE: " + self.date_parse(date))

      descriptions = summary.xpath("descendant::td[@class='description']")
      for desc in descriptions.xpath("descendant::dl"):
        subject = desc.xpath(".//dt/text()").extract_first()

        headlines = []
        for headline in desc.xpath("following-sibling::ul"):
          event = headline.xpath(".//li")[0]
          headlines.append(self.event_parse(event))

        portal[subject] = headlines
    yield portal
