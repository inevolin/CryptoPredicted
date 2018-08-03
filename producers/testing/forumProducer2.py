import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

class MySpider(CrawlSpider):
    name = 'www.blackhatworld.com'
    allowed_domains = ['www.blackhatworld.com']
    start_urls = ['https://www.blackhatworld.com/forums/cryptocurrency.218/']

    rules = (
    	# extract links from subforum
    	# e.g. https://www.blackhatworld.com/forums/cryptocurrency.218/
    	# e.g. https://www.blackhatworld.com/forums/cryptocurrency.218/page-2
    	# follow=True by default if no callback
    	Rule(LinkExtractor(allow=("https://www\.blackhatworld\.com/forums/cryptocurrency\.218/page-\d+((?!\?).)*")), callback='parse_item', follow=True), 
    	# from the above extract links as */seo/* --> this will be direct threads only
    	# from these threads extract only page-x
    	# now we can extract text from pages
    	# otherwise the signatures/other links are messing up our scrape

    	# parse topics:
    	# e.g. https://www.blackhatworld.com/seo/lets-discuss-icos-project-wise-no-ref-links-speculation.1000248/
    	# e.g. https://www.blackhatworld.com/seo/lets-discuss-icos-project-wise-no-ref-links-speculation.1000248/page-2
    	# follow set to True so we can scrape pages within a thread
        #Rule(LinkExtractor(allow=("https://www\.blackhatworld\.com/seo/.*(/|page-\d+)")), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
    	hxs = HtmlXPathSelector(response)
    	with open("log.log", 'ab') as f:
    		f.write((response.url+"\n").encode())
    		threads = hxs.select('//a[contains(@href, "seo/")]/@href').re(r"^seo/.*?/$")
    		for thread in threads:
    			f.write(("\t"+thread+"\n").encode())
    		#pages = hxs.select('//a[contains(@href, "/page-")]/@href').re(r"(http.*?/seo/.*?/page-\d+)$")
    		#for page in pages:
    		#	f.write(("\t"+page+"\n").encode())
        
            