import scrapy
from scrapy.http import Request
import json

class BlogSpider(scrapy.Spider):
    name = 's-dk'
    cookie = {'sessionid': '<REPLACE_WITH_COOKIE_VALUE>'}
    custom_settings = {
        'FEED_URI': 'tenancies_full.csv',
        'FEED_FORMAT': 'csv'
    }

    def start_requests(self):
        yield Request('https://s.dk/api/tenancy/?format=json', cookies=self.cookie)

    def parse(self, response):
        # scrapy.shell.inspect_response(response, self)
        data = json.loads(response.body_as_unicode())
        for result in data['results']:
            flat = dict(result)
            flat.update(result['address'])
            del flat['address']
            url = flat['properties']
            if not url.endswith('?format=json'):
                url = url + '?format=json'

            yield response.follow(
                url,
                self.parse_properties,
                cookies=self.cookie,
                meta={'tenancy': flat},
                dont_filter=True
            )

        try:
            yield response.follow(data['next'], self.parse, cookies=self.cookie)
        except KeyError as e:
            pass

    def parse_properties(self, response):
        tenancy_properties = json.loads(response.body_as_unicode())
        tenancy_properties['pk_property'] = tenancy_properties.pop('pk')
        deposit, rent = 0, 0
        try:
            for expense in tenancy_properties['expenses']:
                if expense['definition'].lower() not in ['deposit', 'indskud']:
                    deposit = expense['amount']
                else:
                    rent += expense['amount']
        except KeyError:
            pass

        tenancy_properties['rent'] = rent
        tenancy_properties['deposit'] = deposit
        tenancy_properties.update(response.meta['tenancy'])

        yield tenancy_properties
