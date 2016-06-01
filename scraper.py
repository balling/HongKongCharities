import scraperwiki
import re
import scrapy
from datetime import datetime
from scrapy.crawler import CrawlerProcess

def text(l):
	return l[0].strip() if len(l) > 0 else ''

def cell(table, row, column):
	return text(table.xpath('tr[{}]/td[{}]/text()'.format(row, column)).extract())

class CharitiesSpider(scrapy.Spider):
	name = "hkcharities"
	def start_requests(self):
		for i in range(1, 15000):
			yield scrapy.Request('http://www.ird.gov.hk/cgi-bin/irdnew/ach/search.cgi?lang=e&id=91/{:05d},'.format(i), callback=self.parse_page, headers={'User-agent': 'Mozilla/5.0'})

	def parse_page(self, response):
		tables = response.css('table')
		data = {}
		data['name_en'] = cell(tables[0], 1, 2)
		data['name_ch'] = cell(tables[0], 2, 2)
		if(len(data['name_en']) or len(data['name_ch'])):
			data['alias_en'] = cell(tables[0], 3, 2)
			data['alias_ch'] = cell(tables[0], 4, 2)
			data['effective_date'] = datetime.strptime(cell(tables[0], 5, 2),'%d.%m.%Y').date()
			data['uid'] = re.search('(?<=id=).*(?=,)', response.url).group(0)
			last_update_text = response.xpath('//p[@align="right"]/text()').extract()[0].split(' ')[-1]
			data['last_update'] = datetime.strptime(last_update_text, '%d/%m/%Y').date()
			scraperwiki.sqlite.save(unique_keys=['uid'], data=data)

process = CrawlerProcess({'LOG_LEVEL': 'INFO'})
process.crawl(CharitiesSpider)
process.start()
