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

namespace MapEditor
{
	public enum Tool
	{
		Tile,
		EraserDetail,
		EraserDeep,
		EraserLayer,
		Rectangle,
		IdMarker,
		None
	}
	/// <summary>
	/// Interaction logic for MainWindow.xaml
	/// </summary>
	public partial class MainWindow : Window
	{
		private static MainWindow me;
		public static MainWindow Instance { get { return me; } }
		private int tileWidth;
		private int tileHeight;

		public MainWindow()
		{
			try
			{
				this.ActiveTool = Tool.None;
				me = this;
				InitializeComponent();
				this.file_new.Click += new RoutedEventHandler(file_new_Click);
				this.file_open.Click += new RoutedEventHandler(file_open_Click);
				this.file_save.Click += new RoutedEventHandler(file_save_Click);
				this.file_exit.Click += new RoutedEventHandler(file_exit_Click);

				this.map_scripts.Click += new RoutedEventHandler(map_scripts_Click);
                this.map_music.Click += new RoutedEventHandler(map_music_Click);

				this.mouse_catcher.MouseDown += new MouseButtonEventHandler(mouse_catcher_MouseDown);
				this.mouse_catcher.MouseUp += new MouseButtonEventHandler(mouse_catcher_MouseUp);
				this.mouse_catcher.MouseMove += new MouseEventHandler(mouse_catcher_MouseMove);

				this.tool_selector.SelectionChanged += new SelectionChangedEventHandler(tool_selector_SelectionChanged);
				this.active_primary_layer.Items.Add("A");
				this.active_primary_layer.Items.Add("B");
				this.active_primary_layer.Items.Add("C");
				this.active_primary_layer.Items.Add("D");
				this.active_primary_layer.Items.Add("E");
				this.active_primary_layer.Items.Add("F");
				this.active_primary_layer.Items.Add("Stairs");
				this.active_primary_layer.SelectionChanged += new SelectionChangedEventHandler(active_primary_layer_SelectionChanged);
				this.active_primary_layer.SelectedIndex = 0;

				this.active_detail_layer.Items.Add("Base");
				this.active_detail_layer.Items.Add("BaseAdorn");
				this.active_detail_layer.Items.Add("BaseDetail");
				this.active_detail_layer.Items.Add("Doodad");
				this.active_detail_layer.Items.Add("DoodadAdorn");
				this.active_detail_layer.Items.Add("Excessive");
				this.active_detail_layer.SelectionChanged += new SelectionChangedEventHandler(active_detail_layer_SelectionChanged);
				this.active_detail_layer.SelectedIndex = 0;

				// layer visibility
				this.layer_a.Checked += new RoutedEventHandler(layer_a_Checked);
				this.layer_b.Checked += new RoutedEventHandler(layer_b_Checked);
				this.layer_c.Checked += new RoutedEventHandler(layer_c_Checked);
				this.layer_d.Checked += new RoutedEventHandler(layer_d_Checked);
				this.layer_e.Checked += new RoutedEventHandler(layer_e_Checked);
				this.layer_f.Checked += new RoutedEventHandler(layer_f_Checked);
				this.layer_stairs.Checked += new RoutedEventHandler(layer_stairs_Checked);
				this.layer_a.Unchecked += new RoutedEventHandler(layer_a_Checked);
				this.layer_b.Unchecked += new RoutedEventHandler(layer_b_Checked);
				this.layer_c.Unchecked += new RoutedEventHandler(layer_c_Checked);
				this.layer_d.Unchecked += new RoutedEventHandler(layer_d_Checked);
				this.layer_e.Unchecked += new RoutedEventHandler(layer_e_Checked);
				this.layer_f.Unchecked += new RoutedEventHandler(layer_f_Checked);
				this.layer_stairs.Unchecked += new RoutedEventHandler(layer_stairs_Checked);

				// detail visibility
				this.detail_base.Checked += new RoutedEventHandler(detail_base_Checked);
				this.detail_baseadorn.Checked += new RoutedEventHandler(detail_baseadorn_Checked);
				this.detail_baseextra.Checked += new RoutedEventHandler(detail_baseextra_Checked);
				this.doodad.Checked += new RoutedEventHandler(doodad_Checked);
				this.doodadadorn.Checked += new RoutedEventHandler(doodadadorn_Checked);
				this.excessive.Checked += new RoutedEventHandler(excessive_Checked);
				this.detail_base.Unchecked += new RoutedEventHandler(detail_base_Checked);
				this.detail_baseadorn.Unchecked += new RoutedEventHandler(detail_baseadorn_Checked);
				this.detail_baseextra.Unchecked += new RoutedEventHandler(detail_baseextra_Checked);
				this.doodad.Unchecked += new RoutedEventHandler(doodad_Checked);
				this.doodadadorn.Unchecked += new RoutedEventHandler(doodadadorn_Checked);
				this.excessive.Unchecked += new RoutedEventHandler(excessive_Checked);

				this.layer_all_off.Click += new RoutedEventHandler(layer_all_off_Click);
				this.layer_all_on.Click += new RoutedEventHandler(layer_all_on_Click);

				this.detail_all_off.Click += new RoutedEventHandler(detail_all_off_Click);
				this.detail_all_on.Click += new RoutedEventHandler(detail_all_on_Click);

				this.tool_selector.SelectedIndex = 0;
			}
			catch (Exception e)
			{
				System.Windows.MessageBox.Show("The following error was encounter so talk to Blake:\n" + e.Message);
				throw;
			}
		}

