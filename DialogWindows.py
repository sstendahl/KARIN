import gi
import csv
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from samples import Sample

class NewSample(Gtk.Dialog):

    def __init__(self, parent):
        # Layout
        Gtk.Dialog.__init__(self, "New sample", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        grid = Gtk.Grid()

       # grid = Gtk.Grid()
       # self.add(grid)
        self.set_border_width(10)
       # self.set_size_request(200, 100)
        self.sample = ""
        self.set_default_size(150, 100)
        #self.connect("response", self.on_response)



        # Layout
        #Username
        self.sampleID = Gtk.Entry()
        self.sampleID.set_text("Sample ID")
        sampleIDlabel = Gtk.Label("Sample ID   ")
        sampleIDlabel.set_alignment(1, 0.5)
        #Password
        self.date = Gtk.Entry()
        self.date.set_text("2020-01-01")
        dateLabel = Gtk.Label("Date   ")
        dateLabel.set_alignment(1, 0.5)

        self.layers = Gtk.Entry()
        self.layers.set_text("50")
        layersLabel = Gtk.Label("Layers   ")
        layersLabel.set_alignment(1, 0.5)

        self.period = Gtk.Entry()
        self.period.set_text("")
        periodLabel = Gtk.Label("Period   ")
        periodLabel.set_alignment(1, 0.5)

        self.bias = Gtk.Entry()
        self.bias.set_text("")
        biasLabel = Gtk.Label("Bias   ")
        biasLabel.set_alignment(1, 0.5)

        self.gasses = Gtk.Entry()
        self.gasses.set_text("Ar: 3 mTorr")
        gassesLabel = Gtk.Label("Gasses   ")
        gassesLabel.set_alignment(1, 0.5)

        self.magPower = Gtk.Entry()
        self.magPower.set_text("")
        magPowerLabel = Gtk.Label("Magnetron Powers   ")
        magPowerLabel.set_alignment(1, 0.5)

        self.growthTimes = Gtk.Entry()
        self.growthTimes.set_text("")
        growthTimesLabel = Gtk.Label("Growth Times   ")
        growthTimesLabel.set_alignment(1, 0.5)

        self.comments = Gtk.Entry()
        self.comments.set_text("")
        commentsLabel = Gtk.Label("Comments   ")
        commentsLabel.set_alignment(1, 0.5)

        self.materials = Gtk.Entry()
        self.materials.set_text("")
        materialsLabel = Gtk.Label("Materials   ")
        materialsLabel.set_alignment(1, 0.5)

        self.gamma = Gtk.Entry()
        self.gamma.set_text("")
        gammaLabel = Gtk.Label("Gamma ratio   ")
        gammaLabel.set_alignment(1, 0.5)

        open_icon = Gio.ThemedIcon(name="document-open-symbolic") #document-open-symbolic
        image = Gtk.Image.new_from_gicon(open_icon, Gtk.IconSize.BUTTON)
        self.specfolder = Gtk.Button()
        self.specfolder.add(image)

        self.specularpath = Gtk.Entry()
        self.specularpath.set_text("")
        specularpathLabel = Gtk.Label("      Path to specular file   ")
        specularpathLabel.set_alignment(1, 0.5)
        self.specfolder = Gtk.Button()
        image = Gtk.Image.new_from_gicon(open_icon, Gtk.IconSize.BUTTON)
        self.specfolder.add(image)
        self.specfolder.connect("clicked", self.chooseSpecfolder)


        self.offspecularpath = Gtk.Entry()
        self.offspecularpath.set_text("")
        offspecularpathLabel = Gtk.Label("      Path to off-specular file   ")
        offspecularpathLabel.set_alignment(1, 0.5)
        self.offspecfolder = Gtk.Button()
        image = Gtk.Image.new_from_gicon(open_icon, Gtk.IconSize.BUTTON)
        self.offspecfolder.add(image)
        self.offspecfolder.connect("clicked", self.chooseOffSpecfolder)


        self.mappath = Gtk.Entry()
        self.mappath.set_text("")
        mapPathLabel = Gtk.Label("      Path to 2D Map   ")
        mapPathLabel.set_alignment(1, 0.5)
        self.mapFolder = Gtk.Button()
        image = Gtk.Image.new_from_gicon(open_icon, Gtk.IconSize.BUTTON)
        self.mapFolder.add(image)
        self.mapFolder.connect("clicked", self.chooseMapfolder)

        self.backgroundPressure = Gtk.Entry()
        self.backgroundPressure.set_text("")
        backgroundPressureLabel = Gtk.Label("Background Pressure   ")
        backgroundPressureLabel.set_alignment(1, 0.5)


        self.connect("response", self.on_response, self.sampleID, self.date, self.layers, self.materials, self.magPower, self.growthTimes, self.gasses, self.backgroundPressure, self.period, self.gamma, self.bias, self.comments, self.specularpath, self.offspecularpath, self.mappath)

        box = self.get_content_area()


        grid.attach(self.sampleID,2,1,1,1)
        grid.attach(sampleIDlabel,1,1,1,1)
        grid.attach(self.date,2,2,1,1)
        grid.attach(dateLabel,1,2,1,1)
        grid.attach(self.layers,2,3,1,1)
        grid.attach(layersLabel,1,3,1,1)
        grid.attach(self.materials,2,4,1,1)
        grid.attach(materialsLabel,1,4,1,1)
        grid.attach(self.magPower,2,5,1,1)
        grid.attach(magPowerLabel,1,5,1,1)
        grid.attach(self.growthTimes,2,6,1,1)
        grid.attach(growthTimesLabel,1,6,1,1)
        grid.attach(self.gasses,2,7,1,1)
        grid.attach(gassesLabel,1,7,1,1)
        grid.attach(self.backgroundPressure,2,8,1,1)
        grid.attach(backgroundPressureLabel,1,8,1,1)
        grid.attach(self.period,2,9,1,1)
        grid.attach(periodLabel,1,9,1,1)
        grid.attach(self.gamma,2,10,1,1)
        grid.attach(gammaLabel,1,10,1,1)
        grid.attach(self.bias,2,11,1,1)
        grid.attach(biasLabel,1,11,1,1)
        grid.attach(self.comments,2,12,1,1)
        grid.attach(commentsLabel,1,12,1,1)
        grid.attach(self.comments,2,12,1,1)
        grid.attach(commentsLabel,1,12,1,1)
        grid.attach(self.specularpath,4,1,1,1)
        grid.attach(specularpathLabel,3,1,1,1)
        grid.attach(self.specfolder,5,1,1,1)
        grid.attach(self.offspecularpath,4,2,1,1)
        grid.attach(offspecularpathLabel,3,2,1,1)
        grid.attach(self.offspecfolder,5,2,1,1)
        grid.attach(self.mappath,4,3,1,1)
        grid.attach(mapPathLabel,3,3,1,1)
        grid.attach(self.mapFolder,5,3,1,1)

        box.add(grid)
        self.show_all()



    def on_response(self, widget, response_id, sampleID, date, layers, materials, magPower, growthTimes, gasses, backgroundPressure, period, gamma, bias, comments, specpath, offspecpath, mappath):
        self.added_sample = Sample(sampleID.get_text(), date.get_text(), layers.get_text(), materials.get_text(), magPower.get_text(), growthTimes.get_text(), gasses.get_text(), backgroundPressure.get_text(), period.get_text(), gamma.get_text(), bias.get_text(), comments.get_text(), specpath.get_text(), offspecpath.get_text(), mappath.get_text())

    def get_result(self):
        return self.added_sample
    def chooseMapfolder(self, widget):
        dialog = Gtk.FileChooserDialog("Select your 2D map", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                       "Ok", Gtk.ResponseType.OK))
        response = dialog.run()
        self.mappath.set_text(dialog.get_filename())
        dialog.destroy()

    def chooseSpecfolder(self, widget):
        dialog = Gtk.FileChooserDialog("Select your 2D map", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                       "Ok", Gtk.ResponseType.OK))
        response = dialog.run()
        self.specularpath.set_text(dialog.get_filename())
        dialog.destroy()

    def chooseOffSpecfolder(self, widget):
        dialog = Gtk.FileChooserDialog("Select your Off Specular File", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                       "Ok", Gtk.ResponseType.OK))
        response = dialog.run()
        self.offspecularpath.set_text(dialog.get_filename())
        dialog.destroy()





