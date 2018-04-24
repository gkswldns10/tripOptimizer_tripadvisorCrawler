from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from trip.items import TripadvisorScraperItem


class tripScraper(CrawlSpider):
    name = "places_la"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.com/Attractions-g32655-Activities-Los_Angeles_California.html"]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="// *[@ id='FILTERED_LIST']/div/div/div/div[1]/div[2]/a[1]"), follow=True, callback='parse_place'),
        Rule(LinkExtractor(allow="http://tripadvisor.com"), callback='parse_place')
    )

    def parse_place(self, response):
        items = []
        item = TripadvisorScraperItem()
        place_name = response.xpath("//*[@id='HEADING']/text()").extract()
        item['name'] = place_name
        item['category'] = "Things to do"
        item['hours'] = ["N/A-N/A"]
        item['city'] = "Los Angeles, CA"
        if(("Tour" not in place_name) and (("Tours") not in place_name)):
            address = response.xpath(
                "//*[@id='taplc_location_detail_header_attractions_0']/div[@class = 'prw_rup prw_common_atf_header_bl headerBL']")
            sub_address = address.xpath("div/div[contains(@class,'blEntry')]")
            street_address = sub_address.xpath(
                "span[@class='street-address']/text()").extract()
            locality = sub_address.xpath(
                "span[@class='locality']/text()").extract()
            item['address'] = street_address + locality
            if(item['address'] != [] and street_address != ""):
                yield item
                items.append(item)

        return items
