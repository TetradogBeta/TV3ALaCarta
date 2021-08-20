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
namespace _3ALaCartaViewer
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            txtCercador.Focus();
        }

        private void txtCercador_TextChanged(object sender, TextChangedEventArgs e)
        {
            const string ENTER = "\r\n";
            Task<IEnumerable<Video>> tVideos;
             if (txtCercador.Text.Contains(ENTER))
            {
                tVideos = TV3ALaCarta.Core.TV3ALaCarta.Cerca(txtCercador.Text.Replace(ENTER,""));
                tVideos.Wait();
                ugVideos.Children.Clear();
                foreach (Video video in tVideos.Result)
                {
                    ugVideos.Children.Add(new VideoViewer(video));
                }
            }
        }
    }
}
