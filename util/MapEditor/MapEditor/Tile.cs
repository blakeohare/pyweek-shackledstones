using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Text;

namespace MapEditor
{
	public class Tile
	{
		private static Dictionary<string, Tile> tiles = new Dictionary<string, Tile>();

		public string ID { get; set; }
		public ImageSource Image { get; set; }
		public string Name { get; set; }

		public Tile(string id, Uri fileUri)
		{
			this.ID = id;
			this.Image = new BitmapImage(fileUri);
			this.Name = System.IO.Path.GetFileNameWithoutExtension(fileUri.OriginalString);
		}
	}
}
