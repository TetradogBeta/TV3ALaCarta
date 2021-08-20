using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using TV3ALaCarta.Core;
using Gabriel.Cat.S.Extension;
using System.Drawing;

namespace _3ALaCartaViewer
{
    /// <summary>
    /// Lógica de interacción para VideoViewer.xaml
    /// </summary>
    public partial class VideoViewer : UserControl
    {
        static Notifications.Wpf.Core.NotificationManager Manager = new Notifications.Wpf.Core.NotificationManager();
        public VideoViewer()
        {
            InitializeComponent();
      
        }
        public VideoViewer(Video video) : this()
        {
            Video = video;
            imgVideo.ToolTip = Video.Descripcio;
            tbTitle.Text =$"{Video.Serie}-{Video.Titol}";
            
            LoadImg();
        }
        public Video Video { get; set; }
        public bool? Downloading { get; set; }
        async Task LoadImg()
        {
            if (!ReferenceEquals(Video, default))
                imgVideo.SetImage( new Uri(Video.Img).DownloadBitmap());
        }
        private void imgVideo_PreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            if (!ReferenceEquals(Video, default))
            {
                new Uri(Video.UriDownloader).Abrir();
            }
        }
        private void imgVideo_PreviewMouseRightButtonUp(object sender, MouseButtonEventArgs e)
        {
           
            Task tDownloading;
            KeyValuePair<string, string> pQualityAndUrl=default;
            string fileName=default;
            string urlData=default;
            if (!ReferenceEquals(Video, default) && !Downloading.HasValue)
            {
                
                tDownloading = new Task(new Action(() => {
                    Downloading = true;
                    Video.EndLoad();
                    if (Video.Videos.ContainsKey("720p"))
                    {
                        fileName = $"{Video.Serie}-{Video.Titol} 720p.mp4";
                        urlData = Video.Videos["720p"];

                    }
                    else if (Video.Videos.ContainsKey("480p"))
                    {
                        fileName = $"{Video.Serie}-{Video.Titol} 480p.mp4";
                        urlData = Video.Videos["480p"];
                    }
                  
                    else if (Video.Videos.Count != 0)
                    {
                        pQualityAndUrl = Video.Videos.First();
                        fileName = $"{Video.Serie}-{Video.Titol} {pQualityAndUrl.Key}.mp4";
                        urlData = pQualityAndUrl.Value;
                        

                    }
                    if (Video.Videos.Count == 0)
                    {
                        Manager.ShowAsync($"No hay links para {Video.Titol}!");
                    }
                    else
                    {
                        fileName=fileName.NormalitzeFileName(string.Empty);
                        Manager.ShowAsync($"Descargando {fileName}");
                        System.IO.File.WriteAllBytes(fileName, new Uri(urlData).DownloadData());
                        Manager.ShowAsync($"Descargado {fileName}");
                    }

                        Downloading = false;

                }));
                
            

                tDownloading.Start();

            }
        }
    }
}
