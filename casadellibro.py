import scrapy
import logging
import re
class CasaDelLibroSpider(scrapy.Spider):
    name = 'casadellibro'
    allowed_domains = ['casadellibro.com']
    start_urls = ["https://www.casadellibro.com/libros/libros-de-actualidad"]
    urls = []
    merchants = []
    logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response):
        for url in ["https://www.casadellibro.com/libros/libros-de-actualidad",
"https://www.casadellibro.com/libros/novedades-libros-infantiles",
"https://www.casadellibro.com/libros/libros/arte/101000000",
"https://www.casadellibro.com/libros/libros/autoayuda-y-espiritualidad/102000000",
"https://www.casadellibro.com/libros/libros/ciencias-humanas/104000000",
"https://www.casadellibro.com/libros/libros/ciencias-politicas-y-sociales/105000000",
"https://www.casadellibro.com/libros/libros/ciencias/103000000",
"https://www.casadellibro.com/libros/libros/cocina/106000000",
"https://www.casadellibro.com/libros/libros/comics-manga-infantil-y-juvenil/412000000",
"https://www.casadellibro.com/libros/libros/comics/411000000",
"https://www.casadellibro.com/libros/libros/deportes-y-juegos/108000000",
"https://www.casadellibro.com/libros/libros/derecho/109000000",
"https://www.casadellibro.com/libros/libros/economia/110000000",
"https://www.casadellibro.com/libros/libros/empresa/111000000",
"https://www.casadellibro.com/libros/libros/filologia/112000000",
"https://www.casadellibro.com/libros/libros/fotografia/113000000",
"https://www.casadellibro.com/libros/libros/guias-de-viaje/114000000",
"https://www.casadellibro.com/libros/libros/historia/115000000",
"https://www.casadellibro.com/libros/libros/idiomas/116000000",
"https://www.casadellibro.com/libros/libros/infantil/117000000",
"https://www.casadellibro.com/libros/libros/informatica/118000000",
"https://www.casadellibro.com/libros/libros/ingenieria/119000000",
"https://www.casadellibro.com/libros/libros/juvenil/117001014",
"https://www.casadellibro.com/libros/libros/libros-de-texto-y-formacion/132000000",
"https://www.casadellibro.com/libros/libros/libros-latinoamericanos/417000000",
"https://www.casadellibro.com/libros/libros/literatura/121000000",
"https://www.casadellibro.com/libros/libros/manualidades/122000000",
"https://www.casadellibro.com/libros/libros/medicina/123000000",
"https://www.casadellibro.com/libros/libros/musica/124000000",
"https://www.casadellibro.com/libros/libros/narrativa-historica/125000000",
"https://www.casadellibro.com/libros/libros/novela-contemporanea/128000000",
"https://www.casadellibro.com/libros/libros/novela-negra/126000000",
"https://www.casadellibro.com/libros/libros/oposiciones/129000000",
"https://www.casadellibro.com/libros/libros/psicologia-y-pedagogia/130000000",
"https://www.casadellibro.com/libros/libros/romantica-y-erotica/416000000",
"https://www.casadellibro.com/libros/libros/salud-y-dietas/131000000",
"https://www.casadellibro.com/libros/libros/novela-contemporanea/128000000",
"https://www.casadellibro.com/libros/libros/novela-negra/126000000",
"https://www.casadellibro.com/libros/libros/narrativa-historica/125000000",
"https://www.casadellibro.com/libros/libros/historia/115000000",
"https://www.casadellibro.com/libros/libros/autoayuda-y-espiritualidad/102000000",
"https://www.casadellibro.com/libros/libros/salud-y-dietas/131000000",
"https://www.casadellibro.com/libros/papeleria",
"https://www.casadellibro.com/libros/ebooks"

]:
            self.log("Going to:" + url)
            yield scrapy.Request(url=url, callback=self.parse_product)


    def parse_product(self, response):
        urls = (response.css('.title::attr(href)').extract())

        for url in urls:
            url = "https://www.casadellibro.com/vender-libro"+url
            self.log("Going to product " + url)
            yield scrapy.Request(url=url, callback=self.parse_merchants)


    def parse_merchants(self, response):
        sellers = response.css(".text-subtitle-2").extract()

        for i in sellers:
            i= str(i[35:-13])
            self.log("merchant " + i)

            yield {
                'seller_name': i
            }
