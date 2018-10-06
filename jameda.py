
import scrapy


class JamedaSpider(scrapy.Spider):
    name = "jameda"
    start_urls = [
        'https://www.jameda.de/berlin/aerzte/urologen/dr-christian-klopf/uebersicht/81098175_1/',
    ]

    headers = {'User-Agent' : 'Mozilla/5.0'}
    base_url = 'https://www.jameda.de'

    def start_requests(self):
        for url,tag in zip(self.start_urls, range(len(self.start_urls))):
            yield scrapy.Request(url=url, meta={'url': url, 'id': tag}, headers=self.headers, callback=self.parse)

    def parse(self, response):
        tag = 1 + response.meta['id']
        url = response.meta['url']
        item = {
            'ID'  : tag,
            'Jameda-Links' : url,
            'Name': response.xpath('//*[@id="profil_name_adresse"]/h1/text()').extract_first(),
            'Adresse': ''.join(response.xpath('//*[@id="profil_name_adresse"]/p[2]/text()').extract()),
            'Kontakt': response.xpath('//*[@id="profil_name_adresse"]/div[3]/text()').extract_first(),
            'Webpage': response.xpath('//*[@id="profil_name_adresse"]/div[3]/a/text()').extract_first(),
            'Likes': response.xpath('//*[@id="empfCount"]/text()').extract_first(),
            'Gesamtnote': response.xpath('//*[@id="profillasche_note"]/span/div[2]/text()').extract_first(),
            'Weiterempfehlungen': response.xpath('//*[@id="profillasche_kleintext"]/div[1]/strong/text()').extract_first(),
            'Profilaufrufe': response.xpath('//*[@id="profillasche_kleintext"]/div[2]/strong/text()').extract_first(),
            'Gesetzlich-Versicherte': response.xpath('//*[@id="content"]/div[2]/div[2]/div[2]/div[1]/div[1]/div/text()').extract_first(),
            'Privatversicherte': response.xpath('//*[@id="content"]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/text()').extract_first(),
            'Anzahl-Bewertungen': response.xpath('//*[@id="profillasche_note"]/div[1]/span/text()').extract_first(),
            'reviews' : list()
        }

        reviewsLink = self.base_url + response.xpath('//*[@id="profillasche_note"]/div[1]/a/@href').extract_first()
        
        request = scrapy.Request(url=reviewsLink, headers=self.headers, callback=self.parse_reviews)
        request.meta['item'] = item
        return request

    def parse_reviews(self, response):
        item = response.meta['item']
        reviews = list()
        temp = len(response.css('div.bewertung').extract())
        
        
        single_ratings = response.css('table.table.gesamtbewertung')
        for i in range(0,temp):
            single_rating = dict()
            temp1 = len(single_ratings[i].css('div.minoTooltip.fragezeichen_cursor::text').extract())
            for j in range(0,temp1):
                single_rating[single_ratings[i].css('div.minoTooltip.fragezeichen_cursor::text').extract()[j]] =                                                                                   single_ratings[i].css('.note-small::text').extract()[j]
            review = {
                'BName': response.css('h2 > a::text').extract()[i],
                'BNote': response.css('div.note1::text').extract()[i],
                'BMeta-Info': response.css('div.text > p.text-klein::text').extract()[i],
                'BText': response.css('div.fliesstext::text').extract()[i+1] + response.css('div.fliesstext::text').extract()[i+2],
                'BEinzelne-Bewertung' : single_rating
            }
            reviews.append(review)
            
        item['reviews'] = item['reviews'] + reviews

        if(int(item['Anzahl-Bewertungen']) <= 100):
            
            yield item
        else:
            half_link = response.xpath('//*[@id="content"]/div[1]/div[1]/div[{0}]/a[1]/@href'.format(3)).extract_first()
            if(isinstance(half_link, str)):
                reviewsLink = self.base_url + half_link
                yield scrapy.Request(url=reviewsLink, meta={'item': item}, headers=self.headers, callback=self.parse_reviews)
            else:
                half_link = response.xpath('//*[@id="content"]/div[1]/div[1]/div[{0}]/a[1]/@href'.format(5)).extract_first()
                reviewsLink = self.base_url + half_link
                yield scrapy.Request(url=reviewsLink, meta={'item': item}, headers=self.headers, callback=self.more_reviews)

    def more_reviews(self,response):
        item = response.meta['item']
        reviews = list()
        temp = len(response.css('div.bewertung').extract())

        single_ratings = response.css('table.table.gesamtbewertung')
        for i in range(0,temp):
            single_rating = dict()
            temp1 = len(single_ratings[i].css('div.minoTooltip.fragezeichen_cursor::text').extract())
            for j in range(0,temp1):
                single_rating[single_ratings[i].css('div.minoTooltip.fragezeichen_cursor::text').extract()[j]] =                                                                                   single_ratings[i].css('.note-small::text').extract()[j]
            review = {
                'BName': response.css('h2 > a::text').extract()[i],
                'BNote': response.css('div.note1::text').extract()[i],
                'BMeta-Info': response.css('div.text > p.text-klein::text').extract()[i],
                'BText': response.css('div.fliesstext::text').extract()[i+1] + response.css('div.fliesstext::text').extract()[i+2],
                'BEinzelne-Bewertung' : single_rating
            }
            reviews.append(review)

        item['reviews'] = item['reviews'] + reviews
        
        # only for test
        file = open('test.txt','w') 
        file.write(str(len(item['reviews']))) 
        file.close() 

        
        yield item
     
