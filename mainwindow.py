import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import numpy as np
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from BornAgainScript import ba, get_sample, get_simulation, run_simulation
from samples import Sample
from DialogWindows import NewSample, SampleDatabase
class MainWindow(Gtk.ApplicationWindow):


    def __init__(self):
        Gtk.Window.__init__(self, title="Header Bar")
        self.set_border_width(10)

        self.samplelist = []
        self.sampleamount = 1


        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "KARIN 2.0 (early alpha 0.05))"
        self.set_titlebar(header_bar)

        #Audio button on the right
        menu_button = Gtk.MenuButton()
        cd_icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(cd_icon, Gtk.IconSize.BUTTON)
        menu_button.add(image)
        menumodel = Gio.Menu()
        menumodel.append("New Sample", "win.newsample")
        menumodel.append("Sample Database", "win.sampledatabase")
        menumodel.append("About", "win.about")
    #    submenu = Gio.Menu()
    #    submenu.append("Quit", "app.quit")
    #    menumodel.append_submenu("Other", submenu)
        menu_button.set_menu_model(menumodel)

        newsample_action = Gio.SimpleAction.new("newsample", None)
        newsample_action.connect("activate", self.newsample)
        self.add_action(newsample_action)
        sampledatabase_action = Gio.SimpleAction.new("sampledatabase", None)
        sampledatabase_action.connect("activate", self.sampledatabase)
        self.add_action(sampledatabase_action)
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_callback)
        self.add_action(about_action)




        header_bar.pack_end(menu_button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        openbutton = Gtk.Button()
        openbutton.add(Gtk.Label("Open"))
        box.add(openbutton)

        open_extend = Gtk.Button()
        open_extend.add(Gtk.Arrow(Gtk.ArrowType.DOWN, Gtk.ShadowType.NONE))
        open_extend.connect("clicked", self.button_clicked)
        box.add(open_extend)

        header_bar.pack_start(box)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        #first page
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False) #False -> all children do not get equal space
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox_right.set_homogeneous(False)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        label = Gtk.Label("This is a plain label")
        vbox_left.pack_start(label, True, True, 0)

        #Left aligned
        label = Gtk.Label()
        label.set_text("This is left aligned text. \n Oh wow multiple lines sooooooo cool.")
        label.set_justify(Gtk.Justification.LEFT)
        vbox_left.pack_start(label, True, True, 0)

        # Line wrap
        self.page1.add(hbox)

        X, Y = [], []
        for line in open('curve2.txt', 'r'):
            values = [float(s) for s in line.split()]
            X.append(values[0])
            Y.append(values[1])
        f = plt.figure()
        f.add_subplot(111)
        plt.plot(X, Y)
        plt.yscale('log')
