# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import TakeFirst


class BasesPublicasItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FidcItem(scrapy.Item):
    _id = scrapy.Field()
    denominacao = scrapy.Field()
    administradora = scrapy.Field()
    gestora = scrapy.Field()
    cnpj = scrapy.Field()
    telefone = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    endereco = scrapy.Field()
    diretor = scrapy.Field()

class FidcInformeMensalItem(scrapy.Item):
    _fidic_id = scrapy.Field()
    competencia = scrapy.Field()
    informe = scrapy.Field()
    cedentes = scrapy.Field()

class ReceitaItem(scrapy.Item):
    cnpj = scrapy.Field()
    data_constituicao = scrapy.Field()
    razao_social = scrapy.Field()
    nome_fantasia = scrapy.Field()
    atividade_economica = scrapy.Field()
    natureza_juridica = scrapy.Field()
    endereco = scrapy.Field()
    contato = scrapy.Field()
    cadastral = scrapy.Field()
    qsa = scrapy.Field()
    html_cartao_cnpj = scrapy.Field()

class ProcessoItem(scrapy.Item):
    processo = scrapy.Field()
    acompanhamento = scrapy.Field()

class CndItem(scrapy.Item):
    cnpj = scrapy.Field()
    certidoes = scrapy.Field()

