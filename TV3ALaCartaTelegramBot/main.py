from TelegramHelper.Bot import Bot

from TV3ALaCarta import TV3ALaCarta
from Element import Element
from os.path import exists
import time
import os
import sys

def Main():
    fileConfig="Config";

    if exists(fileConfig):
        fConfig = open(fileConfig, "r");
        config = fConfig.readlines();
        fConfig.close();
        token=config[0];
    elif len(sys.argv)>1:
        token=sys.argv[1];
        fConfig = open(fileConfig, 'w');
        fConfig.writelines([token]);
        fConfig.close();

    bot=Bot(token,"TV3 A La Carta V2.0");
    bot.Default.AddContains('ccma.cat',SendInfo);
    bot.Default.AddContains("http",lambda cli:cli.SendText("Només links donats per la cerca de TV3 a La Carta!"));
    bot.Default.Default=Cerca;
    bot.AddCommand("Start", lambda cli,args:cli.SendText("1-Text a cercar\n2-URL a obtenir informació"));
    bot.ReplyTractament=ReplyTractament;
    bot.Start();

def ReplyTractament(cli):
    if cli.IsAReplyFromBot:
        cli.Args=cli.Reply.split("\n");
        if len(cli.Args)>0 and cli.Args[0].startswith("/"):
            cli.Command=str(cli.Args[0][1:]);
            cli.Args=cli.Args[1:];

def Cerca(cli):

    if len(cli.Args)>2 and "pagina"== cli.Args[-2].lower():
        pagina=int(cli.Args[-1]);
        text=" ".join(cli.Args[:-2]);
    else:
        pagina=1;
        text=" ".join(cli.Args);
    total=0;        
    for video in TV3ALaCarta.Cerca(TV3ALaCarta.GetCercaUrl(text,pagina)):
        total+=1;
        cli.SendPhoto(video.Img,video.ToMessage());
    if total>0:
        siguientePagina=pagina+1;    
        cli.SendText(text+" Pagina "+str(siguientePagina));
    else:
        cli.SendText("No s'ha trobat res!");

def SendInfo(cli):
    text=" ".join(cli.Args);
    if "\n" in text:
        url=text.split("\n")[-1];
    elif text.startswith("http"):
        if " " in text:
            url=text.split(" ")[0];
        else:
            url=text;
    elif cli.Args[-1].startswith("http"):
        url=cli.Args[-1];

    result=Element.GetInfo(url);
    cli.SendPhoto(result.Img,result.Desc);

Main();
