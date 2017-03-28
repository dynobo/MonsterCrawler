import scrapy
import json
import re
import os.path


class linksSpider(scrapy.Spider):
    name = "links"

    def __init__(self, search=None, *args, **kwargs):
        super(linksSpider, self).__init__(*args, **kwargs)
        urls = {
            'itinstuttgart': (
                 'https://www.monster.de/jobs/suche/'
                 '?q=IT'
                 '&where=stuttgart'
                 '&cy=de'
                 '&client=power'
                 '&rad=20'
                 ),
            'datascience': (
                          'https://www.monster.de/jobs/suche/'
                          '?q=Data-Science'
                          '&cy=de'
                          '&client=power'
                          )
        }
        url = urls[search]
        self.start_urls = []
        for i in range(1, 40):
            self.start_urls.append(url + '&page=' + str(i))

    def parse(self, response):
        for job in response.css('article.js_result_row'):
            title = job.css('.jobTitle *::text').extract()
            company = job.css('.company *::text').extract()
            location = job.css('.location *::text').extract()
            postdate = job.css('.postedDate time::attr(datetime)').extract_first()
            postdate = re.sub('T\d\d:\d\d', '', postdate)
            url = job.css('.jobTitle a::attr(href)').extract_first()
            yield {
                'title': ' '.join(title).strip(),
                'company': ' '.join(company).strip(),
                'location': ' '.join(location).strip(),
                'date': postdate.strip(),
                'url': url.strip(),
            }


class jobsSpider(scrapy.Spider):
    name = 'jobs'
    linksFile = ''

    def __init__(self, search=None, *args, **kwargs):
        super(jobsSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.linksFile = search+'.json'
        if (os.path.isfile(self.linksFile)):
            with open(self.linksFile) as f:
                data = json.load(f)
            for item in data:
                self.start_urls.append(item['url'])

    def parse(self, response):
        url = response.request.url

        # Load meta data
        with open(self.linksFile) as f:
            data = json.load(f)
            for item in data:
                if (item['url'] == url):
                    title = item['title']
                    company = item['company']
                    location = item['location']
                    date = item['date']
                    break

        # Parse Job Description and remove HTML Tags
        for text in response.xpath('//span[@id="TrackingJobBody"]').extract():
            text = re.sub('<!--.*?-->', ' ', text)
            text = re.sub('<.*?>', ' ', text)
            text = text.replace('&amp;', '&')
            text = re.sub('\s+', ' ', text).strip()

            yield {
                'url': url,
                'title': title,
                'company': company,
                'location': location,
                'date': date,
                'text': text
            }
