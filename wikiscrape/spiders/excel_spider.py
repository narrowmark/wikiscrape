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
    # Query for removing external links
    not_external = ".//a[not(contains(@class, 'external text'))]"

    # Only return ongoing events
    if re.findall(r'<li><a.*</a>\n', event.extract()) == []:
      return []

    head = event.xpath(not_external + "/text()|text()")[0].extract()
    event = event.xpath(".//li/text()|" + not_external +
                        "/text()").extract()
    body = ""
    for line in event[1:]:
      body += line

    return [head, body]

  def parse(self, response):
    summaries = response.xpath("//table[@class='vevent']")
    # dict of the form { headline: [most_recent, first, count] }
    current = {}

    for summary in summaries:
      date = summary.xpath(".//span[@class='summary']")[0]

      descriptions = summary.xpath("descendant::td[@class='description']")
      for desc in descriptions:
        for headline in desc.xpath("child::ul/li"):
          parsed = self.headline_parse(headline)
          if parsed == []:
            continue

          #logging.info("HEAD: " + parsed[0])
          #logging.info("BODY: " + parsed[1] + "\n")

          if current.has_key(parsed[0]) == false:
            current[parsed[0]] = [date, date, 1]
          else:
            current[parsed[0]][1] = date
            current[parsed[0]][2] += 1
