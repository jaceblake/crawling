import scrapy


class JamedaSpider(scrapy.Spider):
    name = "jameda"
    start_urls = [
        'https://www.jameda.de/berlin/aerzte/augenaerzte/dr-kirk-nordwald/bewertungen/80121093_1/',
    ]

    headers = {'User-Agent' : 'Mozilla/5.0'}
    
    def start_requests(self):
        for url,tag in zip(self.start_urls, range(len(self.start_urls))):
            yield scrapy.Request(url=url, meta={'url': url, 'id': tag}, headers=self.headers, callback=self.more_reviews)
            
    def more_reviews(self,response):
        item = dict()
        
        reviews = list()
        for content in response.css('.bewertung'):
            single_rating = dict() 
            temp1 = content.css('div.minoTooltip.fragezeichen_cursor::text').extract()
            if (len(temp1) != 0):
                for i,j in zip(temp1,range(len(temp1))):
                    single_rating[i] =  content.css('.note-small::text').extract()[j]
            else:
                pass
            
            review = {
               'BName' : content.css('h2 > a::text').extract_first(),
               'BNote': content.css('div.note1::text').extract_first(),
               'BMeta-Info': content.css('div.text > p.text-klein::text').extract_first(),
               'BText': content.css('div.fliesstext::text').extract()[1],
               'BEinzelne-Bewertung' : single_rating
            }
            reviews.append(review)

        item['reviews'] = reviews
       
        yield item