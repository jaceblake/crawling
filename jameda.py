
import scrapy


class JamedaSpider(scrapy.Spider):
    name = "jameda"
    start_urls = [
        'https://www.jameda.de/berlin/aerzte/augenaerzte/dr-safwan-rihawi/uebersicht/81401665_1/',
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
        for content in response.css('.bewertung'):
            single_rating = dict() 
            temp1 = content.css('div.minoTooltip.fragezeichen_cursor::text').extract()
            if (len(temp1) != 0):
                for i,j in zip(temp1,range(len(temp1))):
                    single_rating[i] =  content.css('.note-small::text').extract()[j]
            review = {
               'BName' : content.css('h2 > a::text').extract_first(),
               'BNote': content.css('div.note1::text').extract_first(),
               'BMeta-Info': content.css('div.text > p.text-klein::text').extract_first(),
               'BText': content.css('div.fliesstext::text').extract()[1],
               'BEinzelne-Bewertung' : single_rating
            }
            reviews.append(review)
            
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
            

     
