# -*- coding: utf-8 -*-
import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from tarjetasBlack.items import TarjetasblackItem


class AranyatarjetasblackSpider(CrawlSpider):
	name = "aranyaTarjetasBlack"
	allowed_domains = ["elpais.com"]
	start_urls = (
		'http://elpais.com/especiales/2014/tarjetas-opacas-caja-madrid/',
	)

	# Desde la página principal, se accede a los gastos de cada consejero a través de enlaces que
	# empiezan por apuntes
	rules = (
		Rule(LinkExtractor(allow=('apuntes*')), callback='parse_item', follow=True),
	)

	 # rules = (
  #       # Extract links matching 'category.php' (but not matching 'subsection.php')
  #       # and follow links from them (since no callback means follow=True by default).
  #       Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

  #       # Extract links matching 'item.php' and parse them with the spider's method parse_item
  #       Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
  #   )

	def parse_item(self, response):
		self.log('Hi, this is an item page! %s' % response.url)			

		item = TarjetasblackItem()	

		nombreConsejero = response.url.split('/')[-2] #Nombre no formateado
		nombreH3 = response.xpath(".//h3[@id='nombre']/text()").extract() #Nombre formateado

		if len(nombreH3) > 0:
			nombreConsejero = nombreH3[0]

		#Extraer nombre del cargo. Ej.: consejero nombrado a petición de ...
		cargoSpan = response.xpath(".//span[@class='organizacion']/text()").extract()
		if len(cargoSpan) > 0:
			item['cargo'] = cargoSpan
		
		item['nombreConsejero'] = nombreConsejero

		item['gastos'] = [] #Array vacío al que se añade cada uno de los gastos
		for datos in response.xpath("//tr"):
			if len(datos.xpath(".//th")) == 0: # En las cabeceras no hay información
				gasto = {}
				gasto['importe'] = datos.xpath(".//td[@class='importe']/text()").extract()
				gasto['fecha'] = datos.xpath(".//td[@class='fecha']/text()").extract()
				gasto['hora'] = datos.xpath(".//td[@class='hora']/text()").extract()
				gasto['comercio'] = datos.xpath(".//td[@class='comercio']/text()").extract()
				if isinstance(gasto['comercio'],list):
					gasto['comercio'] = gasto['comercio'][0].strip()

				gasto['actividad'] = datos.xpath(".//td[@class='actividad']/text()").extract()
				gasto['importe'] = datos.xpath(".//td[@class='importe']/text()").extract()
				gasto['operacion'] = datos.xpath(".//td[@class='operacion']/text()").extract()

				item['gastos'].append(gasto)

		if not item['nombreConsejero'].startswith("plus") and len(item['gastos']) > 0:
			yield item
