using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MapEditor
{
	public class Model
	{
		private static string root = System.Environment.CurrentDirectory.Split("\\util".Split(' '), StringSplitOptions.None)[0];
		public static string Root
		{
			get
			{
				return root;
			}
		}

		private static Model instance = new Model();
		public static Model Instance { get { return instance; } }

		public Map ActiveMap { get; set; }

		public void OpenMap(string name)
		{
			this.ActiveMap = new Map(name);
		}

		public void SaveMap()
		{
			if (this.ActiveMap != null)
			{
				this.ActiveMap.Save();
			}
		}

		public void NewMap(string name, int width, int height)
		{
			this.ActiveMap = new Map(name, width, height);
		}

		public int MapWidth { get { return this.ActiveMap.Width; } }
		public int MapHeight { get; set; }
	}
}
