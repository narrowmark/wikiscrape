import scrapy
import re
import logging

class ExcelOutputSpider(scrapy.Spider):
  name = "excel"
  start_urls = [
    "https://en.wikipedia.org/wiki/Portal:Current_events",
  ]

  logging.basicConfig(filename="excel.log", level=logging.INFO)

  def date_parse(self, date):
    date_list = date.xpath(".//text()").extract()

    date_list = re.findall(r'(?u)\w+', date_list[1])
    date_list = [x.encode('utf-8') for x in date_list]
    month, day, year = date_list[0], date_list[1], date_list[2]

    return month + " " + day + ", " + year

  def headline_parse(self, event):
    # Dump external links
    exclude_external = ".//a[not(contains(@class, 'external text'))]"

    # Only return ongoing events
    if re.findall(r'a.*</a>\n', event.extract()) == []:
      return ""

    plain = ""
    # for line in event.xpath(exclude_external + "/text()|text()"):
    #  plain += line.extract()[0]
    plain += event.xpath(exclude_external + "/text()|text()")[0].extract()
    logging.info("PLAIN:" + plain)
    return plain

  def parse(self, response):
    summaries = response.xpath("//table[@class='vevent']")
    current = {}

    for summary in summaries:
      date = summary.xpath(".//span[@class='summary']")[0]

      descriptions = summary.xpath("descendant::td[@class='description']")
      for desc in descriptions:
        for headline in desc.xpath("child::ul/li"):
          parsed = self.headline_parse(headline)
          if parsed != "":
            logging.info("PARSED: " + parsed)
          if headline.xpath(".//a/text()").extract_first() is None:
            logging.info("EVENT?! NOTHING TO REPORT!")
            continue

          #logging.info("EVENT!!:" + headline.xpath(".//a/text()").extract_first())
