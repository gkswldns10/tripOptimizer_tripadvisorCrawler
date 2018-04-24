from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from trip.items import restaurantItem
import js2xml
import re

class restScraper(CrawlSpider):
    name = "rests_cu"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.com/Restaurants-g35790-Champaign_Champaign_Urbana_Illinois.html"]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//*[@id='EATERY_SEARCH_RESULTS']"), follow=True, callback='parse_rest'),
        Rule(LinkExtractor(allow="http://tripadvisor.com"), callback='parse_rest')
    )

    def parse_rest(self, response):
        items = []
        item = restaurantItem()
        place_name = response.xpath("//*[@id='HEADING']/text()").extract()
        item['title'] = place_name[0]
        item['category'] = "Restaurants"
        item['city'] = "Champaign"
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


        rating = response.xpath('//*[@id="taplc_location_detail_overview_restaurant_0"]/div[1]/div[2]/div[2]/div[1]/div[1]/span/text()').extract()
        if(rating != []):
            item['rating'] = rating[0]
        item['lat'] = None
        item['lon'] = None

        res = response.xpath('.//div[@class="prv_map clickable"]/img[@width="310"]').extract()
        #print("-"*50)
        #for js in response.xpath('.//script[@type="text/javascript"]/text()').extract()
        ah = response.xpath('.//script[@type="text/javascript"]/text()').extract()
        #print(ah)
        #print("-" * 50)
        for js in response.xpath('.//script[@type="text/javascript"]/text()').extract():
            try:
                jstree = js2xml.parse(js)
                #print(jstree)

                # look for assignment of `var lazyImgs`
                for imgs in jstree.xpath('//var[@name="lazyImgs"]/*'):

                    # use js2xml.make_dict() -- poor name I know
                    # to build a useful Python object
                    data = js2xml.make_dict(imgs)

                    for d in data:
                        if 'center' in d['data']:
                            parsed = re.search(r'center=[\S]*&maptype', d['data']).group(0)
                            print('-'*30)
                            latlong = parsed.split('=')[1].split('&')[0].split(',')
                            item['lat'] = latlong[0]
                            item['lon'] = latlong[1]
                            print('-'*30)
                            break


            except Exception:
                pass


        item['addr'] = street_address[0] + " " + locality[0]
        #rating = response.xpath(
        #    "//span[@class='header_rating']").xpath("span[@class='ui_bubble_rating']/content()").extract()
        #item['rating'] = rating

        item['hours'] = "N/A - N/A"

        if(item['title'] != ['\n', '\n', '\n', '\n'] and item['addr'] != [] and item['hours'] != [] and item['lat'] and item['lon']):
            yield item
            print(item)
            items.append(item)

        return items
