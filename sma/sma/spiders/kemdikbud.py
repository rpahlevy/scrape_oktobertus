# -*- coding: utf-8 -*-
import scrapy


class KemdikbudSpider(scrapy.Spider):
    name = 'kemdikbud'
    allowed_domains = ['referensi.data.kemdikbud.go.id']
    start_urls = ['https://referensi.data.kemdikbud.go.id/index11.php']

    def parse(self, response):
        for href in response.css('tr > td > a::attr(href)'):
            yield response.follow(href.get(), callback=self.parse_provinsi)

    def parse_provinsi(self, response):
        for href in response.css('tr > td > a::attr(href)'):
            yield response.follow(href.get(), callback=self.parse_kota)

    def parse_kota(self, response):
        for href in response.css('tr > td > a::attr(href)'):
            yield response.follow(href.get() + '&id=13', callback=self.parse_kecamatan)

    def parse_kecamatan(self, response):
        for row in response.css('tr'):
            col = row.css('td')
            if col is None or len(col) < 5:
                continue
            npsn        = col[1].css('a b::text').get() or ''
            if len(npsn) == 0:
                continue
            nama        = col[2].css('::text').get() or ''
            alamat      = col[3].css('::text').get() or ''
            kelurahan   = col[4].css('::text').get() or ''
            status      = col[5].css('::text').get() or ''
            yield {
                'npsn'      : npsn.strip(),
                'nama'      : nama.strip(),
                'alamat'    : alamat.strip() +', '+ kelurahan.strip(),
                'status'    : status.strip(),
            }


