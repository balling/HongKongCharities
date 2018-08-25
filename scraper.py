#import scraperwiki
import scrapy
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
from functools import partial

def text(l):
	return l[0].strip() if len(l) > 0 else ''

def cell(table, row, column):
	return text(table.xpath('tr[{}]/td[{}]/text()'.format(row, column)).extract())

class CharitiesSpider(scrapy.Spider):
	name = "hkcharities"
	custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
    }
	def start_requests(self):
		for i in range(1, 16000):
			uid = '91/{:05d}'.format(i)
			yield FormRequest('https://www.ird.gov.hk/charity/view_detail.php', formdata={'org_id':uid}, callback=partial(self.parse_page, uid=uid))

	def parse_page(self, response, uid):
		tables = response.css('table')
		if(len(tables) == 0):
			return
		table = tables[0]
		data = {}
		data['name_en'] = cell(table, 1, 2)
		data['name_ch'] = cell(table, 2, 2)
		if(len(data['name_en']) or len(data['name_ch'])):
			data['alias_en'] = cell(table, 3, 2)
			data['alias_ch'] = cell(table, 4, 2)
			data['effective_date'] = datetime.strptime(cell(table, 5, 2),'%d.%m.%Y').date()
			data['uid'] = uid
			last_update_text = response.xpath('//p[@align="right"]/text()').extract()[0].split(' ')[-1]
			data['last_update'] = datetime.strptime(last_update_text, '%d/%m/%Y').date()
			print(data)
			# scraperwiki.sqlite.save(unique_keys=['uid'], data=data)

process = CrawlerProcess({'LOG_LEVEL': 'INFO'})
process.crawl(CharitiesSpider)
process.start()
