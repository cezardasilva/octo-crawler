import scrapy
import os
import sys
from scrapy.selector import Selector
from selenium import webdriver
from octoCrawler.items import FidcItem
from octoCrawler.items import FidcInformeMensalItem
from octoCrawler.classes.GiantSpider import GiantSpider


class FidicsSpider(scrapy.Spider):
    name = "Fidcs"
    allowed_domains = ["cvmweb.cvm.gov.br"]
    start_urls = [
        "http://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CConsolFdo/FormBuscaParticFdo.aspx?TP_FIDC=IN489&PK_PARTIC="
    ]

    fidcs_urls = [106297,111771,118537,96308,95803,139408,85553,109689,89969,103021,104764,98190,84006,120039,134269,98953,128391,132491,93608,138297,94716,115390,117665,98500,96762,87968,107825,131264,89162,119507,132220,121671,110665,134156,134146,96788,97160,43464,111159,63632,64284,116793,140483,108021,130309,102748,118662,117692,107155,130356,59871,138454,106736,127391,131978,97883,132271,133538,96800,104765,75957,96418,68016,115627,138111,100209,123305,132747,111781,74763,109968,133599,69045,96467,135917,108432,75974,106444,115933,98730,95639,61273,112845,95487,92133,89288,72110,118868,118529,57886,77890,100360,118669,88841,85729,95735,46877,84975,133895,67292,75163,60945,101793,73687,71204,125040,107408,89651, 70974,  73529, 44682,  141172,  103906,  132696,  127719,  111163,  115859,  43438,  135009,  100796,  132466,  137689,  135924,  110696,  133848,  130840,  107455,  71286,  128221,  141107,  134925,  116364,  114793,  134786,  126550,  141219,  105679,  107436,  120200,  139271,  123652,  138914,  117802,  130985,  108290,  134497,  119531,  125017,  129742,  120840,  133698,  117735,  127679,  101264,  82075,  135789,  127580,  115504,  137352,  131210,  112864,  124176,  112064,  79282,  81777,  82207,  60923,  60942,  120051,  98195,  99336,  107138,  74931,  74788,  79044,  104904,  82717,  104417,  126315,  126787,  138007,  107509,  89282,  120168,  123650,  135681,  136414,  119178,  135067,  128810,  138594,  131861,  133341,  97366,  126454,  116594,  132156,  127578,  116215,  83390,  69221,  133055,  111292,  103655,  131274,  127236,  118891,  109273,  140818,  96758,  134695,  60962,  43088,  58756,  91018,  93467,  117410,  109842,  137255,  110392,  96768,  136006,  130306,  102186,  106257,  58905,  104871,  106128,  118966,  134824,  111779,  57051,  105331,  107566,  109733,  131411,  119672,  94086,  102183,  106284,  92198,  76542,  130814,  42209,  61254,  95722,  112689,  82410,  107290,  70133,  66077,  91549,  137184,  133981,  92126,  138314,  118842,  111948,  127392,  124068,  104050,  94720,  133863,  95057,  84085,  131118,  136654,  110852,  70810,  130314,  95509,  139718,  106336,  89032,  91639,  98598,  137597,  96211,  134870,  106282,  129168,  94827,  60943,  135244,  131447,  77925,  132164,  108243,  81031,  139111,  131120,  105788,  88194,  130984,  94599,  135379,  123353,  102513,  132851,  135264,  87965,  77984,  130810,  91526,  124576,  99644,  120060,  130330,  103022,  115907,  116617,  128778,  115860,  138008,  118812,  102754,  131762,  141589,  105723,  88626,  111441,  129987,  119909,  134224,  111294,  77247,  137531,  94108,  119921,  137686,  124986,  126700,  126553,  134548,  90442,  90178,  129686,  138153,  129581,  101335,  103749,  141679,  125957,  95717,  141580,  133333,  135226,  138639,  87814,  100379,  98724,  119500,  90509,  84825,  76540,  80872,  81798,  84764,  80339,  77775,  76511,  76338,  90500,  92733,  109361,  116122,  99471,  99472,  90639,  138089,  136026,  137540,  120180,  120175,  138868,  126334,  138867,  126084,  138286,  133609,  138863,  126537,  133050,  122591,  135544,  139147,  138864,  77926,  126622,  125195,  125903,  123785,  126538,  121964,  141720,  90144,  127389,  140493,  130117,  92197,  129780,  110480,  138862,  124621,  117732,  96861,  129476,  124064,  102089,  115975,  129928,  105791,  137998,  130564,  123637,  126732,  137539,  86733,  76210,  76331,  110382,  138479,  121440,  132718,  126158,  92341,  130811,  139173,  137535,  136112,  77480,  103713,  126749,  126688,  132027,  140115,  134203,  123275,  125659,  83443,  116723,  134744,  133045,  112088,  127008,  138865,  126445,  119340,  123853,  120305,  91019,  134871,  98140,  127707,  115031,  140677,  99796,  134976,  138504,  73286,  73287,  119706,  136590,  116467,  89691,  132270,  76341,  123859,  117764,  135975,  132267]

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.gs = GiantSpider()

    def parse(self, response):
        for fidc in self.fidcs_urls:
            try:
                self.execute(response, fidc)
            except:
                pass
        self.driver.quit()

    def execute(self, response, fidc):
        self.driver.get(response.url + `fidc`)
        captcha = self.gs.decodeCaptchaBypass("106297", self.driver, "fidc", (996, 266, 1135, 305))

        if captcha:
            captchaInput = self.driver.find_element_by_xpath("//*[@id='numRandom']")
            captchaInput.send_keys(captcha)
            continuarInput = self.driver.find_element_by_xpath("//*[@id='btnContinuar']")
            continuarInput.click()
            error_element = self.driver.find_elements_by_xpath("//*[@id='lblMsg']")
            if error_element:
                self.execute(response, fidc)
            self.html = self.driver.page_source
            _id = self.scrapingHeader()
            self.scrapingInformeMensal(_id)
        else:
            print "Captcha invalido!"

    def scrapingHeader(self):
        data = [];
        fidc = FidcItem()
        fidc["administradora"] = {}
        fidc["diretor"] = {}
        fidc["gestora"] = {}
        fidc["gestora"]["diretor"] = {}
        _id = None
        for sel in Selector(text=self.html).xpath('//*[@id="tabAtivos"]/tbody/tr/td/span'):
            result = sel.xpath('text()').extract()
            if len(result) > 0:
                data.append(result)
            else:
                result = []
                result.append(" ")
                data.append(result)

        if data:
            fidc["denominacao"] = data[1][0]
            fidc["cnpj"] = data[2][0]
            fidc["administradora"]["denominacao"] = data[3][0]
            fidc["administradora"]["cnpj"] = data[4][0]
            fidc["diretor"]["nome"] = data[5][0]
            fidc["diretor"]["cpf"] = data[6]
            fidc["telefone"] = data[7][0]
            fidc["fax"] = data[8][0]
            fidc["email"] = data[9]
            fidc["endereco"] = data[10][0]
            fidc["gestora"]["denominacao"] = data[11][0]
            fidc["gestora"]["cnpj"] = data[12][0]
            fidc["gestora"]["diretor"]["responsavel"] = data[13][0]
            fidc["gestora"]["diretor"]["cpf"] = data[14]
            fidc["gestora"]["telefone"] = data[15][0]
            fidc["gestora"]["fax"] = data[16][0]
            fidc["gestora"]["email"] = data[17]
            if len(data) > 18:
                fidc["gestora"]["endereco"] = data[18][0]
            _id = self.gs.saveItem(fidc, self.name)
            pass
        return _id

    def scrapingInformeMensal(self, _id):
        btn = self.driver.find_element_by_xpath("//*[@id='Hyperlink4']")
        btn.click()
        self.html = self.driver.page_source
        informe_mensal = FidcInformeMensalItem()
        informe_mensal["informe"] = {}
        informe_mensal["cedentes"] = {}

        competencia = Selector(text=self.html).xpath("//*[@id='ddlComptc']/option").extract()
        if competencia:
            for i in range(1, (len(competencia) + 1)):
                btn = self.driver.find_element_by_xpath("//*[@id='ddlComptc']/option[" + str(i) + "]")
                btn.click()
                self.html = self.driver.page_source
                informe = [];

                elements_informe = Selector(text=self.html).xpath("//tr[contains(@style, 'background-color:#FAEFCA;')]")
                for k in range(1, (len(elements_informe))):
                    tmpInforme = {}
                    titulo_descricao = elements_informe[k].xpath("td[1]/span/b/text()").extract()
                    titulo_valor = elements_informe[k].xpath("td[2]/span/text()").extract()
                    descricao = elements_informe[k].xpath("td[1]/span/text()").extract()
                    valor = elements_informe[k].xpath("td[2]/span/text()").extract()
                    if len(titulo_descricao) > 0 and len(titulo_valor) > 0:
                        tmpInforme["descricao"] = titulo_descricao[0].strip(' \r\n\t').strip()
                        tmpInforme["valor"] = titulo_valor[0].strip(' \r\n\t').strip()
                    else:
                        if len(descricao) > 0 and len(valor) > 0:
                            tmpInforme["descricao"] = descricao[0].strip(' \r\n\t').strip()
                            tmpInforme["valor"] = valor[0].strip(' \r\n\t').strip()

                    if tmpInforme:
                        informe.append(tmpInforme)

                cedentes = Selector(text=self.html).xpath("//*[@id='Table6']/tbody/tr")

                cedente = {}

                for j in range(1, (len(cedentes))):
                    cnpj = cedentes[j].xpath("td[2]/span/text()").extract()[0].strip()
                    if cnpj and cnpj <> "0":
                        cedente[cnpj] = cedentes[j].xpath("td[3]/span/text()").extract()[0].strip()

                informe_mensal["_fidic_id"] = _id
                informe_mensal["competencia"] = \
                Selector(text=self.html).xpath("//*[@id='ddlComptc']/option[" + str(i) + "]/text()").extract()[0]
                informe_mensal["informe"] = informe
                if cedente:
                    informe_mensal["cedentes"] = cedente
                else:
                    informe_mensal["cedentes"] = "Nenhum cedente"
                _informe = self.gs.saveItem(informe_mensal, "fidc_informe_mensal")
