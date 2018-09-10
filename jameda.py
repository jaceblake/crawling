# -*- coding: utf-8 -*-

import scrapy


class JamedaSpider(scrapy.Spider):
    name = "jameda"
    start_urls = [
        'https://web.archive.org/web/20161010235748/http://www.jameda.de:80/berlin/aerzte/augenaerzte/fachgebiet/',
    ]

    def parse(self, response):
        
        # follow profile pages
        for url in response.css('.ergebnis-info > h2 > a::attr(href)').extract():
            url = response.urljoin(url)
            yield scrapy.Request(url, self.parse_doctor)
         
        '''
        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)
        
            
        temp = response.css('div.ergebnis')
        for quote in temp:
            self.log(temp.index(quote))
            yield {
                'Id': quote.css('div.jee > div.jee-ranking::text').extract_first(),
                'Entfernung': quote.css('div.jee-km > strong::text').extract_first(),
            }
        '''
     
    def parse_doctor(self, response):
        web = response.css('div > a::attr(href)').extract()[38]
        try: 
            if(web[-2] != 'e'):
                web = 'nicht vorhanden'
        except:
                web = 'nicht vorhanden'
        adresse = ''
        for i in response.css('div > p::text').extract():
            if(len(i) == 12 and  i[6:12] == 'Berlin'):
                temp1 = response.css('div > p::text').extract().index(i)
                adresse = response.css('div > p::text').extract()[temp1-1 :temp1+1]
        kontakt = ''
        for i in response.css('div > div::text').extract():
            if(i[0:3] == '030'):
                kontakt = i
        yield {
            'name': response.css('div > h1::text').extract_first(),
            'adresse': " ".join(adresse),
            'kontakt': kontakt,
            'webpage': web,
            'likes': response.css('div.empfehlungen-blase-inner::text').extract_first(),
            'gesamtnote': response.css('div.zahl::text').extract_first(),
            'weiterempfehlungen': response.css('div.text-klein > div > strong::text').extract()[0],
            'profilaufrufe': response.css('div.text-klein > div > strong::text').extract()[1],
            'kassenpatienten': response.css('div.haken_ja_nein').extract()[0][-7],
            'privatpatienten': response.css('div.haken_ja_nein').extract()[1][-7],
            'Anzahl_Bewertungen': response.css('div.box-gray > span::text').extract_first(),
        }