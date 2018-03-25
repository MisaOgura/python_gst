#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')

from gi.repository import GObject, Gst, GstBase, Gtk, GObject


class Main:

    def __init__(self):
        Gst.init(None)

        self.pipeline = Gst.Pipeline('mypipeline')

        self.audiotestsrc = Gst.ElementFactory.make('audiotestsrc', 'audio')
        self.pipeline.add(self.audiotestsrc)

        self.sink = Gst.ElementFactory.make('osxaudiosink', 'sink')
        self.pipeline.add(self.sink)

        self.audiotestsrc.link(self.sink)

        window = AudioWindow(pipeline=self.pipeline)
        window.connect('delete-event', Gtk.main_quit)
        window.show_all()


class AudioWindow(Gtk.Window):

    def __init__(self, pipeline):
        self.pipeline = pipeline
        Gtk.Window.__init__(self, title='Test Audio Player')

        buttons = {
            'Play': self.on_play,
            'Stop': self.on_stop,
            'Quit': self.on_quit
        }

        self.box = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)

        for label, callback in buttons.items():
            button = Gtk.Button(label=label)
            button.connect('clicked', callback)
            self.box.add(button)

        self.add(self.box)

    def on_play(self, button):
        print('%s button clicked' % button.get_label())
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_stop(self, button):
        print('%s button clicked' % button.get_label())
        self.pipeline.set_state(Gst.State.READY)

    def on_quit(self, button):
        print('%s button clicked' % button.get_label())
        Gtk.main_quit()


start = Main()
Gtk.main()