        void map_music_Click(object sender, RoutedEventArgs e)
        {
            PickMusic music = new PickMusic("");
            music.ShowDialog();
            
        }

        void map_variables_Click(object sender, RoutedEventArgs e)
        {
            (new MapVariables()).ShowDialog();
        }

		void map_scripts_Click(object sender, RoutedEventArgs e)
		{
			(new IdListWindow()).ShowDialog();
		}

		void file_exit_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void detail_all_on_Click(object sender, RoutedEventArgs e)
		{
			if (ActiveMap == null) return;
			foreach (CheckBox cb in new CheckBox[] { this.detail_base, this.detail_baseadorn, this.detail_baseextra, this.doodad, this.doodadadorn, this.excessive })
			{
				cb.IsChecked = true;
			}
		}

		void detail_all_off_Click(object sender, RoutedEventArgs e)
		{
			if (ActiveMap == null) return;
			foreach (CheckBox cb in new CheckBox[] { this.detail_base, this.detail_baseadorn, this.detail_baseextra, this.doodad, this.doodadadorn, this.excessive })
			{
				cb.IsChecked = false;
			}
		}

		internal void layer_all_on_Click(object sender, RoutedEventArgs e)
		{
			if (ActiveMap == null) return;
			foreach (CheckBox cb in new CheckBox[] { this.layer_a, this.layer_b, this.layer_c, this.layer_d, this.layer_e, this.layer_f, this.layer_stairs })
			{
				cb.IsChecked = true;
			}
		}

		void layer_all_off_Click(object sender, RoutedEventArgs e)
		{
			if (ActiveMap == null) return;
			foreach (CheckBox cb in new CheckBox[] { this.layer_a, this.layer_b, this.layer_c, this.layer_d, this.layer_e, this.layer_f, this.layer_stairs })
			{
				cb.IsChecked = false;
			}
		}

		private void SetDetailLayerOpacity(object checkbox, string name)
		{
			if (ActiveMap == null) return;
			bool? val = ((CheckBox)checkbox).IsChecked;
			foreach (string layer in "A B C D E F Stairs".Split(' '))
			{
				Grid detail = this.GetDetailLayer(layer, name);
				detail.Opacity = (val.HasValue && val.Value) ? 1.0 : 0.15;
			}
		}

		void excessive_Checked(object sender, RoutedEventArgs e)
		{
			this.SetDetailLayerOpacity(sender, "Excessive");
		}

		void doodadadorn_Checked(object sender, RoutedEventArgs e)
		{
			this.SetDetailLayerOpacity(sender, "DoodadAdorn");
		}

		void doodad_Checked(object sender, RoutedEventArgs e)
		{
			this.SetDetailLayerOpacity(sender, "Doodad");
		}

		void detail_baseextra_Checked(object sender, RoutedEventArgs e)
		{
			this.SetDetailLayerOpacity(sender, "BaseDetail");
		}

