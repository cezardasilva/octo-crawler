import scrapy
import os
from scrapy.selector import Selector
from octoCrawler.items import CndItem
from octoCrawler.classes.GiantSpider import GiantSpider
from selenium import webdriver

class CndSpider(scrapy.Spider):
    name = "cnd"
    url = "http://cnd.dataprev.gov.br/cws/contexto/cnd/cnd.html"
    start_urls = ["http://cnd.dataprev.gov.br/cws/contexto/cnd/cnd.html"]

    def __init__(self, cnpj="02558157000162"):
        self.gs = GiantSpider()
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)             
        self.cnpj = cnpj

    def parse(self, response):        
        frame = self.driver.find_element_by_name("CORPO")
        self.driver.switch_to.frame(frame)

        cnpjInput = self.driver.find_element_by_name("num")
        cnpjInput.send_keys(self.cnpj)
        cnpjSelect = self.driver.find_element_by_xpath("/html/body/center/form/font/p[1]/table/tbody/tr[1]/td/font/input[1]")
        cnpjSelect.click()
        continuarInput = self.driver.find_element_by_xpath("/html/body/center/form/font/p[1]/table/tbody/tr[2]/td[2]/input[1]")
        continuarInput.click()

        self.html = self.driver.page_source

        self.driver.quit()
        return self.scraping()

    def scraping(self):
        certidao = {}
        cnd = CndItem()
        cnd["certidoes"] = []
        cnd["cnpj"] = self.cnpj
        certidaoTotal = Selector(text=self.html).xpath('/html/body/div[2]/table[1]/tbody/tr').extract()        

        for i in range(2, (len(certidaoTotal) + 1)):
            numero = Selector(text=self.html).xpath('/html/body/div[2]/table[1]/tbody/tr['+str(i)+']/td[1]/font/a/text()').extract()
            if numero:
                certidao["numero"] = numero[0]
            else:
                certidao["numero"] = Selector(text=self.html).xpath('/html/body/div[2]/table[1]/tbody/tr['+str(i)+']/td[1]/font/text()').extract()[0]
            certidao["data_emissao"] = Selector(text=self.html).xpath('/html/body/div[2]/table[1]/tbody/tr['+str(i)+']/td[2]/font/text()').extract()[0]
            certidao["fin"] = Selector(text=self.html).xpath('/html/body/div[2]/table[1]/tbody/tr['+str(i)+']/td[3]/font/text()').extract()[0]
            certidao["data_validade"] = Selector(text=self.html).xpath('/html/body/div[2]/table[1]/tbody/tr['+str(i)+']/td[4]/font/text()').extract()[0]
            certidao["data_cancelamento"] = Selector(text=self.html).xpath('/html/body/div[2]/table[1]/tbody/tr['+str(i)+']/td[5]/font/text()').extract()[0]
            certidao["hora_brasilia"] = Selector(text=self.html).xpath('/html/body/div[2]/table[1]/tbody/tr['+str(i)+']/td[6]/font/text()').extract()[0]
            cnd["certidoes"].append(certidao)
            
        captcha = self.gs.saveItem(cnd, self.name)