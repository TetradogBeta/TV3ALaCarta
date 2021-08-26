from bs4 import BeautifulSoup
import cloudscraper
import re
import Element
import urllib.parse

class TV3ALaCarta:
    URL = "https://www.ccma.cat";
    URLCERCADOR = URL + "/tv3/alacarta/cercador/";
    @staticmethod
    def GetCercaUrlSinPagina(text):
        text=urllib.parse.quote(text);
        return TV3ALaCarta.URLCERCADOR+"text="+text+"&profile=videos&pagina=";
    def GetCercaUrl(text,pagina=1):
        return TV3ALaCarta.GetCercaUrlSinPagina(text)+str(pagina);
    @staticmethod
    def Carca(urlCerca):
        scraper = cloudscraper.create_scraper();
        page = scraper.get(str(urlCerca)).text;
        soup=BeautifulSoup(str(page),"html.parser");
        lstElements=soup.select(".F-llistat-item");
        for video in lstElements:
            yield Element(video);