		void detail_baseadorn_Checked(object sender, RoutedEventArgs e)
		{
			this.SetDetailLayerOpacity(sender, "BaseAdorn");
		}

		void detail_base_Checked(object sender, RoutedEventArgs e)
		{
			this.SetDetailLayerOpacity(sender, "Base");
		}

		private Map ActiveMap { get { return Model.Instance.ActiveMap; } }

		private void SetLayerOpacity(object checkbox, string name)
		{
			if (ActiveMap == null) return;
			bool? val = ((CheckBox)checkbox).IsChecked;
			this.GetLayer(name).Opacity = (val.HasValue && val.Value) ? 1.0 : 0.15;
		}

		void layer_stairs_Checked(object sender, RoutedEventArgs e)
		{
			this.SetLayerOpacity(sender, "Stairs");
		}

		void layer_f_Checked(object sender, RoutedEventArgs e)
		{
			this.SetLayerOpacity(sender, "F");
		}

		void layer_e_Checked(object sender, RoutedEventArgs e)
		{
			this.SetLayerOpacity(sender, "E");
		}

		void layer_d_Checked(object sender, RoutedEventArgs e)
		{
			this.SetLayerOpacity(sender, "D");
		}

		void layer_c_Checked(object sender, RoutedEventArgs e)
		{
			this.SetLayerOpacity(sender, "C");
		}

		void layer_b_Checked(object sender, RoutedEventArgs e)
		{
			this.SetLayerOpacity(sender, "B");
		}

		void layer_a_Checked(object sender, RoutedEventArgs e)
		{
			this.SetLayerOpacity(sender, "A");
		}

		private void file_open_Click(object sender, RoutedEventArgs e)
		{
			System.Windows.Forms.OpenFileDialog ofd = new System.Windows.Forms.OpenFileDialog();
			ofd.InitialDirectory = Model.Root + "\\maps";
			//System.Windows.MessageBox.Show(string.Join(", ", System.IO.Directory.GetFiles(Model.Root + "\\maps")));
			ofd.Multiselect = false;
			if (ofd.ShowDialog() == System.Windows.Forms.DialogResult.OK)
			{
				string mapname = System.IO.Path.GetFileNameWithoutExtension(ofd.FileName);
				Model.Instance.OpenMap(mapname);
				this.PopulateArtboard();
				this.UpdateIdHighlights();
			}
		}

		private void file_save_Click(object sender, RoutedEventArgs e)
		{
			Map map = Model.Instance.ActiveMap;
			if (map != null)
			{
				map.Save();
			}
		}

		void active_primary_layer_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			this.ActivePrimaryLayer = e.AddedItems[0].ToString();
			this.UpdateIdHighlights();
		}

		public void UpdateIdHighlights()
		{
			if (ActiveMap != null)
			{
				foreach (ID id in ActiveMap.Ids)
				{
					int x = id.X;
					int y = id.Y;
					Border b = this.GetGridCell(x, y);
					b.Background = Brushes.Transparent;
					b.Child = null;
					b.ToolTip = null;
				}

				Brush brush = new SolidColorBrush(Color.FromArgb(100, 255, 255, 0));

				foreach (ID id in ActiveMap.Ids)
				{
					if (id.Layer == this.ActivePrimaryLayer)
					{
						int x = id.X;
						int y = id.Y;
						Border b = this.GetGridCell(x, y);
						b.Background = brush;
						b.Child = new TextBlock() { Text = id.Name, FontSize = 10, Foreground = Brushes.Black };
						b.ToolTip = id.Name;
					}
				}
			}
		}