#
        canvas = FigureCanvas(f)  # a Gtk.DrawingArea
        canvas.set_size_request(1200, 800)
        vbox_right.pack_start(canvas, False, True, 0)
  #      self.page1.add(vbox_right)



        self.notebook.append_page(self.page1, Gtk.Label('Specular data'))

        #second page
        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label('Hey there durr durr I am page two'))
        icon = Gtk.Image.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.MENU)
        self.notebook.append_page(self.page2, icon)

        #second page
        self.page3 = Gtk.Grid()
        #self.page3.set_row_homogeneous(True)
        self.page3.set_column_homogeneous(False)
        self.page3.set_border_width(10)
        self.button = Gtk.Button(label="Simulate")
        self.button.connect("clicked", self.button_clicked)
        self.bilayerfield = Gtk.Entry()
        self.bilayerfield.set_text("10")
        bilayerlabel = Gtk.Label("Bilayers N      ")
        bilayerlabel.set_justify(Gtk.Justification.RIGHT)

        self.interfacewidthfield = Gtk.Entry()
        self.interfacewidthfield.set_text("4.5")
        interfacewidthlabel = Gtk.Label("Interface Width (Å)      ")
        interfacewidthlabel.set_justify(Gtk.Justification.RIGHT)


        self.lattercorlengthfield = Gtk.Entry()
        self.lattercorlengthfield.set_text("200")
        lattercorrlengthlabel = Gtk.Label("Latteral correlation length (Å)      ")
        lattercorrlengthlabel.set_justify(Gtk.Justification.RIGHT)


        self.crosscorlengthfield = Gtk.Entry()
        self.crosscorlengthfield.set_text("10000")
        crosscorrlengthlabel = Gtk.Label("Cross correlation length (Å)      ")
        crosscorrlengthlabel.set_justify(Gtk.Justification.RIGHT)

        self.page3.attach(bilayerlabel,1,1,1,1)
        self.page3.attach(self.bilayerfield,2,1,1,1)
        self.page3.attach(interfacewidthlabel,1,2,1,1)
        self.page3.attach(self.interfacewidthfield,2,2,1,1)

        self.page3.attach(lattercorrlengthlabel,1,3,1,1)
        self.page3.attach(self.lattercorlengthfield,2,3,1,1)
        self.page3.attach(crosscorrlengthlabel,1,4,1,1)
        self.page3.attach(self.crosscorlengthfield,2,4,1,1)


        self.simulatebutton = Gtk.Button(label="Simulate")
        self.simulatebutton.set_vexpand(False)
        self.simulatebutton.set_hexpand(False)
        self.simulatebutton.connect("clicked", self.button_clicked)
        self.page3.attach(self.simulatebutton,2,5,1,1)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(X, Y)
        plt.yscale("linear")
        plt.draw()

        baplotcanvas = FigureCanvas(fig)  # a Gtk.DrawingArea
        baplotcanvas.set_size_request(1100, 800)
        self.page3.attach(baplotcanvas,3,1,5,400)

        self.notebook.append_page(self.page3, Gtk.Label("BornAgain"))

    def button_clicked(self, widget):
        print("Gametime")
        plt.clf()
        interfacewidth = float(self.interfacewidthfield.get_text())
        bilayers = int(self.bilayerfield.get_text())
        crosscorrlength = int(self.crosscorlengthfield.get_text())
        lattcorrlength = int(self.lattercorlengthfield.get_text())
        result = run_simulation(bilayers, interfacewidth, crosscorrlength, lattcorrlength)
        result_array = np.log(result.array())
        plt.pcolormesh(result_array)
        plt.draw()
        print(bilayers)
        print(self.bilayerfield.get_text())
        return result_array
        
        #       ba.plot_simulation_result(result, intensity_min=0.1)


        #ba.plot_simulation_result(result, intensity_min=0.1)

    def about_callback(self, action, parameter):
        print("You clicked \"About\"")
        dialog = DialogExample(self)

    def newsample(self, action, parameter):
        dialog = NewSample(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.newsample = dialog.get_result()
            print(self.newsample.sampleID)
            self.samplelist.append(self.newsample)
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()



    def sampledatabase(self, action, parameter):
     #  print(self.samplelist[0].sampleID.get_text())
        dialog = SampleDatabase(self, self.samplelist)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        dialog.destroy()


class DialogExample(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(            self,
            "My Dialog",
            parent,
            0,
            (
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK,
            ),
        )


        self.set_default_size(150, 100)

        label = Gtk.Label("© Sjoerd Broekhuijsen 2020")

        label = Gtk.Label("KARIN is licensed under the GPLv3 license")
        label.set_justify(Gtk.Justification.CENTER)

        box = self.get_content_area()
        box.add(label)
        self.show_all()

#sample1 = Sample("IFM20020", 200612, "1E-7")
#result = run_simulation()
#ba.plot_simulation_result(result, intensity_min=0.1)


window = MainWindow()
#window.maximize()
window.connect("delete-event", Gtk.main_quit) #connect close button to delete-event signal
window.show_all() #display windows
Gtk.main() #main loop, keeps window open

