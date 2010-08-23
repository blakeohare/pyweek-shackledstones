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
	/// Interaction logic for NewKeyWindow.xaml
	/// </summary>
	public partial class NewKeyWindow : Window
	{
		public NewKeyWindow()
		{
			InitializeComponent();
			this.ok_button.Click += new RoutedEventHandler(ok_button_Click);
			this.FinalName = null;
		}

		public string FinalName { get; set; }

		void ok_button_Click(object sender, RoutedEventArgs e)
		{
			this.DialogResult = true;
			this.Close();
			this.FinalName = this.key_name.Text.Trim();
		}
	}
}