		void active_detail_layer_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			this.ActiveDetailLayer = e.AddedItems[0].ToString();
		}

		public string ActivePrimaryLayer { get; set; }
		public string ActiveDetailLayer { get; set; }

		private Tool ActiveTool { get; set; }
		bool tile_palette_shown = false;
		void tool_selector_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			ComboBox cb = sender as ComboBox;
			if (cb.SelectedItem == this.cb_erased)
			{
				this.ActiveTool = Tool.EraserDeep;
				//this.palette_host.Children.Clear();
			}
			else if (cb.SelectedItem == this.cb_erasel)
			{
				this.ActiveTool = Tool.EraserLayer;
				//this.palette_host.Children.Clear();
			}
			else if (cb.SelectedItem == this.cb_eraset)
			{
				this.ActiveTool = Tool.EraserDetail;
				//this.palette_host.Children.Clear();
			}
			else if (cb.SelectedItem == this.cb_rect)
			{
				this.ActiveTool = Tool.Rectangle;
				//this.palette_host.Children.Clear();
				this.Show_Tile_Palette();
			}
			else if (cb.SelectedItem == this.cb_tile)
			{
				this.ActiveTool = Tool.Tile;
			//	this.palette_host.Children.Clear();
				this.Show_Tile_Palette();
			}
			else if (cb.SelectedItem == this.cb_id)
			{
				this.ActiveTool = Tool.IdMarker;

			}
			else
			{
				this.ActiveTool = Tool.None;
			}
		}

		private void Show_Rectangle_Palette()
		{

		}

		private void Show_Tile_Palette()
		{
			if (this.tile_palette_shown) return;
			this.tile_palette_shown = true;
			Grid g = new Grid() { Background = Brushes.Blue };
			g.RowDefinitions.Add(new RowDefinition() { Height = new GridLength(0, GridUnitType.Auto) });
			g.RowDefinitions.Add(new RowDefinition() { Height = new GridLength(1, GridUnitType.Star) });

			ComboBox cb = new ComboBox();
			foreach (string category in TileStore.Categories)
			{
				cb.Items.Add(category);
			}
			cb.SelectionChanged += new SelectionChangedEventHandler(cb_SelectionChanged);
			g.Children.Add(cb);
			Grid h = new Grid() { Background = Brushes.Red, VerticalAlignment = System.Windows.VerticalAlignment.Stretch };
			h.SetValue(Grid.RowProperty, 1);
			g.Children.Add(h);
			this.ShowTileCategory(h, cb);
			this.palette_host.Children.Add(g);
			cb.SelectedIndex = 0;
		}

		public string ActiveCategory { get; set; }

		void cb_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			ComboBox cb = (ComboBox)sender;
			this.ShowTileCategory((cb.Parent as Grid).Children[1] as Grid, cb);
		}
		private void ShowTileCategory(Grid host, ComboBox comboBox)
		{
			string category = (string)comboBox.SelectedItem;
			this.ActiveCategory = category;
			ListBox lb = new ListBox() { VerticalAlignment = System.Windows.VerticalAlignment.Stretch };
			List<Tile> tiles = TileStore.GetTilesInCategory(category);
			foreach (Tile tile in tiles)
			{
				ListBoxItem lbi = new ListBoxItem();
				lbi.Content = new Image() { Source = tile.Image };
				lb.Items.Add(lbi);
			}
			lb.SelectionChanged += new SelectionChangedEventHandler(lb_SelectionChanged);
			host.Children.Add(lb);
		}

		public Tile ActiveTile { get; set; }

		void lb_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			ListBox lb = (ListBox)sender;
			string category = this.ActiveCategory;
			if (!string.IsNullOrEmpty(category))
			{
				List<Tile> tiles = TileStore.GetTilesInCategory(category);
				int index = lb.SelectedIndex;
				if (index >= 0)
				{
					this.ActiveTile = tiles[index];
				}
			}
		}



		private bool mouse_is_down = false;
		private int start_drag_x = 0;
		private int start_drag_y = 0;
		private int end_drag_x = 0;
		private int end_drag_y = 0;

		void mouse_catcher_MouseMove(object sender, MouseEventArgs e)
		{
			if (ActiveMap == null) return;

			if (this.ActiveTool == Tool.IdMarker) { return; }

			if (this.mouse_is_down)
			{
				Point p = e.GetPosition(this.mouse_catcher);
				if (this.ActiveTool == Tool.Tile)
				{
					this.Do_Draw(p);
				}
				int x = GetX(p.X);
				int y = GetY(p.Y);
				if (this.ActiveTool != Tool.Tile)
				{
					this.ChangeTheseHighlights(start_drag_x, start_drag_y, this.end_drag_x, this.end_drag_y, x, y);
				}
				this.end_drag_x = x;
				this.end_drag_y = y;
			}
		}

		void mouse_catcher_MouseUp(object sender, MouseButtonEventArgs e)
		{
			if (ActiveMap == null) return;

			this.mouse_is_down = false;

			if (this.ActiveTool == Tool.IdMarker) { return; }

			if (this.ActiveTool != Tool.Tile)
			{
				int left = 0;
				int right = ActiveMap.Width - 1;
				int top = 0;
				int bottom = ActiveMap.Height - 1;

				for (int x = left; x <= right; ++x)
				{
					for (int y = top; y <= bottom; ++y)
					{
						this.GetGridCell(x, y).Background = Brushes.Transparent;
					}
				}

				left = Math.Max(left, Math.Min(this.start_drag_x, this.end_drag_x));
				right = Math.Min(right, Math.Max(this.start_drag_x, this.end_drag_x));
				top = Math.Max(top, Math.Min(this.start_drag_y, this.end_drag_y));
				bottom = Math.Min(bottom, Math.Max(this.start_drag_y, this.end_drag_y));

				for (int x = left; x <= right; ++x)
				{
					for (int y = top; y <= bottom; ++y)
					{
						this.Do_Draw(x, y);
					}
				}
			}
		}

		private int GetX(double x)
		{
			return Math.Max(0, Math.Min(ActiveMap.Width - 1, (int)(x / 32)));
		}
		private int GetY(double y)
		{
			return Math.Max(0, Math.Min(ActiveMap.Height - 1, (int)(y / 32)));
		}

		void mouse_catcher_MouseDown(object sender, MouseButtonEventArgs e)
		{
			if (ActiveMap == null) return;

			this.mouse_is_down = true;
			Point p = e.GetPosition(this.mouse_catcher);
			this.start_drag_x = GetX(p.X);
			this.start_drag_y = GetY(p.Y);
			this.end_drag_x = this.start_drag_x;
			this.end_drag_y = this.start_drag_y;

			if (this.ActiveTool != Tool.Tile && this.ActiveTool != Tool.IdMarker)
			{
				this.HighlightThese(start_drag_x, this.start_drag_y, this.end_drag_x, this.end_drag_y);
			}
			else
			{
				this.Do_Draw(p);
			}
		}

		private static readonly SolidColorBrush gridHighlight = new SolidColorBrush(Color.FromArgb(100, 255, 255, 255));

		private void HighlightThese(int startX, int startY, int endX, int endY)
		{
			Border r = this.GetGridCell(startX, startY);
			r.Background = gridHighlight;
		}

		private void ChangeTheseHighlights(int startX, int startY, int endXA, int endYA, int endXB, int endYB)
		{
			HashSet<Border> before = new HashSet<Border>();
			HashSet<Border> after = new HashSet<Border>();

			int xLeft = Math.Min(startX, endXA);
			int xRight = Math.Max(startX, endXA);
			int yTop = Math.Min(startY, endYA);
			int yBottom = Math.Max(startY, endYA);

			int x;
			int y;
			for (x = xLeft; x <= xRight; ++x)
			{
				for (y = yTop; y <= yBottom; ++y)
				{
					Border r = this.GetGridCell(x, y);
					if (r != null) before.Add(r);
				}
			}

			xLeft = Math.Min(startX, endXB);
			xRight = Math.Max(startX, endXB);
			yTop = Math.Min(startY, endYB);
			yBottom = Math.Max(startY, endYB);

			for (x = xLeft; x <= xRight; ++x)
			{
				for (y = yTop; y <= yBottom; ++y)
				{
					Border r = this.GetGridCell(x, y);
					if (r != null) after.Add(this.GetGridCell(x, y));
				}
			}

			List<Border> remove_these = new List<Border>();
			foreach (Border r in after)
			{
				if (before.Contains(r))
				{
					remove_these.Add(r);
				}
			}
			foreach (Border r in remove_these)
			{
				after.Remove(r);
				before.Remove(r);
			}

			foreach (Border r in after)
			{
				r.Background = gridHighlight;
			}

			foreach (Border r in before)
			{
				r.Background = Brushes.Transparent;
			}
		}

		private void Do_Draw(Point p)
		{
			int x = GetX(p.X);
			int y = GetY(p.Y);
			this.Do_Draw(x, y);
		}

		private int GetLayerIndex(string layerName)
		{
			int index;
			switch (layerName)
			{
				case "A": index = 0; break;
				case "B": index = 1; break;
				case "C": index = 2; break;
				case "D": index = 3; break;
				case "E": index = 4; break;
				case "F": index = 5; break;
				default: index = 6; break; // stairs
			}
			return index;
		}

		private Grid GetLayer(string layerName)
		{
			int index = this.GetLayerIndex(layerName);
			return this.layerstack.Children[index] as Grid;
		}


		private int GetDetailLayerIndex(string detailLayer)
		{
			int index;

			switch (detailLayer)
			{
				case "Base": index = 0; break;
				case "BaseAdorn": index = 1; break;
				case "BaseDetail": index = 2; break;
				case "Doodad": index = 3; break;
				case "DoodadAdorn": index = 4; break;
				default: index = 5; break; // excessive
			}

			return index;
		}
		private Grid GetDetailLayer(string layerName, string detailLayer)
		{
			Grid layer = this.GetLayer(layerName);
			int index = this.GetDetailLayerIndex(detailLayer);

			return layer.Children[index] as Grid;
		}

		private void RefreshLayer(string primaryLayer)
		{
			int index = this.GetLayerIndex(primaryLayer);
			this.layerstack.Children.RemoveAt(index);
			this.layerstack.Children.Insert(index, this.PopulateLayer(primaryLayer));
		}

		private void RefreshDetail(string primaryLayer, string detailLayer)
		{
			Grid layer = this.GetLayer(primaryLayer);
			int index = this.GetDetailLayerIndex(detailLayer);
			layer.Children.RemoveAt(index);
			layer.Children.Insert(index, this.PopulateDetail(primaryLayer, detailLayer));
		}

		private void RefreshTile(string primaryLayer, string detailLayer, int x, int y)
		{
			Map m = Model.Instance.ActiveMap;
			Grid layer = this.GetDetailLayer(primaryLayer, detailLayer);
			int index = y * m.Width + x;
			Tile t = m.GetTile(primaryLayer, detailLayer, x, y);

			(layer.Children[index] as Image).Source = t != null ? t.Image : null;
		}

		private void Do_Draw(int x, int y)
		{
			Map map = Model.Instance.ActiveMap;
			
			if (map != null && x >= 0 && x < map.Width && y >= 0 && y < map.Height)
			{
				string layer = this.ActivePrimaryLayer;
				string detail = this.ActiveDetailLayer;
				int left, right, top, bottom;
				switch (this.ActiveTool)
				{
					case Tool.IdMarker:
						AddId addid = new AddId(x, y, this.ActivePrimaryLayer);
						if (addid.ShowDialog() ?? false)
						{
							this.UpdateIdHighlights();
						}
						this.mouse_is_down = false;
						
						break;
					case Tool.Tile:
						if (this.ActiveTile != null)
						{
							map.SetTile(layer, detail, x, y, this.ActiveTile);
							this.RefreshTile(layer, detail, x, y);
						}
						break;
					case Tool.Rectangle:
						if (this.ActiveTile != null)
						{
							left = Math.Min(this.start_drag_x, this.end_drag_x);
							right = Math.Max(this.start_drag_x, this.end_drag_x);
							top = Math.Min(this.start_drag_y, this.end_drag_y);
							bottom = Math.Max(this.start_drag_y, this.end_drag_y);

							for (int tx = left; tx <= right; ++tx)
							{
								for (int ty = top; ty <= bottom; ++ty)
								{
									map.SetTile(layer, detail, tx, ty, this.ActiveTile);
									this.RefreshTile(layer, detail, tx, ty);
								}
							}
						}
						break;
					case Tool.EraserDetail:
						left = Math.Min(this.start_drag_x, this.end_drag_x);
						right = Math.Max(this.start_drag_x, this.end_drag_x);
						top = Math.Min(this.start_drag_y, this.end_drag_y);
						bottom = Math.Max(this.start_drag_y, this.end_drag_y);

						for (int tx = left; tx <= right; ++tx)
						{
							for (int ty = top; ty <= bottom; ++ty)
							{
								map.SetTile(layer, detail, tx, ty, null);
								this.RefreshTile(layer, detail, tx, ty);
							}
						}
						break;
					case Tool.EraserLayer:
						left = Math.Min(this.start_drag_x, this.end_drag_x);
						right = Math.Max(this.start_drag_x, this.end_drag_x);
						top = Math.Min(this.start_drag_y, this.end_drag_y);
						bottom = Math.Max(this.start_drag_y, this.end_drag_y);

						for (int tx = left; tx <= right; ++tx)
						{
							for (int ty = top; ty <= bottom; ++ty)
							{
								foreach (string det in "Base BaseAdorn BaseDetail Doodad DoodadAdorn Excessive".Split(' '))
								{
									map.SetTile(layer, det, tx, ty, null);
									this.RefreshTile(layer, det, tx, ty);
								}
							}
						}
						break;
					case Tool.EraserDeep:
						left = Math.Min(this.start_drag_x, this.end_drag_x);
						right = Math.Max(this.start_drag_x, this.end_drag_x);
						top = Math.Min(this.start_drag_y, this.end_drag_y);
						bottom = Math.Max(this.start_drag_y, this.end_drag_y);

						for (int tx = left; tx <= right; ++tx)
						{
							for (int ty = top; ty <= bottom; ++ty)
							{
								foreach (string det in "Base BaseAdorn BaseDetail Doodad DoodadAdorn Excessive".Split(' '))
								{
									foreach (string lay in "A B C D E F Stairs".Split(' '))
									{
										map.SetTile(lay, det, tx, ty, null);
										this.RefreshTile(lay, det, tx, ty);
									}
								}
							}
						}
						break;
					default: break;
				}
			}
		}

		void file_new_Click(object sender, RoutedEventArgs e)
		{
			NewMap nm = new NewMap();
			nm.ShowDialog();
		}

		public Grid LayerList { get { return this.layerstack; } }

		public void PopulateArtboard()
		{
			if (Model.Instance.ActiveMap != null)
			{
				Map map = Model.Instance.ActiveMap;
				this.tileWidth = map.Width;
				this.tileHeight = map.Height;

				this.PopulateGrid();
				this.layerstack.Children.Clear();

				foreach (string layerName in "A B C D E F Stairs".Split(' '))
				{
					Grid layer = this.PopulateLayer(layerName);
					this.layerstack.Children.Add(layer);
				}
				MainWindow.Instance.layer_all_on_Click(null, null);
			}
		}

		private Border GetGridCell(int x, int y)
		{
			if (ActiveMap != null)
			{
				return this.gridoverlay.Children[ActiveMap.Width * y + x] as Border;
			}
			return null;
		}

		private void PopulateGrid()
		{
			Grid overlay = this.gridoverlay;
			overlay.Children.Clear();
			SolidColorBrush black = Brushes.Black;
			for (int y = 0; y < this.tileHeight; ++y)
			{
				for (int x = 0; x < this.tileWidth; ++x)
				{
					Border r = new Border() { Width = 32, Height = 32, HorizontalAlignment = System.Windows.HorizontalAlignment.Left, VerticalAlignment = System.Windows.VerticalAlignment.Top };
					r.Margin = new Thickness(x * 32, y * 32, 0, 0);
					r.BorderBrush = black;
					r.BorderThickness = new Thickness(.5);
					overlay.Children.Add(r);
				}
			}
		}

		private Grid PopulateLayer(string layerName)
		{
			Grid layer = new Grid();
			string[] details = "Base BaseAdorn BaseDetail Doodad DoodadAdorn Excessive".Split(' ');
			foreach (string detail in details)
			{
				layer.Children.Add(this.PopulateDetail(layerName, detail));
			}
			return layer;
		}

		private Grid PopulateDetail(string layerName, string detailLayer)
		{
			Grid layer = new Grid();
			Image img;
			Tile tile;
			Map map = Model.Instance.ActiveMap;
			for (int y = 0; y < this.tileHeight; ++y)
			{
				for (int x = 0; x < this.tileWidth; ++x)
				{
					tile = map.GetTile(layerName, detailLayer, x, y);
					img = new Image() { Width = 32, Height =32, HorizontalAlignment = System.Windows.HorizontalAlignment.Left, VerticalAlignment = System.Windows.VerticalAlignment.Top };
					img.Margin = new Thickness(x * 32, y * 32, 0, 0);

					if (tile != null)
					{
						img.Source = tile.Image;
					}
					layer.Children.Add(img);
				}
			}
			return layer;
		}
	}
}
