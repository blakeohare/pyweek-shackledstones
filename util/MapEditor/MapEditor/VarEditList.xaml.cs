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
	/// Interaction logic for VarEditList.xaml
	/// </summary>
	public partial class VarEditList : Window
	{
		public VarEditList()
		{
			InitializeComponent();
			this.edit_button.Click += new RoutedEventHandler(edit_button_Click);
			this.new_var.Click += new RoutedEventHandler(new_var_Click);
			this.RefreshListing();
		}

		void new_var_Click(object sender, RoutedEventArgs e)
		{
			NewKeyWindow nkw = new NewKeyWindow();
			if (nkw.ShowDialog() ?? false)
			{
				string name = nkw.FinalName.Trim();
				if (!string.IsNullOrEmpty(name))
				{
					if (Model.Instance.ActiveMap.Values.ContainsKey(name))
					{
						System.Windows.MessageBox.Show("The map already contains a definition for " + name);
					}
					else
					{
						Model.Instance.ActiveMap.Values.Add(name, "");
						this.RefreshListing();
					}
				}
			}
		}

		void edit_button_Click(object sender, RoutedEventArgs e)
		{
			int index = this.ids.SelectedIndex;
			if (index >= 0)
			{
				int i = 0;
				foreach (string key in Model.Instance.ActiveMap.Values.Keys)
				{
					if (i == index)
					{
						EditKeyWindow ekw = new EditKeyWindow(Model.Instance.ActiveMap.Values[key]);
						if (ekw.ShowDialog() ?? false)
						{
							Model.Instance.ActiveMap.Values[key] = ekw.FinalValue;
							this.RefreshListing();
						}
						break;
					}

					++i;
				}
			}
		}

		private void RefreshListing()
		{
			this.ids.Items.Clear();
			foreach (string key in Model.Instance.ActiveMap.Values.Keys)
			{
				string value = Model.Instance.ActiveMap.Values[key];
				if (value.Length > 30) {
					value = value.Substring(0, 30) + "...";
				}
				this.ids.Items.Add(key + " - " + value);
			}
		}
	}
}
