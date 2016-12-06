import scrapy

class NewsSpider(scrapy.Spider):
  name = "news"
  start_urls = [
    "https://en.wikipedia.org/wiki/Portal:Current_events",
  ]

  def parse(self, response):
    overview_text = "//td[@style='vertical-align:top;']"
    dates = response.xpath(overview_text + "/table[@class='vevent']")
    date_count = len(dates)
    overview = response.xpath(overview_text + "/table[1]")
    for date in range(date_count):
      subjects = dates[date].xpath(".//tr[2]/td/dl")
      subject_count = len(subjects)
      for subject in range(subject_count):
        events = subjects[subject].xpath(".//ul")
        event_count = len(events)
        for event in range(event_count):
          specs = events[event].xpath(".//li")
          spec_count = len(specs)

