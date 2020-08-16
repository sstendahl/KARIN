import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import numpy as np
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
from BornAgainScript import ba, get_sample, get_simulation, run_simulation
from samples import Sample
from DialogWindows import NewSample, SampleDatabase
class MainWindow(Gtk.ApplicationWindow):
#Testing git

    def __init__(self):
        self.samplelist = []
        with open('samplelist.csv', 'r') as file:
            reader = csv.reader(file)
            i = 0
            for row in reader:
                if i == 0:
                    print(f'Column names are {", ".join(row)}')
                    print("hi")
                    i = i + 1
                else:
                    print(row[0])
                    newSample = Sample(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]) #SampleID, Date, BG pressure
                    self.samplelist.append(newSample)

        Gtk.Window.__init__(self, title="Header Bar")
        self.set_border_width(10)

        self.sampleamount = 1


        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "KARIN 2.0 (early alpha 0.10))"
        self.set_titlebar(header_bar)

        #Audio button on the right
        menu_button = Gtk.MenuButton()
        cd_icon = Gio.ThemedIcon(name="open-menu-symbolic") #document-open-symbolic
        image = Gtk.Image.new_from_gicon(cd_icon, Gtk.IconSize.BUTTON)
        menu_button.add(image)
        menumodel = Gio.Menu()
        menumodel.append("New Sample", "win.newsample")
        #menumodel.append("Sample Database", "win.sampledatabase")
        menumodel.append("About", "win.about")
    #    submenu = Gio.Menu()
    #    submenu.append("Quit", "app.quit")
    #    menumodel.append_submenu("Other", submenu)
        menu_button.set_menu_model(menumodel)

        newsample_action = Gio.SimpleAction.new("newsample", None)
        newsample_action.connect("activate", self.newsample)
        self.add_action(newsample_action)
        #sampledatabase_action = Gio.SimpleAction.new("sampledatabase", None)
        #sampledatabase_action.connect("activate", self.sampledatabase)
        #self.add_action(sampledatabase_action)
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_callback)
        self.add_action(about_action)




        header_bar.pack_end(menu_button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        openbutton = Gtk.Button()
        openbutton.add(Gtk.Label("Sample DB"))
        openbutton.connect("clicked", self.sampledatabase)
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

        main_area = Gtk.Stack()
        main_area.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        main_area.set_transition_duration(540)

        specularlabel = Gtk.Label("Options for specular data will be shown here")

        main_area.add_titled(specularlabel, "specularlabel", "Specular")

        offspeclabel = Gtk.Label("Options for off-specular data will be shown here")
        main_area.add_titled(offspeclabel, "offspecularlabel", "Off-specular")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(main_area)

        self.hbox = Gtk.Box(spacing=10)
        self.hbox.set_homogeneous(False) #False -> all children do not get equal space
        self.vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.vbox_left.set_homogeneous(False)
        self.vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.vbox_right.set_homogeneous(False)

        self.hbox.pack_start(self.vbox_left, True, True, 0)
        self.hbox.pack_start(self.vbox_right, True, True, 0)

        label = Gtk.Label("This is a plain label")
        label.set_justify(Gtk.Justification.LEFT)
        self.vbox_left.pack_start(stack_switcher, False, True, 0)
        self.vbox_left.pack_start(main_area, True, True, 0)

        # Line wrap
        self.page1.add(self.hbox)
        self.f = plt.figure()
        self.canvas = FigureCanvas(self.f)  # a Gtk.DrawingArea
        self.vbox_right.pack_start(self.canvas, False, True, 0)
        self.ax = self.f.add_subplot(111)
        plt.xlabel('Grazing incidence angle θ (°)')
        plt.ylabel('Intensity (arb. u)')
        plt.yscale('log')
#
        self.canvas.set_size_request(1200, 800)
        #self.draw_plot()
  #      self.page1.add(vbox_right)



        self.notebook.append_page(self.page1, Gtk.Label('X-Ray reflectivity'))

        self.page3 = Gtk.Box()
        self.page3.set_border_width(10)
        self.page3.add(Gtk.Label('Hey there durr durr I am page three'))
        icon = Gtk.Image.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.MENU)
        self.notebook.append_page(self.page3, Gtk.Label('2D Maps'))


        #second page
        self.page4 = Gtk.Grid()
        #self.page3.set_row_homogeneous(True)
        self.page4.set_column_homogeneous(False)
        self.page4.set_border_width(10)
        self.button = Gtk.Button(label="Simulate")
        self.button.connect("clicked", self.button_clicked)
        self.bilayerfield = Gtk.Entry()
        self.bilayerfield.set_text("10")

        bilayerlabel = Gtk.Label("Bilayers N      ")
        bilayerlabel.set_alignment(1, 0.5)


        self.interfacewidthfield = Gtk.Entry()
        self.interfacewidthfield.set_text("4.5")
        interfacewidthlabel = Gtk.Label("Interface Width (Å)      ")
        interfacewidthlabel.set_alignment(1, 0.5)


        self.lattercorlengthfield = Gtk.Entry()
        self.lattercorlengthfield.set_text("200")
        lattercorrlengthlabel = Gtk.Label("Latteral correlation length (Å)      ")
        lattercorrlengthlabel.set_alignment(1, 0.5)


        self.crosscorlengthfield = Gtk.Entry()
        self.crosscorlengthfield.set_text("10000")
        crosscorrlengthlabel = Gtk.Label("Cross correlation length (Å)      ")
        crosscorrlengthlabel.set_alignment(1, 0.5)

        self.page4.attach(bilayerlabel,1,1,1,1)
        self.page4.attach(self.bilayerfield,2,1,1,1)
        self.page4.attach(interfacewidthlabel,1,2,1,1)
        self.page4.attach(self.interfacewidthfield,2,2,1,1)

        self.page4.attach(lattercorrlengthlabel,1,3,1,1)
        self.page4.attach(self.lattercorlengthfield,2,3,1,1)
        self.page4.attach(crosscorrlengthlabel,1,4,1,1)
        self.page4.attach(self.crosscorlengthfield,2,4,1,1)




        self.simulatebutton = Gtk.Button(label="Simulate")
        self.simulatebutton.set_vexpand(False)
        self.simulatebutton.set_hexpand(False)
        self.simulatebutton.connect("clicked", self.button_clicked)
        self.page4.attach(self.simulatebutton,2,5,1,1)

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        self.spinner.stop()
        self.page4.attach(self.spinner,2,6,1,1)

        fig = plt.figure()
        plt.yscale("log")
        plt.draw()
        ax = fig.add_subplot(111)

        baplotcanvas = FigureCanvas(fig)  # a Gtk.DrawingArea
        baplotcanvas.set_size_request(1100, 800)
        self.page4.attach(baplotcanvas,3,1,5,400)

        self.notebook.append_page(self.page4, Gtk.Label("BornAgain"))

    def button_clicked(self, widget):
        self.spinner.start()
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
        self.spinner.stop()
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
            self.samplelist.append(self.newsample)
            with open('samplelist.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Sample ID", "Date", "Amount of Layers", "Materials", "Magnetron Powers", "Growth Times", "Inlet gasses", "Background Pressure", "Period", "Gamma ratio", "Bias", "Comments", "Specular file location", "Off-specular file location", "2D Map location"])
                for i in range(len(self.samplelist)):
                    writer.writerow([self.samplelist[i].sampleID, self.samplelist[i].date, self.samplelist[i].layers, self.samplelist[i].materials, self.samplelist[i].magPower, self.samplelist[i].growthTimes, self.samplelist[i].gasses, self.samplelist[i].backgroundpressure, self.samplelist[i].period, self.samplelist[i].gamma, self.samplelist[i].bias, self.samplelist[i].comments, self.samplelist[i].specularpath, self.samplelist[i].offspecularpath, self.samplelist[i].mappath])
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()



    def sampledatabase(self, widget):
     #  print(self.samplelist[0].sampleID.get_text())
        dialog = SampleDatabase(self, self.samplelist)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            index = dialog.get_sampleID()
            specularpath = self.samplelist[index].specularpath
            if specularpath is not '':
                X, Y = [], []
                for line in open(specularpath, 'r'):
                    values = [float(s) for s in line.split()]
                    X.append(values[0])
                    Y.append(values[1])
                f = plt.figure()
                self.f = plt.figure()
                self.canvas = FigureCanvas(self.f)  # a Gtk.DrawingArea

                for grandkid in self.vbox_right.get_children():
                    self.vbox_right.remove(grandkid)
                self.ax = self.f.add_subplot(111)
                plt.plot(X, Y, label=self.samplelist[index].sampleID)
                plt.xlabel('Grazing incidence angle θ (°)')
                plt.ylabel('Intensity (arb. u)')
                plt.legend()
                print(X)
                self.vbox_right.add(self.canvas)
                self.vbox_right.show_all()

                plt.yscale('log')
                self.canvas.set_size_request(1200, 800)


            #

        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        dialog.destroy()


class DialogExample(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(            self,
            "About",
            parent,
            0,
            (
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK,
            ),
        )


        self.set_default_size(150, 100)

        copylabel = Gtk.Label("Copyright © 2020, Sjoerd Broekhuijsen")
        label = Gtk.Label("KARIN is licensed under the GPLv3 license")
        label.set_justify(Gtk.Justification.CENTER)

        box = self.get_content_area()
        box.add(label)
        box.add(copylabel)

        self.show_all()

#sample1 = Sample("IFM20020", 200612, "1E-7")
#result = run_simulation()
#ba.plot_simulation_result(result, intensity_min=0.1)


window = MainWindow()
#window.maximize()
window.connect("delete-event", Gtk.main_quit) #connect close button to delete-event signal
window.show_all() #display windows
Gtk.main() #main loop, keeps window open

