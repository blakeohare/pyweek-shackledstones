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
		EraserTile,
		EraserDeep,
		EraserLayer,
		Rectangle,
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
			this.ActiveTool = Tool.None;
			me = this;
			InitializeComponent();
			this.file_new.Click += new RoutedEventHandler(file_new_Click);
			this.file_open.Click += new RoutedEventHandler(file_open_Click);
			this.file_save.Click += new RoutedEventHandler(file_save_Click);
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

			//Base BaseAdorn BaseDetail Doodad DoodadAdorn Excessive
			this.active_detail_layer.Items.Add("Base");
			this.active_detail_layer.Items.Add("BaseAdorn");
			this.active_detail_layer.Items.Add("BaseDetail");
			this.active_detail_layer.Items.Add("Doodad");
			this.active_detail_layer.Items.Add("DoodadAdorn");
			this.active_detail_layer.Items.Add("Excessive");
			this.active_detail_layer.SelectionChanged += new SelectionChangedEventHandler(active_detail_layer_SelectionChanged);
			this.active_detail_layer.SelectedIndex = 0;

			this.tool_selector.SelectedIndex = 0;
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
		}

		void active_detail_layer_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			this.ActiveDetailLayer = e.AddedItems[0].ToString();
		}

		public string ActivePrimaryLayer { get; set; }
		public string ActiveDetailLayer { get; set; }

		private Tool ActiveTool { get; set; }

		void tool_selector_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			ComboBox cb = sender as ComboBox;
			if (cb.SelectedItem == this.cb_erased)
			{
				this.ActiveTool = Tool.EraserDeep;
				this.palette_host.Children.Clear();
			}
			else if (cb.SelectedItem == this.cb_erasel)
			{
				this.ActiveTool = Tool.EraserLayer;
				this.palette_host.Children.Clear();
			}
			else if (cb.SelectedItem == this.cb_eraset)
			{
				this.ActiveTool = Tool.EraserTile;
				this.palette_host.Children.Clear();
			}
			else if (cb.SelectedItem == this.cb_rect)
			{
				this.ActiveTool = Tool.Rectangle;
				this.palette_host.Children.Clear();
				this.Show_Rectangle_Palette();
			}
			else if (cb.SelectedItem == this.cb_tile)
			{
				this.ActiveTool = Tool.Tile;
				this.palette_host.Children.Clear();
				this.Show_Tile_Palette();
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

		void mouse_catcher_MouseMove(object sender, MouseEventArgs e)
		{
			if (this.mouse_is_down)
			{
				Point p = e.GetPosition(this.mouse_catcher);
				this.Do_Draw(p);
			}
		}

		void mouse_catcher_MouseUp(object sender, MouseButtonEventArgs e)
		{
			this.mouse_is_down = false;
		}

		void mouse_catcher_MouseDown(object sender, MouseButtonEventArgs e)
		{
			this.mouse_is_down = true;
			Point p = e.GetPosition(this.mouse_catcher);
			this.Do_Draw(p);
		}

		private void Do_Draw(Point p)
		{
			int x = (int)(p.X / 32);
			int y = (int)(p.Y / 32);
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

				switch (this.ActiveTool)
				{
					case Tool.Tile:
						if (this.ActiveTile != null)
						{
							map.SetTile(layer, detail, x, y, this.ActiveTile);
							this.RefreshTile(layer, detail, x, y);
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
			}
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
					Rectangle r = new Rectangle() { Width = 32, Height = 32, HorizontalAlignment = System.Windows.HorizontalAlignment.Left, VerticalAlignment = System.Windows.VerticalAlignment.Top };
					r.Margin = new Thickness(x * 32, y * 32, 0, 0);
					r.Stroke = black;
					r.StrokeThickness = .5;
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
