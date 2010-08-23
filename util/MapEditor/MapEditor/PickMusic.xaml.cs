using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.IO;
namespace MapEditor
{
    /// <summary>
    /// Interaction logic for PickMusic.xaml
    /// </summary>
    public partial class PickMusic : Window
    {
        public string SelectedMusic
        {
            get { return selectedmusic; }
        }
        private string selectedmusic = "";
        public PickMusic(string currentmusic)
        {
            InitializeComponent();
            selectedmusic = currentmusic;
            string folder=Model.Root + @"\media\music";
            MusicChoice.Items.Add("");
            if (Directory.Exists(folder))
            {
                string[] filenames = Directory.GetFiles(folder,"*.mp3");
                foreach (string longname in filenames)
                {
                    string filename = getShortenedName(longname);
                    MusicChoice.Items.Add(filename);
                    if (filename == currentmusic)
                    {
                        MusicChoice.SelectedIndex = MusicChoice.Items.Count - 1;
                    }
                }
            }
            Change.Click += new RoutedEventHandler(Change_Click);

        }
        private string getShortenedName(string filename)
        {
            char[] splitchars = new char[] { '\\' };
            string[] parts = filename.Split(splitchars);
            string namepart = parts[parts.Length - 1];
            return namepart;
        }


        void Change_Click(object sender, RoutedEventArgs e)
        {
            selectedmusic = MusicChoice.SelectedItem as string;
            this.Close();
        }
    }
}