class SampleDatabase(Gtk.Dialog):
        def __init__(self, parent, samplelist):
            Gtk.Dialog.__init__(self, "Sample Database", parent, 0,
                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
            self.samplelist = samplelist
            print(samplelist[0].bias)
            self.result = ""
            self.set_default_size(150, 500)
            print(parent)
            # Convert data to ListStore (lists that TreeViews can display)
            samples_list_store = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str, str, str)
            row = []
            print(str(len(samplelist)))
            for i in range(len(samplelist)):
                column = []
                column.append(samplelist[i].sampleID)
                column.append(samplelist[i].date)
                column.append(samplelist[i].layers)
                column.append(samplelist[i].materials)
                column.append(samplelist[i].magPower)
                column.append(samplelist[i].growthTimes)
                column.append(samplelist[i].gasses)
                column.append(samplelist[i].backgroundpressure)
                column.append(samplelist[i].period)
                column.append(samplelist[i].gamma)
                column.append(samplelist[i].bias)
                column.append(samplelist[i].comments)
                row.append(column)

            for item in row:
                samples_list_store.append(list(item)),
                print(i)

            # TreeView is the item that is displayed
            sample_tree_view = Gtk.TreeView(samples_list_store)

            for i, col_title in enumerate(["Sample ID", "Date", "Amount of Layers", "Materials", "Magnetron Powers", "Growth Times", "Inlet gasses", "Background Pressure", "Period", "Gamma ratio", "Bias", "Comments"]):
                # Render means how to draw the data
                renderer = Gtk.CellRendererText()

                # Create columns (text is column number)
                column = Gtk.TreeViewColumn(col_title, renderer, text=i)
                column.set_sort_column_id(i)
                # Add column to TreeView
                sample_tree_view.append_column(column)


                # Handle selection
            selected_row = sample_tree_view.get_selection()
            selected_row.connect("changed", self.set_sampleID)
            # Add TreeView to main layour
            self.scroll = Gtk.ScrolledWindow()

            self.scroll.add(sample_tree_view)
            self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

            self.box = self.get_content_area()
            self.box.pack_start(self.scroll, True, True, 0)

           # self.add_button = Gtk.Button(label="Add Sample")
         #   self.second_button.connect("clicked")
            #self.box.pack_start(self.add_button, True, True, 0)
            self.remove_button = Gtk.Button(label="Remove Sample")
            self.remove_button.connect("clicked", self.removesample, selected_row)
            self.box.pack_start(self.remove_button, True, True, 0)

            self.show_all()

            #        for row in people_list_store:
            #            print(row[:])
            #            print(row[2])

            # user selected row

        def set_sampleID(self, selection):
            model, iter = selection.get_selected()
            if iter is not None:
                #rowcontents = model[treeiter][0:3]  # for a 4 column treeview
                rownumobj = model.get_path(iter)
                self.rownum = int(rownumobj.to_string())
                print(self.rownum)
                sampleID = model[iter][0]
                print("SampleID: " + str(self.rownum))
                return self.rownum

        def get_sampleID(self):
            return self.rownum

        def removesample(self, widget, selection):
            model, row = selection.get_selected()
            #for i in range(len(self.samplelist)):
            for item in self.samplelist:
                print(item.sampleID)
                if item.sampleID == model[row][0]:
                    self.samplelist.remove(item)

            with open('samplelist.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Sample ID", "Date", "Amount of Layers", "Materials", "Magnetron Powers", "Growth Times", "Inlet gasses", "Background Pressure", "Period", "Gamma ratio", "Bias", "Comments", "Specular file location", "Off-specular file location", "2D Map location"])
                for i in range(len(self.samplelist)):
                    writer.writerow([self.samplelist[i].sampleID, self.samplelist[i].date, self.samplelist[i].layers, self.samplelist[i].materials, self.samplelist[i].magPower, self.samplelist[i].growthTimes, self.samplelist[i].gasses, self.samplelist[i].backgroundpressure, self.samplelist[i].period, self.samplelist[i].gamma, self.samplelist[i].bias, self.samplelist[i].comments, self.samplelist[i].specularpath, self.samplelist[i].offspecularpath, self.samplelist[i].mappath])
            model, paths = selection.get_selected_rows()
            for path in paths:
                iter = model.get_iter(path)
                model.remove(iter)



