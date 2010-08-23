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
	/// Interaction logic for AddId.xaml
	/// </summary>
	public partial class AddId : Window
	{
		private int x;
		private int y;
		private string layer;

		public AddId(int x, int y, string layer)
		{
			this.x = x;
			this.y = y;
			this.layer = layer;
			InitializeComponent();
			this.ok.Click += new RoutedEventHandler(ok_Click);
			this.cancel.Click += new RoutedEventHandler(cancel_Click);
		}

		void cancel_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void ok_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
			Model.Instance.ActiveMap.AddId(layer, x, y, this.id_name.Text);
		}
	}
}
