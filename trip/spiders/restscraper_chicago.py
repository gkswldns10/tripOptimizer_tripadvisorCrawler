from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from trip.items import restaurantItem


class restScraper(CrawlSpider):
    name = "rests_chicago"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.com/Restaurants-g35805-Chicago_Illinois.html"]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//*[@id='search-results-content js-search-results-content']"), follow=True, callback='parse_rest'),
        Rule(LinkExtractor(allow="http://yelp.com"), callback='parse_rest')
    )

    def parse_rest(self, response):
        print(response)
        items = []
        item = restaurantItem()
        place_name = response.xpath("//*[@id='HEADING']/text()").extract()
        item['name'] = place_name
        item['category'] = "Restaurant"
        item['city'] = "Chicago, IL"
        address = response.xpath(
            "//*[@id='taplc_location_detail_header_restaurants_0']/div[@class = 'prw_rup prw_common_atf_header_bl headerBL']")
        sub_address = address.xpath(
            "div/div[contains(@class,'blEntry address')]")
        street_address = sub_address.xpath(
            "span[@class='street-address']/text()").extract()
        locality = sub_address.xpath(
            "span[@class='locality']/text()").extract()
        hours = response.xpath(
            '//*[@id="taplc_restaurants_detail_info_content_0"]/div[1]/span[2]/div/span[1]/text()').extract()
        item['address'] = street_address + locality
        item['hours'] = hours

        if(item['title'] != ['\n', '\n', '\n', '\n'] and item['addr'] != [] and item['hours'] != []):
            yield item
            items.append(item)

        return items
