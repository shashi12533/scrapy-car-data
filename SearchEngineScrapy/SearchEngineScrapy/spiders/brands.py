# -*- coding: utf-8 -*-
import scrapy
import json
import ast
import xlrd
from collections import defaultdict
import json


class BrandsSpider(scrapy.Spider):

    name = 'brands'
    allowed_domains = ['http://www.oriparts.com']
    loc = ('../MarutiAutoParts/Ciaz/Ciaz-1-2990.xlsx')
    rotate_user_agent = True
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 6)
    data=[]
    for i in range(sheet.nrows):
        if len(sheet.cell_value(i, 6))>15:
            data.append(sheet.cell_value(i, 6))
    # print(len(data))
    start_urls = [i for i in data[200:400]]
    # start_urls = ['https://boodmo.com/catalog/part-nut-6767270/','https://boodmo.com/catalog/part-switch_assy_lighting_turn-6773719/',
    #               'https://boodmo.com/catalog/part-spark_plug-6772555/',
    #               'https://boodmo.com/catalog/part-cushion_glove_box_side-6787085/'
     #]

    def __init__(self, category=None):
        self.failed_urls = []

    # start_urls = ['http://oriparts.com/redirect/product/110600',
    #               'http://oriparts.com/redirect/product/1361919',
    #               'http://oriparts.com/redirect/product/1361920',
    #               'http://oriparts.com/redirect/product/86034',
    #               'http://oriparts.com/redirect/product/1349691',
    #               'https://boodmo.com/catalog/part-brake_assy_rear_rh-6793979/']

    #     start_urls = ['http://oriparts.com/redirect/product/1349691']

    # with open('ttt.text','w') as f:
    #     for i in start_urls:
    #         f.write(str(i))
    #         f.write("\n")

    # def start_requests(self):
    #     urls = self.start_urls
    #     for url in urls:
    #         proxy = 'http://104.248.115.226	:9090'
    #         yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': proxy})

    def parse(self, response):
        print(response.url)
        if response.status == 404:
            self.crawler.stats.inc_value('failed_url_count')
            self.failed_urls.append(response.url)
        l = ['Partlink', 'PartName', 'PartNo', 'Brand', 'Price', 'PartImg', 'Origin', 'Class', 'Feature', 'Mrp']
        PartName = str(response.xpath(
            '//*[@id="replacement_parts_page"]/div[2]/div[2]/div[2]/div[1]/h2/text()').extract_first()).strip("\n\t")
        PartName = PartName.strip()
        PartNo = str(response.xpath(
            '//*[@id="replacement_parts_page"]/div[2]/div[2]/div[2]/ul[1]/li[1]/span/text()').extract_first()).strip(
            "\n\t")
        PartNo = PartNo.strip()
        Brand = str(response.xpath(
            '//*[@id="replacement_parts_page"]/div[2]/div[2]/div[2]/ul[1]/li[2]/a/text()').extract_first()).strip(
            "\n\t")
        Brand = Brand.strip()
        Partlink = response.url
        Origin = str(response.xpath(
            '//*[@ id = "replacement_parts_page"]/div[2]/div[2]/div[2]/ul[1]/li[3]/text()').extract_first()).strip(
            "\n\t")
        Origin = Origin.strip()
        Price = str(response.xpath('//*[@id="part_block_price"]/div[1]/div[1]/span[1]/text()').extract_first()).strip(
            "\n\t")
        Price = Price.strip()
        PartImg = response.xpath('//*[@id="main-image"]/@src').getall()[0]
        try:
            Mrp = str(response.xpath('//*[@id="part_block_price"]/div[1]/div[2]/text()[2]').getall()[0])
            Mrp = Mrp.strip()
        except Exception as e:
            Mrp = None
        # code mein gadbadi hao
        Class = str(response.xpath(
            '//*[@id="replacement_parts_page"]/div[2]/div[2]/div[2]/ul[2]/li/b/text()').extract_first()).strip("\n\t")
        Class = Class.strip()

        Features = response.xpath('//*[@id="replacement_parts_page"]/div[2]/div[2]/div[2]/ul[3]/li')
        Feature = ''
        for idx in range(len(Features)):
            c = Features[idx].xpath('text()').getall()[0]
            Feature = Feature + c
            Feature = Feature + "\n"

        Af = response.xpath('//*[@id="replacement_parts_page"]/div[2]/div[4]/div[2]/div[1]/div[1]/a')
        aftermarket_keys = {}
        aftermarket_keys = {'Af' + str(idx + 1): None for idx in range(10)}
        aftermarket_check = response.xpath("//*[contains(text(), 'AFTERMARKET')]")
        if aftermarket_check:
            for idx in range(len(Af)):
                f = Af[idx].xpath('span')
                s = ""
                for idy in range(len(f)):
                    c = f[idy].xpath('text()').getall()[0]
                    s = s + c
                    s = s + "\n"
                aftermarket_keys.update({"Af" + str(idx + 1): s})
        oem = response.xpath('//*[@id="replacement_parts_page"]/div[2]/div[6]/div[2]/div/div/a')
        oem_keys = {}
        oem_keys = {'Oem' + str(idx + 1): None for idx in range(10)}
        oem_check = response.xpath("//*[contains(text(), 'OEM Replacement Parts')]")
        if len(oem_check) > 0 and len(aftermarket_check)==0:
            oem = response.xpath('//*[@id="replacement_parts_page"]/div[2]/div[4]/div[2]/div/div[1]/a')
            oem_keys = {'Oem' + str(idx + 1): None for idx in range(10)}
            for idx in range(len(oem)):
                f = oem[idx].xpath('span')
                s = ""
                for idy in range(len(f)):
                    c = f[idy].xpath('text()').getall()[0]
                    s = s + c
                    s = s + "\n"
                oem_keys.update({"Oem" + str(idx + 1): s})
        else:
            if len(oem_check)>0:
                for idx in range(len(oem)):
                    f = oem[idx].xpath('span')
                    s = ""
                    for idy in range(len(f)):
                        c = f[idy].xpath('text()').getall()[0]
                        s = s + c
                        s = s + "\n"
                    oem_keys.update({"Oem" + str(idx + 1): s})

        compat = response.xpath('//*[@id="parts-compatibility-tab-1"]/a')
        comp_keys = {}
        comp_keys = {'Comp' + str(idx + 1): None for idx in range(500)}
        comp_check = response.xpath("//*[contains(text(), 'COMPATIBILITY')]")
        if len(comp_check) > 0:
            for idx in range(len(compat)):
                f = compat[idx].xpath('span')
                s = ""
                for idy in range(len(f)):
                    c = f[idy].xpath('text()').getall()[0]
                    s = s + c
                    s = s + "\n"
                comp_keys.update({"Comp" + str(idx + 1): s})
        resp = {}
        resp.update({l[0]: Partlink})
        resp.update({l[1]: PartName})
        resp.update({l[2]: PartNo})
        resp.update({l[3]: Brand})
        resp.update({l[4]: Price})
        resp.update({l[5]: PartImg})
        resp.update({l[6]: Origin})
        resp.update({l[7]: Class})
        newd = {**resp, **aftermarket_keys}
        newd1 = {**newd, **oem_keys}
        newd2 = {**newd1, **comp_keys}
        newd2.update({l[8]: Feature})
        newd2.update({l[9]: Mrp})
        # newd = {**resp,**oem_keys}
        # newd1 = {**newd,**aftermarket_keys}
        # newd2 ={**newd1,**comp_keys}
        # import csv
        # with open('output.csv', 'a') as output:
        #     writer = csv.writer(output)
        #     for key, value in newd2.iteritems():
        #         writer.writerow([key, value])
        yield newd2

        # a_selectors = response.xpath("//a")
        # for selector in a_selectors:
        #     link = selector.xpath("@href").extract_first()
        #     if link[0]=='/':
        #         yield {"link":'https://www.carparts.com'+link}
    # link = 'https://www.carparts.com'+link
    # request = response.follow(link, callback=self.parse)
    # yield request.body
    # with open('out.json','r') as f:
    # data = ast.literal_eval(f.read())

    # def parse(self, response):
    #     global a_selectors
    #     a_selectors = ''
    #     a_selectors = str(response.xpath('//*[@id="articles"]/div/p/text()').extract_first()).strip("\n\t")
    #     if len(a_selectors) < 5:
    #         a_selectors = str(response.xpath('//*[@id="articles"]/div/text()').extract_first()).strip("\n\t")
    #     brand_name = str(response.xpath('//*[@id="Breadcrumbs"]/div/span/a/span/text()').extract_first())
    #     # if a_selectors=="":
    #     #     a_selectors = str(response.xpath('//*[@id="articles"]/div/p/text()').extract_first())
    #     yield {brand_name: a_selectors.strip("\n\t")}

    def handle_spider_closed(self,spider, reason):
        self.crawler.stats.set_value('failed_urls', ','.join(spider.failed_urls))

    def process_exception(self, response, exception, spider):
        ex_class = "%s.%s" % (exception.__class__.__module__, exception.__class__.__name__)
        self.crawler.stats.inc_value('downloader/exception_count', spider=spider)
        self.crawler.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)

