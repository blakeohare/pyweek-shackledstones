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
	/// Interaction logic for ScriptEditWindow.xaml
	/// </summary>
	public partial class ScriptEditWindow : Window
	{
		private string orig;
		private string final;

		public ScriptEditWindow(string script_original_contents)
		{
			InitializeComponent();
			this.orig = script_original_contents;
			this.final = script_original_contents;
			this.script_content.Text = this.orig;
			this.ok_button.Click += new RoutedEventHandler(ok_button_Click);
		}

		void ok_button_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
			this.final = this.script_content.Text.Trim();
		}

		public string FinalScript { get { return this.final; } }
	}
}
