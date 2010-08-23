using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MapEditor
{
	public class Map
	{
		public string Name { get; set; }
		private Dictionary<string, string> values = new Dictionary<string, string>();
		private Dictionary<string, List<ID>> idsByLayer = new Dictionary<string, List<ID>>();
		private List<ID> ids = new List<ID>();
		private Dictionary<string, ID> idsByName = new Dictionary<string, ID>();
		private Dictionary<string, Dictionary<string, List<Tile>>> layers;
		public int Width { get; set; }
		public int Height { get; set; }

		public bool IsValid { get; set; }

		// load from file
		public Map(string name)
		{
			this.Name = name;
			if (this.Read(name))
			{
				this.IsValid = this.ParseIds() && this.ParseScripts() && this.ParseTiles();
			}
			else
			{
				this.IsValid = false;
			}
		}

		// create blank
		public Map(string name, int width, int height)
		{
			this.Name = name;
			this.Width = width;
			this.Height = height;
			this.layers = this.InitializeLayers(width, height, true);
		}

		public Tile GetTile(string layerName, string detailLayer, int x, int y)
		{
			return this.layers[layerName][detailLayer][x + y * this.Width];
		}

		private Dictionary<string, Dictionary<string, List<Tile>>> InitializeLayers(int width, int height, bool fill)
		{
			this.idsByLayer = new Dictionary<string, List<ID>>();

			Dictionary<string, Dictionary<string, List<Tile>>> layers = new Dictionary<string, Dictionary<string, List<Tile>>>();
			foreach (string layerName in "A B C D E F Stairs".Split(' '))
			{
				this.idsByLayer.Add(layerName, new List<ID>());
				Dictionary<string, List<Tile>> layer = new Dictionary<string, List<Tile>>();

				foreach (string detailLayer in "Base BaseAdorn BaseDetail Doodad DoodadAdorn Excessive".Split(' '))
				{
					List<Tile> tileList = new List<Tile>(width * height);
					layer[detailLayer] = tileList;
					if (fill)
					{
						for (int i = 0; i < width * height; ++i)
						{
							tileList.Add(null);
						}
					}
				}
				layers[layerName] = layer;
			}

			return layers;
		}

		public void SetTile(string layerName, string detailLayer, int x, int y, Tile tile)
		{
			this.layers[layerName][detailLayer][y * this.Width + x] = tile;
		}

		private bool ParseScripts()
		{
			if (this.values.ContainsKey("scripts"))
			{
				string[] scripts = this.values["scripts"].Split(new string[] { "|||" }, StringSplitOptions.RemoveEmptyEntries);
				List<string> final_script = new List<string>();
				foreach (string script in scripts)
				{
					string[] lines = script.Trim().Split('|');
					foreach (string line in lines)
					{
						final_script.Add(line.Trim());
					}

					string name = final_script[0];
					final_script.RemoveAt(0);

					if (this.idsByName.ContainsKey(name))
					{
						this.idsByName[name].Script = string.Join("\n", final_script.ToArray());
					}
					else
					{
						System.Windows.MessageBox.Show("Invalid script ID name");
					}
				}
			}
			return true;
		}

		private bool ParseIds()
		{

			this.idsByLayer = new Dictionary<string, List<ID>>();
			foreach (string layerName in "A B C D E F Stairs".Split(' '))
			{
				this.idsByLayer.Add(layerName, new List<ID>());
			}

			if (this.values.ContainsKey("IDs"))
			{
				string[] ids = this.values["IDs"].Trim().Split(',');
				foreach (string id in ids)
				{
					string[] parts = id.Trim().Split('|');
					if (parts.Length == 4)
					{
						int x;
						int y;
						string name = parts[0];
						string layer = parts[1];
						if (!int.TryParse(parts[2], out x))
						{
							System.Windows.MessageBox.Show("One of the X coordinates for a tile ID is not a valid number");
							return false;
						}
						if (!int.TryParse(parts[3], out y))
						{
							System.Windows.MessageBox.Show("One of the Y coordinates for a tile ID is not a valid number");
							return false;
						}

						if (this.idsByName.ContainsKey(name))
						{
							System.Windows.MessageBox.Show("Duplicate tile ID in this map file");
							return false;
						}
						ID id_instance = new ID() { Layer = layer, Name = name, X = x, Y = y };
						this.ids.Add(id_instance);
						this.idsByLayer[layer].Add(id_instance);
						this.idsByName.Add(name, id_instance);
					}
				}
			}

			return true;
		}

		private bool ParseTiles()
		{
			this.layers = this.InitializeLayers(this.Width, this.Height, true);

			foreach (string layer in "A B C D E F Stairs".Split(' '))
			{
				string layerName = "Layer" + layer;
				if (this.values.ContainsKey(layerName))
				{
					string[] spots = this.values[layerName].Trim().Split(',');
					if (spots.Length != this.Width * this.Height)
					{
						System.Windows.MessageBox.Show(layerName + " didn't have the correct number of tiles in it");
						return false;
					}
					else
					{
						int index = 0;
						foreach (string spot in spots)
						{
							// Base BaseAdorn BaseDetail Doodad DoodadAdorn Excessive
							string[] tiles = spot.Split('|');
							if (tiles.Length != 6)
							{
								System.Windows.MessageBox.Show(layerName + " has a tile without the correct number of ids in the stack");
								return false;
							}
							else
							{
								for (int i = 0; i < 6; ++i)
								{
									string name = "";
									switch (i)
									{
										case 0: name = "Base"; break;
										case 1: name = "BaseAdorn"; break;
										case 2: name = "BaseDetail"; break;
										case 3: name = "Doodad"; break;
										case 4: name = "DoodadAdorn"; break;
										case 5: name = "Excessive"; break;
										default: break;
									}

									string tileId = tiles[i].Trim();
									Tile t = null;
									if (tileId != "")
									{
										t = TileStore.Get(tileId);
									}
									this.layers[layer][name][index] = t;
								}
							}
							++index;
						}
					}
				}
			}

			return true;
		}

		public List<ID> Ids { get { return this.ids; } }

		public void AddId(string layer, int x, int y, string name)
		{
			if (this.idsByName.ContainsKey(name))
			{
				System.Windows.MessageBox.Show("An ID of that name alrady exists. The ID was not added.");
			}
			else
			{
				foreach (ID idc in this.ids)
				{
					if (idc.Layer == layer && idc.X == x && idc.Y == y)
					{
						System.Windows.MessageBox.Show("There's already an ID on that layer in that spot. The ID was not added.");
						return;
					}
				}

				ID id = new ID() { Name = name.Trim(), X = x, Y = y, Layer = layer };
				this.ids.Add(id);
				this.idsByLayer[layer].Add(id);
				this.idsByName.Add(id.Name, id);

				MainWindow.Instance.UpdateIdHighlights();
			}
		}

		public void Save()
		{
			this.values["width"] = this.Width.ToString();
			this.values["height"] = this.Height.ToString();
			
			Tile tile;
			foreach (string layerName in "A B C D E F Stairs".Split(' '))
			{
				bool layerContainsAnything = false;
				List<string> spots = new List<string>();
				for (int y = 0; y < this.Height; ++y)
				{
					for (int x = 0; x < this.Width; ++x)
					{
						string spot = "";
						foreach (string detailsName in "Base BaseAdorn BaseDetail Doodad DoodadAdorn Excessive".Split(' '))
						{
							tile = this.GetTile(layerName, detailsName, x, y);
							spot += "|" + (tile == null ? "" : tile.ID);
							if (tile != null)
							{
								layerContainsAnything = true;
							}
						}
						spots.Add(spot.Substring(1));
					}
				}

				if (layerContainsAnything)
				{
					this.values["Layer" + layerName] = string.Join(",", spots.ToArray());
				}
				else if (this.values.ContainsKey("Layer" + layerName))
				{
					this.values.Remove("Layer" + layerName);
				}
			}

			string ids = "";
			string scripts = "";

			foreach (ID id in this.ids)
			{
				ids += "," + id.Name + "|" + id.Layer + "|" + id.X.ToString() + "|" + id.Y.ToString();
				if (!string.IsNullOrEmpty(id.Script))
				{
					scripts += "|||" + id.Name + "|" + string.Join("|", id.Script.Trim().Split('\n'));
				}
			}

			if (ids.Length > 0)
			{
				ids = ids.Substring(1);
				if (scripts.Length > 0)
				{
					scripts = scripts.Substring(3);
				}
			}

			this.values["IDs"] = ids;
			this.values["scripts"] = scripts;

			List<string> entries = new List<string>();
			foreach (string key in this.values.Keys)
			{
				string line = "#" + key + ":" + this.values[key];
				entries.Add(line);
			}
			string file_content = string.Join("\r\n", entries.ToArray());
			System.IO.File.WriteAllText(Model.Root + "\\maps\\" + this.Name + ".txt", file_content,	System.Text.Encoding.UTF8);
		}

		private bool Read(string name)
		{
			string filename = Model.Root + "\\maps\\" + name + ".txt";
			string[] lines = new string[0];
			try
			{
				lines = System.IO.File.ReadAllLines(filename);
			}
			catch (Exception)
			{
				System.Windows.MessageBox.Show("Error occured while reading file");
				return false;
			}

			foreach (string line in lines)
			{
				string[] parts = line.Trim().Split(':');
				if (parts.Length >= 2 && parts[0][0] == '#')
				{
					string key = parts[0].Substring(1);
					string value = parts[1];
					for (int i = 2; i < parts.Length; ++i)
					{
						value += ":" + parts[i];
					}

					if (this.values.ContainsKey(key))
					{
						System.Windows.MessageBox.Show("Map file contains duplicate keys");
						return false;
					}
					
					this.values.Add(key, value);
					
				}
			}
			int width = 0;
			int height = 0;

			if (!this.values.ContainsKey("width") || !int.TryParse(this.values["width"], out width))
			{
				System.Windows.MessageBox.Show("This map does not have a valid width");
				return false;
			}
			if (!this.values.ContainsKey("height") || !int.TryParse(this.values["height"], out height))
			{
				System.Windows.MessageBox.Show("This map does not have a valid height");
				return false;
			}

			this.Width = width;
			this.Height = height;

			return true;
		}
	}
}
