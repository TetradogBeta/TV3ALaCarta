from bs4 import BeautifulSoup
import json
import cloudscraper

class Element:
    MAXCAPTION=720;
    def __init__(self,nodeStr):
        node=BeautifulSoup(str(nodeStr),"html.parser");
        desc=node.select_one(".entraLlarg");
        if desc is None:
           desc=node.select_one(".entradeta");
           if desc is None:
               desc=node.select_one(".entramobil");


        if desc is not None:
            self.Descripcio=desc.text;
            if len(self.Descripcio)> Element.MAXCAPTION:
                self.Descripcio=self.Descripcio[0:Element.MAXCAPTION]+"...";
        else:
            self.Descripcio="";    

        self.UriRel=node.find_all("a")[0]["href"]; 
        self.Img=node.find_all("img");
        if len(self.Img)>0:
           self.Img=self.Img[0]["src"];
        else:
            self.Img=None;

        self.Titol=node.find_all("h3")[0].text;
        self.Info=node.select_one(".info"); 
        self.Data=node.select_one(".data")["datetime"];
        self.Duracio=node.select_one(".duration");
        if self.Duracio is not None:
            self.Duracio=self.Duracio.text[1:];
            self.Duracio=self.Duracio.replace("\n","");
            self.Duracio=self.Duracio.replace("\t","");
            self.Duracio=self.Duracio.replace(" ","");
  
        
        self.Id=self.UriRel.split('/')[-2];
        self.UrlJSon="http://dinamics.ccma.cat/pvideo/media.jsp?media=video&version=0s&idint="+self.Id;
    
    def ToMessage(self):
        message=self.Titol+"\n";
        message+="Data "+self.Data+"\n";
        if self.Duracio is not None:
            message+="Duració "+self.Duracio+"\n";
        message+=self.Descripcio+"\n";
        message+=self.UrlJSon;
        return message;
    @staticmethod
    def GetInfo(urlJson):
        scraper = cloudscraper.create_scraper();
        data = scraper.get(urlJson).text;
        info=json.loads(data);
        message=info["informacio"]["titol_complet"]+":\n";
        if "media" in info:
            message+="Links:";
            for video in info["media"]["url"]:
                message+="\n";
                message+=str(video["label"]);
                message+=":";
                message+=str(video["file"]);
        if "variants" in info:
            if  message :
                message+="\n";
            message+="Audio Descripció Links:";
            for video in info["variants"]["media"]["url"]:
                message+="\n";
                message+=str(video["label"]);
                message+=":";
                message+=str(video["file"]);

        if "subtitols" in info:
            if  message:
                message+="\n";

            if "text" in info["subtitols"]:
                message+="Subtitol:";
                message+="\n"+info["subtitols"]["text"]+": ";
                message+=info["subtitols"]["url"];
            else:
                message+="Subtitols:";    
                for subtitol in info["subtitols"]:
                    message+="\n"+subtitol["text"]+": ";
                    message+=subtitol["url"];
        obj = lambda: None;
        obj.Img=info["imatges"]["url"];
        obj.Desc=message;
        return  obj;        