using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MapEditor
{
	public static class TileStore
	{
		private static Dictionary<string, Tile> tiles = new Dictionary<string, Tile>();
		private static Dictionary<string, List<Tile>> categories = new Dictionary<string, List<Tile>>();

		public static Tile Get(string id)
		{
			return tiles[id];
		}

		public static string[] Categories
		{
			get
			{
				List<string> categories = new List<string>();
				foreach (string c in TileStore.categories.Keys)
				{
					categories.Add(c);
				}
				categories.Sort();
				return categories.ToArray();
			}
		}

		public static List<Tile> GetTilesInCategory(string category)
		{
			if (string.IsNullOrEmpty(category))
			{
				return new List<Tile>();
			}
			return categories[category];
		}

		static TileStore()
		{
			string[] lines = "".Split(' ');
			try
			{
				lines = System.IO.File.ReadAllLines(Model.Root + @"\data\tiles.txt");
			}
			catch (Exception e)
			{
				System.Windows.MessageBox.Show(e.ToString() + "\n" + e.Message + "\n" + System.Environment.CurrentDirectory  + "There was an error while initializing the tiles");
			}

			foreach (string line in lines)
			{
				string fline = line.Trim();
				if (fline.Length > 0 && fline[0] != '#')
				{
					string[] parts = fline.Split('\t');
					if (parts.Length == 4 || parts.Length == 5)
					{
						string id = parts[0].Trim();
						string category = parts[1].Trim();
						string physics = parts[2].Trim();
						string[] images = parts[3].Trim().Split('|');
						int animDelay = 4;
						if (parts.Length == 5)
						{
							if (!int.TryParse(parts[4], out animDelay))
							{
								System.Windows.MessageBox.Show("Looks like the row with tile ID: " + id + " has an invalid anim delay value. Should be a number.");
								return;
							}
						}

						string filename = Model.Root + "\\images\\tiles\\" + images[0].Replace('/', '\\');

						Tile t = new Tile(id, new Uri(filename, UriKind.Absolute));
						if (tiles.ContainsKey(id))
						{
							System.Windows.MessageBox.Show("Duplicate tile ID's in the tile definitions file");
							return;
						}

						tiles[id] = t;
						if (!categories.ContainsKey(category))
						{
							categories.Add(category, new List<Tile>());
						}

						categories[category].Add(t);
					}
				}
			}
		}
	}
}
