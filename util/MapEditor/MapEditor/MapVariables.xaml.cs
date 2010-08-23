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
    /// Interaction logic for MapVariables.xaml
    /// </summary>
    public partial class MapVariables : Window
    {
        public MapVariables()
        {
            InitializeComponent();
            this.AddValue.Click += new RoutedEventHandler(AddValue_Click);
        }

        void AddValue_Click(object sender, RoutedEventArgs e)
        {
            StackPanel added = new StackPanel();
            added.Orientation = Orientation.Horizontal;
            TextBox key = new TextBox();
            key.Width = 100;
            
            TextBox value=new TextBox();
            key.HorizontalAlignment = HorizontalAlignment.Stretch;
            value.HorizontalAlignment = HorizontalAlignment.Stretch;
            value.Width = 100;
            added.Children.Add(key);
            added.Children.Add(value);
            
            variables.Items.Add(added);
        }


    }
}
