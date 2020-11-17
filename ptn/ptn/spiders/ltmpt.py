# -*- coding: utf-8 -*-
import scrapy


class LtmptSpider(scrapy.Spider):
    name = 'ltmpt'
    allowed_domains = ['sidata-ptn.ltmpt.ac.id']
    start_urls = ['https://sidata-ptn.ltmpt.ac.id/ptn_sb.php']

    def parse(self, response):
        for href in response.css('tr > td > a::attr(href)'):
            yield response.follow(href.get(), callback=self.parse_detail)

    def parse_detail(self, response):
        universitas = response.css('.panel-title::text').get() or ''

        # saintek
        for row in response.css('#jenis1 tbody tr'):
            col = row.css('td')

            prodi           = col[2].css('a::text').get() or ''
            daya_tampung    = col[3].css('::text').get() or 0
            peminat         = col[4].css('::text').get() or 0

            yield {
                'universitas': universitas.strip(),
                'bidang': 'SAINTEK',
                'prodi': prodi.strip(),
                'daya_tampung': daya_tampung.strip(),
                'peminat': peminat.strip(),
            }

        # soshum
        for row in response.css('#jenis2 tbody tr'):
            col = row.css('td')

            prodi           = col[2].css('a::text').get() or ''
            daya_tampung    = col[3].css('::text').get() or 0
            peminat         = col[4].css('::text').get() or 0

            yield {
                'universitas': universitas.strip(),
                'bidang': 'SOSHUM',
                'prodi': prodi.strip(),
                'daya_tampung': daya_tampung.strip(),
                'peminat': peminat.strip(),
            }
