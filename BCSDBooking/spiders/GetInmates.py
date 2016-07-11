# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime, timedelta
from BCSDBooking.items import BcsdbookingItem
import urllib
import urlparse

class InmateSpider(CrawlSpider):

    # Set date/time variables
    # ---
    now = datetime.today()
    today = urllib.quote_plus(now.strftime("%m/%d/%Y"))

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
    start_urls = ["http://inmate.co.buchanan.mo.us/NewWorld.InmateInquiry/buchananco?BookingFromDate=" + today + "&BookingToDate=" + today]
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
            item = BcsdbookingItem()
            item['inmate'] = response.css('.FieldList .Name span::text').extract_first()
            item['bookingdate'] = response.css('.Booking .BookingData .FieldList .BookingDate span::text').extract_first()
            item['totalbondamount'] = response.css('.BookingData .FieldList .TotalBondAmount span::text').extract_first(),
            item['chargedescrption'] = response.css('.BookingData .BookingCharges .Grid tbody .ChargeDescription::text').extract(),
            item['offensedate'] = response.css('.BookingCharges .Grid tbody .OffenseDate::text').extract(),
            item['sourceurl'] = response.url,
            item['image_urls'] = ["http://inmate.co.buchanan.mo.us/" + s for s in response.xpath('//div[@class="BookingPhotos"]/a/@href').extract()]
            yield item