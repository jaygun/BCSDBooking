# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime, timedelta
import urllib
import urlparse

class BookingSpider(CrawlSpider):

    # Set date/time variables
    # ---
    now = datetime.today()
    dateto = urllib.quote_plus(now.strftime("%m/%d/%Y"))

    # We can get a range of days - example to get yesterday
    # ---
    #past = now - timedelta(1)
    #datefrom = urllib.quote_plus(past.strftime('%m/%d/%Y'))

    # 24 Hour times in url allowed - example to get past hour
    # ---
    #past = now - timedelta(hours = 1)
    #datefrom = urllib.quote_plus(past.strftime('%m/%d/%Y %H:%M'))

    name = "GetInmates"
    allowed_domains = ["inmate.co.buchanan.mo.us"]
    start_urls = ["http://inmate.co.buchanan.mo.us/NewWorld.InmateInquiry/buchananco?BookingFromDate=" + dateto + "&BookingToDate=" + dateto]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="Next"]',)), callback="parse_page", follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_page(response)

    def parse_page(self, response):
        for inmate in response.xpath('//*[@id="Inmate_Index"]//*/tr/td/a/@href'):
            inmate_url = response.urljoin(inmate.extract())
            yield Request(inmate_url, callback=self.parse_inmate)

    def parse_inmate(self, response):
        yield {
            'name': response.css('.FieldList .Name span::text').extract_first(),
            'bookingdate': response.css('.Booking .BookingData .FieldList .BookingDate span::text').extract_first(),
            'totalbondamount': response.css('.BookingData .FieldList .TotalBondAmount span::text').extract_first(),
            'chargedescrption': response.css('.BookingData .BookingCharges .Grid tbody .ChargeDescription::text').extract(),
            'offensedate': response.css('.BookingCharges .Grid tbody .OffenseDate::text').extract(),
            'photo': urlparse.urljoin(response.url, response.css('.BookingPhotos a::attr(href)').extract_first()),
            'sourceurl': response.url,
        }