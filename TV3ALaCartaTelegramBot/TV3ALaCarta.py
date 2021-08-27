from bs4 import BeautifulSoup
from Element import Element
import cloudscraper
import re
import urllib.parse

class TV3ALaCarta:
    URL = "https://www.ccma.cat";
    URLCERCADOR = URL + "/tv3/alacarta/cercador/";
    @staticmethod
    def GetCercaUrlSinPagina(text):
        text=urllib.parse.quote(str(text));
        return TV3ALaCarta.URLCERCADOR+"?text="+text+"&profile=videos";
    @staticmethod
    def GetCercaUrl(text,pagina=1):
        return TV3ALaCarta.GetCercaUrlSinPagina(text)+"&pagina="+str(pagina);
    @staticmethod
    def Cerca(urlCerca):
        scraper = cloudscraper.create_scraper();
        page = scraper.get(str(urlCerca)).text;
        soup=BeautifulSoup(str(page),"html.parser");
        lstElements=soup.find_all("ul","R-resultats");
        for video in lstElements[0]:
            yield Element(video);
