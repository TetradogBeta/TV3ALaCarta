using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Gabriel.Cat.S.Extension;
using HtmlAgilityPack;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace TV3ALaCarta.Core
{
    public static class TV3ALaCarta
    {
        public enum DataPublicacio
        {
            Sempre,UltimMes,UltimaSetmana,UltimAny
        }
        public const string URL = "https://www.ccma.cat";
        public const string URLCERCADOR = URL + "/tv3/alacarta/cercador/";

        public static async Task<IEnumerable<Video>> Cerca(string text,DataPublicacio data=DataPublicacio.Sempre)
        {
            string url = $"{URLCERCADOR}?text={text.Replace(" ", "%20")}&profile=videos";

            if (data != DataPublicacio.Sempre)
            {
                url = $"{url}&data_publicacio={data.ToString().ToUpper()}";
            }
            url = $"{url}&perfil=rellevancia";

            return  new HtmlDocument().LoadUrl(url).GetByClass("F-llistat-item").Select(item=>new Video(item));
        }
    }
    public class Video
    {
        public const string URLDOWNLOADER = "https://videostv3.vercel.app/video/";
        public const string URLINFO = "http://dinamics.ccma.cat/pvideo/media.jsp?media=video&version=0s&idint=";
        /*
         <li class="F-llistat-item"><a class="F-capsaImatge" href="/tv3/super3/les-sisters/operacio-polls/video/6064767/"><img 
								loading="lazy"
								class="media-object"
								alt="Operació polls"
								src="https://img.ccma.cat/multimedia/jpg/9/9/1603071873099.jpg"
								srcset="
									https://img.ccma.cat/multimedia/jpg/9/9/1603071873099_480x270.jpg 480w,
									https://img.ccma.cat/multimedia/jpg/9/9/1603071873099_375x210.jpg 375w,
									https://img.ccma.cat/multimedia/jpg/9/9/1603071873099_270x152.jpg 270w,
									https://img.ccma.cat/multimedia/jpg/9/9/1603071873099_240x135.jpg 240w,
									https://img.ccma.cat/multimedia/jpg/9/9/1603071873099_233x131.jpg 233w,
									https://img.ccma.cat/multimedia/jpg/9/9/1603071873099_184x103.jpg 184w,
									https://img.ccma.cat/multimedia/jpg/9/9/1603071873099_135x76.jpg 135w
									
								"
								sizes="
									(max-width: 468px) 135px,
									(max-width: 768px) 33vw,
									240px
								"
							><time class="duration" datetime="PT00H11M59S"><span class="hide-text">:</span>
                            	00:11:59
                            </time><div class="ico"><div class="ico-play_3ac C-resetBoto">
        <span class="hide-text">Veure vídeo</span></div></div></a><div class="F-info">
        <div class="info"><span class="">Les sisters </span></div><h3 class="titol">
        <a href="/tv3/super3/les-sisters/operacio-polls/video/6064767/">Operació polls</a></h3>
        <time class="data" datetime="2021-08-19">19/08/2021</time><p class="entradeta">
        <span class="entraCurt">Epidèmia de polls a Pom-les-Bains! La Marine aprofita l'ocasió per no haver d'anar a la piscina i s'inventa que ha agafat polls. El mateix dia s'organ</span><button class="botoMes" type="button">Més</button><span class="entraLlarg">itza una cursa al parc i el corconet no se la vol perdre. Però com hi pot anar si ha fet creure a tothom que té polls? La solució: disfressar-se de noi.</span></p></div><p class="entradetaMobil">
							Epidèmia de polls a Pom-les-Bains! La Marine aprofita l'ocasió per no haver d'anar a la piscina i s'inventa que ha agafat polls. El mateix dia s'organitza una cursa al parc i el corconet no se la vol perdre. Però com hi pot anar si ha fet creure a tothom que té polls? La solució: disfressar-se de noi.
						</p><button class="botoMesMobil" type="button">Més</button></li><li class="F-llistat-item C-noImg"><div class="F-info"><div class="info"><span class="">Espies de veritat </span></div><h3 class="titol"><a href="/tv3/super3/espies-veritat/espies-de-veritat-cap-123-que-continui-lespectacle-perque-si-no-/video/3242930/">Que continuï l'espectacle, perquè si no...</a></h3><time class="data" datetime="2021-08-19">19/08/2021</time><p class="entradeta"><span class="entraCurt">Després d'una actuació penosa de la Clover en una classe de teatre, l'estrany comportament d'en Virgil cridarà l'atenció de les Espies. A més d'anar v</span><button class="botoMes" type="button">Més</button><span class="entraLlarg">estit de cowboy, parla amb un accent desconegut! I no és pas l'únic! La Mandy es presentarà a classe vestida d'astronauta, i la Mindy, de minyona! A més, sembla que estiguin hipnotitzats! Tot un misteri!</span></p></div><p class="entradetaMobil">
							Després d'una actuació penosa de la Clover en una classe de teatre, l'estrany comportament d'en Virgil cridarà l'atenció de les Espies. A més d'anar vestit de cowboy, parla amb un accent desconegut! I no és pas l'únic! La Mandy es presentarà a classe vestida d'astronauta, i la Mindy, de minyona! A més, sembla que estiguin hipnotitzats! Tot un misteri!
						</p><button class="botoMesMobil" type="button">Més</button></li>
         
         */

        public Video() {
            UriRel = string.Empty;
            Img = string.Empty;
            Serie = string.Empty;
            Descripcio = string.Empty;
            Titol = string.Empty;
            Data = default;
            Duracio = default;
        }
        public Video(HtmlNode nodeVideo)
        {
            HtmlNode nodeDesc = nodeVideo.GetByClass("entraLlarg").FirstOrDefault();
            if (ReferenceEquals(nodeDesc, default))
            {
                nodeDesc = nodeVideo.GetByClass("entradeta").FirstOrDefault();
                if (ReferenceEquals(nodeDesc, default))
                {
                    nodeDesc = nodeVideo.GetByClass("entramobil").FirstOrDefault();
                }
                }
            UriRel = nodeVideo.GetByTagName("a").First().Attributes["href"].Value;
            Img = nodeVideo.GetByTagName("img").First().Attributes["src"].Value;
            Titol = nodeVideo.GetByTagName("h3").First().FirstChild.InnerText;
            if (!ReferenceEquals(nodeDesc, default))
            {
                Descripcio = nodeDesc.FirstChild.InnerText;
            }
            Serie = nodeVideo.GetByClass("info").First().InnerText;
            Data = DateTime.Parse(nodeVideo.GetByClass("data").First().Attributes["datetime"].Value);
            Duracio = TimeSpan.Parse(nodeVideo.GetByClass("duration").First().InnerText.Substring(1));

        }
        public string UriDownloader => URLDOWNLOADER + Id;
        public string UriInfo => URLINFO + Id.Substring(0,Id.Length-1);
        public string Id => UriRel.Substring(UriRel.Substring(0,UriRel.Length-1).LastIndexOf('/')+1);
        public string Uri => TV3ALaCarta.URL+ UriRel;
        public string UriRel { get; set; }
        public string Img { get; set; }
        public string Serie { get; set; }
        public string Descripcio { get; set; }
        public string Titol { get; set; }
        public DateTime Data { get; set; }
        public TimeSpan Duracio { get; set; }
        bool Loaded { get; set; } = false;
        public SortedList<string,string> Videos { get; set; }
        public SortedList<string,string> VideosAmbDescripcio { get; set; }
        public string UriSubtitulsCatala { get; set; }
        public void EndLoad()
        {
            JObject data;
            JToken media;
            JToken variants;
            JToken subtituls;

            if (!Loaded)
            {
                data = JObject.Parse(new Uri(UriInfo).DownloadString());
                Videos = new SortedList<string, string>();
                VideosAmbDescripcio = new SortedList<string, string>();
                media = data["media"];
                if (!ReferenceEquals(media, default))
                {
                    foreach (JToken video in media["url"])
                    {
                        Videos.Add(video["label"].ToString(), video["file"].ToString());
                    }
                }
                variants = data["variants"];
                if (!ReferenceEquals(variants, default))
                {
                    foreach (JToken video in variants["media"]["url"])
                    {
                        VideosAmbDescripcio.Add(video["label"].ToString(), video["file"].ToString());
                    }
                }
                subtituls = data["subtitols"];
                if (!ReferenceEquals(subtituls, default))
                {
                    UriSubtitulsCatala = subtituls["url"].ToString();
                }

                Loaded = true;
            }
        }
    
    }
}
