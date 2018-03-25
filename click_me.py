import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Click Me Window')

        self.button = Gtk.Button(label='Click here!')
        print(dir(self.button)) # to see available properties of an widget

        self.button.connect('clicked', self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print(widget)
        print('Thanks for clicking :)')

win = MyWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
