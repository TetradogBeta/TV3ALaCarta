from TV3ALaCarta import TV3ALaCarta
from Element import Element
import telepot



class TelegramBot:
    Bot=None;
    def __init__(self,msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.IdChat=chat_id;

    def CercaPagina(self,text,pagina):
        for video in TV3ALaCarta.Cerca(TV3ALaCarta.GetCercaUrl(text,pagina)):
            self.EnviaImg(video.Img,video.ToMessage());
        siguientePagina=int(pagina)+1;    
        self.EnviaLinkPagina(siguientePagina,text);


    def EnviaLinkPagina(self,pagina,text):
        TelegramBot.Bot.sendMessage(self.IdChat,"Para 'la pagina "+str(pagina)+"' reenvia el siguiente mensaje");
        TelegramBot.Bot.sendMessage(self.IdChat,text+" Pagina "+str(pagina));
    def EnviaImg(self,urlImg,desc):
        if urlImg is not None:
            TelegramBot.Bot.sendPhoto(self.IdChat,urlImg,desc);
        else:
            self.EnviaText(desc);
    def EnviaText(self,text):
        TelegramBot.Bot.sendMessage(self.IdChat,text);

    @staticmethod
    def Start(token):
        TelegramBot.Bot=telepot.Bot(token);
        TelegramBot.Bot.message_loop(TelegramBot._DoIt);
    
    @staticmethod
    def _DoIt(message):
        chat=TelegramBot(message);
        url=None;
        if "caption" in message:
            if "http" in message["caption"]:
                camposUrl=message["caption"].split("\n");
                url=camposUrl[-1];
            else:
                message=message["caption"];
        elif "reply_to_message" in message:
            if "http" in message["reply_to_message"]["caption"]:
                if "\n" in message["reply_to_message"]["caption"]:
                    camposUrl=message["reply_to_message"]["caption"].split("\n");
                    url=camposUrl[-1];
                else:
                    url=message["reply_to_message"]["caption"]; 
            else:
                message=message["reply_to_message"]["caption"];        
        elif "http" in message["text"]:
            url=message["text"];
        else:
            message=message["text"];


        if url is not None:
            result=Element.GetInfo(url);
            chat.EnviaImg(result.Img,result.Desc);
        elif "pagina " in message.lower():
            textParts=message.lower().split("pagina ");
            chat.CercaPagina(textParts[0],textParts[1]);
        else:
            chat.CercaPagina(message,1);






