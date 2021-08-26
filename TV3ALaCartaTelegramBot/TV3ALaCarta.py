from bs4 import BeautifulSoup
import cloudscraper
import re
import Element


class TV3ALaCarta:
    URL = "https://www.ccma.cat";
    URLCERCADOR = URL + "/tv3/alacarta/cercador/";
    @staticmethod
    def GetCercaUrlSinPagina(text):
        text=text.replace(" ","%20");#escapar todo
        return TV3ALaCarta.URLCERCADOR+"text="+text+"&profile=videos&pagina=";
    def GetCercaUrl(text,pagina=1):
        return TV3ALaCarta.GetCercaUrlSinPagina(text)+str(pagina);
    @staticmethod
    def Carca(urlCerca):
        scraper = cloudscraper.create_scraper();
        page = scraper.get(str(urlCerca)).text;
        soup=BeautifulSoup(str(page),"html.parser");
        lstElements=soup.find("F-llistat-item");
        for video in lstElements:
            yield Element(video);
