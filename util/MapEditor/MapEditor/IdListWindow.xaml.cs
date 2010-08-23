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
	/// Interaction logic for IdListWindow.xaml
	/// </summary>
	public partial class IdListWindow : Window
	{
		public IdListWindow()
		{
			InitializeComponent();
			this.edit_button.Click += new RoutedEventHandler(edit_button_Click);
			this.RefreshListing();
		}

		void edit_button_Click(object sender, RoutedEventArgs e)
		{
			int index = this.ids.SelectedIndex;
			if (index >= 0)
			{
				ID idToEdit = Model.Instance.ActiveMap.Ids[index];
				ScriptEditWindow editor = new ScriptEditWindow(idToEdit.Script ?? "");
				editor.ShowDialog();
				idToEdit.Script = string.IsNullOrEmpty(editor.FinalScript) ? null : editor.FinalScript;
			}
		}

		private void RefreshListing()
		{
			this.ids.Items.Clear();
			foreach (ID id in Model.Instance.ActiveMap.Ids)
			{
				this.ids.Items.Add(id.Name + " (" + id.Layer + "," + id.X.ToString() + "," + id.Y.ToString() + ")" + (id.Script == null ? "" : " [HAS SCRIPT]"));
			}
		}
	}
}
