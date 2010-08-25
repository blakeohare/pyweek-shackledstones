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
	/// Interaction logic for EditKeyWindow.xaml
	/// </summary>
	public partial class EditKeyWindow : Window
	{
		public EditKeyWindow(string initialValue)
		{
			InitializeComponent();
			this.key_value.Text = initialValue.Replace("\\n", "\r\n").Replace("\\\\", "\\");
			this.done.Click += new RoutedEventHandler(done_Click);
			this.FinalValue = initialValue;
		}

		public string FinalValue { get; set; }

		void done_Click(object sender, RoutedEventArgs e)
		{
			this.DialogResult = true;
			this.FinalValue = this.key_value.Text.Replace("\\", "\\\\").Replace("\r", "").Replace("\n", "\\n");
			this.Close();
		}
	}
}
