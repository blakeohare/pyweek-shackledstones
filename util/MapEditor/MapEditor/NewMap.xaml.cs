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
using System.Windows.Shapes;

namespace MapEditor
{
	/// <summary>
	/// Interaction logic for NewMap.xaml
	/// </summary>
	public partial class NewMap : Window
	{
		public NewMap()
		{
			InitializeComponent();
			this.accept.Click += new RoutedEventHandler(accept_Click);
		}

		void accept_Click(object sender, RoutedEventArgs e)
		{
			this.Close();

			int width;
			int height;
			string name;

			try
			{
				width = int.Parse(this.tile_width.Text);
				height = int.Parse(this.tile_height.Text);
				name = this.map_id.Text;

			}
			catch (Exception ex)
			{
				System.Windows.MessageBox.Show(ex.Message);
				return;
			}

			if (System.IO.File.Exists(Model.Root + "\\maps\\" + name + ".txt"))
			{
				System.Windows.MessageBox.Show("There is already a map by this name");
			}
			else
			{
				Model.Instance.NewMap(name, width, height);
				MainWindow.Instance.PopulateArtboard();
			}
		}
	}
}
