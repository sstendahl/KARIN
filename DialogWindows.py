import gi
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
       # self.set_border_width(10)
       # self.set_size_request(200, 100)
        self.sample = ""
        self.set_default_size(150, 100)
        #self.connect("response", self.on_response)



        # Layout
        #Username
        self.sampleID = Gtk.Entry()
        self.sampleID.set_text("Sample ID")
        sampleIDlabel = Gtk.Label("Sample ID   ")
        #Password
        self.date = Gtk.Entry()
        self.date.set_text("2020-01-01")
        dateLabel = Gtk.Label("Date   ")

        self.backgroundPressure = Gtk.Entry()
        self.backgroundPressure.set_text("1E-7")
        backgroundPressureLabel = Gtk.Label("Background Pressure   ")

        self.connect("response", self.on_response, self.sampleID, self.date, self.backgroundPressure)

        box = self.get_content_area()



        grid.attach(self.sampleID,2,1,1,1)
        grid.attach(sampleIDlabel,1,1,1,1)
        grid.attach(self.date,2,2,1,1)
        grid.attach(dateLabel,1,2,1,1)
        grid.attach(self.backgroundPressure,2,3,1,1)
        grid.attach(backgroundPressureLabel,1,3,1,1)
        box.add(grid)
        self.show_all()



    def on_response(self, widget, response_id, sampleID, date, backgroundPressure):
        self.added_sample = Sample(sampleID.get_text(), date.get_text(), backgroundPressure.get_text())

    def get_result(self):
        return self.added_sample



class SampleDatabase(Gtk.Dialog):
        def __init__(self, parent, samplelist):
            Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
            self.samplelist = samplelist
            self.result = ""
            self.set_default_size(150, 100)
            print(parent)
            # Convert data to ListStore (lists that TreeViews can display)
            samples_list_store = Gtk.ListStore(str, str, str)
            row = []
            print(str(len(samplelist)))
            for i in range(len(samplelist)):
                column = []
                column.append(samplelist[i].sampleID)
                column.append(samplelist[i].sampleDate)
                column.append(samplelist[i].backgroundpressure)
                row.append(column)

            for item in row:
                samples_list_store.append(list(item)),
                print(i)

            # TreeView is the item that is displayed
            people_tree_view = Gtk.TreeView(samples_list_store)

            for i, col_title in enumerate(["Sample ID", "Date", "Background Pressure"]):
                # Render means how to draw the data
                renderer = Gtk.CellRendererText()

                # Create columns (text is column number)
                column = Gtk.TreeViewColumn(col_title, renderer, text=i)
                column.set_sort_column_id(i)
                # Add column to TreeView
                people_tree_view.append_column(column)

            # Handle selection
            selected_row = people_tree_view.get_selection()
            selected_row.connect("changed", self.item_selected)
            # Add TreeView to main layour
            box = self.get_content_area()
            box.pack_start(people_tree_view, True, True, 0)
            self.show_all()

            #        for row in people_list_store:
            #            print(row[:])
            #            print(row[2])

            # user selected row

        def item_selected(self, selection):
            model, row = selection.get_selected()
            if row is not None:
                print("Name: " + model[row][0])
                print("Age: " + str(model[row][1]))
                print("Job: " + model[row][2])
                print("")
                print("hmmm")
                print(self.samplelist[0].sampleID)
                print("hi there")
                print(self.samplelist[0])




