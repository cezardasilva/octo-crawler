import scrapy
import os
import re
from scrapy.selector import Selector
from octoCrawler.items import ReceitaItem
from octoCrawler.classes.GiantSpider import GiantSpider
from selenium import webdriver

class ReceitaFederalSpider(scrapy.Spider):
    name = "ReceitaFederal"
    url = "http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/valida.asp"
    start_urls = ["http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/valida.asp"]

    def __init__(self, cnpj="21101794000150"):
        self.gs = GiantSpider()
        self.driver = webdriver.Firefox()                   
        self.cnpj = cnpj

    def parse(self, response):         
        self.driver.get(self.url)  
        
        self.fillForm()        

        self.html = self.driver.page_source

        receita = self.scraping()

        qsaButton = self.driver.find_element_by_name("qsa")
        qsaButton.click()

        self.html = self.driver.page_source 
        self.driver.close()       
        self.driver.quit()
        receita = self.scrapingQSA(receita)
        self.gs.saveItem(receita, self.name)
        self.gs.updateFile(self.cnpj);



    def fillForm(self):
        captcha = self.gs.decodeCaptchaBypass(self.cnpj, self.driver, self.name, (182,150,363,199))

        cnpjInput = self.driver.find_element_by_xpath("//*[@id='cnpj']")
        cnpjInput.send_keys(self.cnpj)

        captchaInput = self.driver.find_element_by_xpath("//*[@id='txtTexto_captcha_serpro_gov_br']")
        captchaInput.send_keys(captcha)

        continuarInput = self.driver.find_element_by_xpath("//*[@id='submit1']")
        continuarInput.click()

        error = self.driver.find_elements_by_xpath("//*[@id='theForm']/font/font/table/tbody/tr[2]/td/font/b");
        if len(error) > 0:
            self.fillForm()

    def scraping(self):
        receita = ReceitaItem()
        receita['endereco'] = {}
        receita['contato'] = {}
        receita['cadastral'] = {}

        pre_xpath = "/html/body/table[2]/tbody/tr/td/"
        cnpjValido = Selector(text=self.html).xpath(pre_xpath + 'table[2]/tbody/tr/td[1]/font[2]/b[1]/text()');
        if cnpjValido:
            cnpj = Selector(text=self.html).xpath(pre_xpath + 'table[2]/tbody/tr/td[1]/font[2]/b[1]/text()').extract()[0].strip(' \r\n\t')
            receita['cnpj'] = re.sub('[./-]', '', cnpj)
            receita['data_constituicao'] = Selector(text=self.html).xpath(pre_xpath + '/table[2]/tbody/tr/td[3]/font/b/text()').extract()[0].strip(' \r\n\t') 
            receita['razao_social'] = Selector(text=self.html).xpath(pre_xpath + 'table[3]/tbody/tr/td/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita['nome_fantasia'] = Selector(text=self.html).xpath(pre_xpath + 'table[4]/tbody/tr/td/font[2]/b/text()').extract()[0].strip(' \r\n\t')

            atividade_primaria = Selector(text=self.html).xpath(pre_xpath + 'table[5]/tbody/tr/td/font[2]/b').extract()
            
            #receita['atividade_economica_primaria'] = Selector(text=self.html).xpath(pre_xpath + 'table[2]/tbody/tr/td[1]/font[2]/b[1]/text()').extract()[0] 
            #receita['atividade_economica_secundaria'] = Selector(text=self.html).xpath(pre_xpath + 'table[2]/tbody/tr/td[1]/font[2]/b[1]/text()').extract()[0] 


            receita['natureza_juridica'] = Selector(text=self.html).xpath(pre_xpath + 'table[7]/tbody/tr/td/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            #Preencher o Endereco
            receita['endereco']['logradouro'] = Selector(text=self.html).xpath(pre_xpath + 'table[8]/tbody/tr/td[1]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita["endereco"]["numero"] = Selector(text=self.html).xpath(pre_xpath + 'table[8]/tbody/tr/td[3]/font[2]/b/text()').extract()[0].strip(' \r\n\t')
            receita["endereco"]["complemento"] = Selector(text=self.html).xpath(pre_xpath + 'table[8]/tbody/tr/td[5]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita["endereco"]["bairro"] = Selector(text=self.html).xpath(pre_xpath + 'table[9]/tbody/tr/td[3]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita["endereco"]["cidade"] = Selector(text=self.html).xpath(pre_xpath + 'table[9]/tbody/tr/td[5]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita["endereco"]["uf"] = Selector(text=self.html).xpath(pre_xpath + 'table[9]/tbody/tr/td[7]/font[2]/b/text()').extract()[0].strip(' \r\n\t')
            receita["endereco"]["cep"] = Selector(text=self.html).xpath(pre_xpath + 'table[9]/tbody/tr/td[1]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            #Preencher o Contato
            receita['contato']['email'] = Selector(text=self.html).xpath(pre_xpath + 'table[10]/tbody/tr/td[1]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita['contato']['telefone'] = Selector(text=self.html).xpath(pre_xpath + 'table[10]/tbody/tr/td[1]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita['contato']['ente_federativo_responsavel'] = Selector(text=self.html).xpath(pre_xpath + 'table[11]/tbody/tr/td/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            #Preencher os dados Cadastrais
            receita['cadastral']['situacao'] = Selector(text=self.html).xpath(pre_xpath + 'table[12]/tbody/tr/td[1]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita['cadastral']['data'] = Selector(text=self.html).xpath(pre_xpath + 'table[12]/tbody/tr/td[3]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            receita['cadastral']['motivo'] = Selector(text=self.html).xpath(pre_xpath + 'table[13]/tbody/tr/td/font[2]/b/text()').extract()[0].strip(' \r\n\t')
            receita['cadastral']['situacao_especial'] = Selector(text=self.html).xpath(pre_xpath + 'table[14]/tbody/tr/td[1]/font[2]/b/text()').extract()[0].strip(' \r\n\t')
            receita['cadastral']['data_especial'] = Selector(text=self.html).xpath(pre_xpath + 'table[14]/tbody/tr/td[3]/font[2]/b/text()').extract()[0].strip(' \r\n\t') 
            #Preencher evidencia do cartao CNPJ
            receita["html_cartao_cnpj"] = self.html
        return receita

    def scrapingQSA(self, receita):
        #Preencher QSA
        receita['qsa'] = {}
        capital_social = Selector(text=self.html).xpath('/html/body/table[2]/tbody/tr/td/table/tbody/tr[3]/td[2]/text()')
        if capital_social:
            receita['qsa']['capital_social'] = capital_social.extract()[0].strip(' \r\n\t')
        else:
            receita['qsa']['capital_social'] = "NAO PREENCHIDO"

        qsa = Selector(text=self.html).xpath('/html/body/table[3]/tbody/tr/td/table[3]/tbody/tr')
        if qsa:
            receita['qsa']['quadro_social'] = []
            quadros = Selector(text=self.html).xpath('/html/body/table[3]/tbody/tr/td/table[3]/tbody/tr')
            for k in range(1, (len(quadros))):
                tmpQuadro = {}
                nome_empresarial = Selector(text=self.html).xpath('/html/body/table[3]/tbody/tr/td/table[3]/tbody/tr['+str(k)+']/td/fieldset/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/text()').extract()
                qualificacao = Selector(text=self.html).xpath('/html/body/table[3]/tbody/tr/td/table[3]/tbody/tr['+str(k)+']/td/fieldset/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/text()').extract()
                if len(nome_empresarial) > 0:
                    tmpQuadro["nome_empresarial"] = nome_empresarial[0].strip(' \r\n\t')
                    if len(qualificacao) > 0:
                        tmpQuadro["qualificacao"] = qualificacao[0].strip(' \r\n\t')
                        receita['qsa']['quadro_social'].append(tmpQuadro)

                
        else:
            receita['qsa']['quadro_social'] = "A NATUREZA JURIDICA NAO PERMITE O PREENCHIMENTO DO QSA";
            
        return receita