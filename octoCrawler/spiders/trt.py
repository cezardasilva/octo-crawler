#-*- conding: utf8 -*-
import os
import re
import math
import time
import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector
from octoCrawler.items import ProcessoItem
from octoCrawler.classes.GiantSpider import GiantSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class TrtSpider(CrawlSpider):
    name = "trt"
    start_urls = ["http://aplicacao4.tst.jus.br/consultaProcessual/empregadorForm.do?nomeParte=TELEFONICA+BRASIL+S.A.+&stCheckBox=on&consulta=Consultar"]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(restrict_xpaths=('/html/body/table/tr/td/form/span[2]/a[text()="Proxima"]', ), deny=())),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="processo"]/tbody/tr/td/table/tr/td/a', )), callback='parse_page'),
    )

    def __init__(self, razao_social="TELEFONICA BRASIL S.A.", arquivados=False):
        super(TrtSpider, self).__init__()
        self.gs = GiantSpider()       
        self.razaoSocial = razao_social
        self.arquivados = arquivados              
        

    def parse_page(self, response):
        processo = ProcessoItem()
        processo["processo"] = []
        processo["acompanhamento"] = []

        #Pegar cabecalho do TRT
        for i in range(4, len(response.xpath("/html/table/tr"))):
            restoProcesso = {}
            descricao = response.xpath("/html/table/tr[" + str(i) + "]/td/b/text()").extract();
            valor = response.xpath("/html/table/tr[" + str(i) + "]/td[1]/text()").extract()
            if descricao:
                restoProcesso["descricao"] = descricao[0].strip(' \n\t')
                if valor:                    
                    valor2 = response.xpath("/html/table/tr[" + str(i) + "]/td[2]/font/text()").extract()
                    if valor2: 
                        valorFinal = valor[0].strip('\r\n\t') + valor2[0].strip('\r\n\t')
                    else:
                        valorFinal = valor[0].strip('\r\n\t')
                    restoProcesso["valor"] = valorFinal
            if restoProcesso:                
                processo["processo"].append(restoProcesso)

        #Pegar o Acompanhamento Processual
        for i in range(3, len(response.xpath("/html/table/tr/td/table/tr"))):
            acompanhamento = {}
            data = response.xpath("/html/table/tr/td/table/tr["+str(i)+"]/td[1]/font/text()").extract()
            descricao = response.xpath("/html/table/tr/td/table/tr["+str(i)+"]/td[2]/table/tr/td/font/text()").extract()      
            if not descricao:
                descricao = response.xpath("/html/table/tr/td/table/tr["+str(i)+"]/td[2]/table/tr/td/font/a/text()").extract()
                pass
            acompanhamento["data"] = data[0].strip('\r\n\t')
            acompanhamento["descricao"] = descricao[0].strip('\r\n\t')
            processo["acompanhamento"].append(acompanhamento)

        self.gs.saveItem(processo, "processo_trt");