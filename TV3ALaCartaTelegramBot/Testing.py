from TV3ALaCarta import TV3ALaCarta
from Element import Element

for video in TV3ALaCarta.Cerca(TV3ALaCarta.GetCercaUrl("si no",2)):
    print(Element.GetInfo(video.UrlJSon).Desc);