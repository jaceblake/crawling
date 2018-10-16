
import scrapy


class JamedaSpider(scrapy.Spider):
    name = "jameda"
    start_urls = [
        'https://www.jameda.de/berlin/aerzte/augenaerzte/dr-kirk-nordwald/uebersicht/80121093_1/',
    ]

    headers = {'User-Agent' : 'Mozilla/5.0'}
    base_url = 'https://www.jameda.de'
    boffset_100 = '?boffset=100'
    boffset_200 = '&boffset=200'
    boffset_300 = '&boffset=300'
    boffset_400 = '&boffset=400'

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
            'meta': response.xpath('//*[@id="profillasche_note"]/div[1]/span/text()').extract_first(),
            'reviews' : list()
        }

        reviewsLink = self.base_url + response.xpath('//*[@id="profillasche_note"]/div[1]/a/@href').extract_first()
        
        request = scrapy.Request(url=reviewsLink, headers=self.headers, callback=self.parse_reviews)
        request.meta['item'] = item
        request.meta['reviewsLink'] = reviewsLink
        return request

    def parse_reviews(self, response):
        item = response.meta['item']
        
        reviewsLink = response.meta['reviewsLink']
        
        reviews = list()
        temp = len(response.css('div.bewertung').extract())
        
        
        single_ratings = response.css('table.table.gesamtbewertung')
        for i in range(0,temp):
            try:
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
            except:
                pass
            
        item['reviews'] = item['reviews'] + reviews

        if(int(item['meta']) <= 100):
            # only for test
            file = open('test.txt','w') 
            file.write(str(len(item['reviews']))) 
            file.close() 
            yield item
        elif(int(item['meta']) > 100 and int(item['meta']) < 200):
            temp = int(item['meta']) - 100
            item['meta'] = str(temp)
            url=reviewsLink + self.boffset_100
            yield scrapy.Request(url=url, meta={'item': item,'reviewsLink': reviewsLink}, headers=self.headers, callback=self.parse_reviews)
        elif(int(item['meta']) > 200 and int(item['meta']) < 300):
            temp = int(item['meta']) - 100
            item['meta'] = str(temp)
            url=reviewsLink + self.boffset_100 + self.boffset_200
            yield scrapy.Request(url=url, meta={'item': item,'reviewsLink': reviewsLink}, headers=self.headers, callback=self.parse_reviews)
        elif(int(item['meta']) > 300 and int(item['meta']) < 400):
            temp = int(item['meta']) - 100
            item['meta'] = str(temp)
            url=reviewsLink + self.boffset_100 + self.boffset_200 + self.boffset_300
            yield scrapy.Request(url=url, meta={'item': item,'reviewsLink': reviewsLink}, headers=self.headers, callback=self.parse_reviews)
        elif(int(item['meta']) > 400 and int(item['meta']) < 500):
            temp = int(item['meta']) - 100
            item['meta'] = str(temp)
            url=reviewsLink + self.boffset_100 + self.boffset_200 + self.boffset_300 + self.boffset_400
            yield scrapy.Request(url=url, meta={'item': item,'reviewsLink': reviewsLink}, headers=self.headers, callback=self.parse_reviews)
            

    def more_reviews(self,response):
        item = response.meta['item']
        reviews = list()
        temp = len(response.css('div.bewertung').extract())

        single_ratings = response.css('table.table.gesamtbewertung')
        for i in range(0,temp):
            try:
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
            except:
                pass

        item['reviews'] = item['reviews'] + reviews
        
        # only for test
        file = open('test.txt','w') 
        file.write(str(len(item['reviews']))) 
        file.close() 

        
        yield item
     
