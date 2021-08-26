from bs4 import BeautifulSoup
import json
import cloudscraper

class Element:
    def __init__(self,nodeStr):
        node=BeautifulSoup(str(nodeStr),"html.parser");
        desc=node.find("entraLlarg");
        if desc is None:
           desc=node.find("entradeta");
           if desc is None:
               desc=node.find("entramobil");


        if desc is not None:
            self.Descripcio=desc[0];

        self.UriRel=node.find("a")[0]["href"]; 
        self.Img=node.find("img")[0]["src"];
        self.Titol=node.find("h3")[0];
        self.Info=node.find("info")[0]; 
        self.Data=node.find("data")[0]["datetime"];
        self.Duracio=node.find("duration")[0];
        self.Id=self.UriRel.split('/')[-2];
        self.UrlJSon="http://dinamics.ccma.cat/pvideo/media.jsp?media=video&version=0s&idint="+self.Id;
    def ToMessage(self):
        message="";


        return message;
    @staticmethod
    def GetInfo(urlJson):
        scraper = cloudscraper.create_scraper();
        data = scraper.get(urlJson).text;
        info=json.loads(data);
        message="";
        if info["media"] is not None:
            message="Links:";
            for video in info["media"]["url"]:
                message+="/n";
                message+=str(video["label"]);
                message+=":";
                message+=str(vide["file"]);
        if info["variants"] is not None:
            if message is not "":
                message+="/n";
            message+="Audio Descripció Links:";
            for video in info["variants"]["media"]["url"]:
                message+="/n";
                message+=str(video["label"]);
                message+=":";
                message+=str(vide["file"]);

        if info["subtitols"] is not None:
            if message is not "":
                message+="/n";
                message+="Subtitols:"+str(info["subtitols"]["url"]);

        return message;        