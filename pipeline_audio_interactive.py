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

        window = AudioWindow(
            pipeline=self.pipeline,
            audiosrc=self.audiotestsrc
        )

        window.connect('delete-event', Gtk.main_quit)
        window.show_all()


class AudioWindow(Gtk.Window):

    def __init__(self, pipeline, audiosrc):
        self.pipeline = pipeline
        self.audiosrc = audiosrc

        Gtk.Window.__init__(self, title='Test Audio Player')
        self.set_border_width(5)

        btns = {
            'Play': self.on_play,
            'Stop': self.on_stop,
            'Quit': self.on_quit,
            'Vol up': self.inc_vol,
            'Vol down': self.dec_vol,
        }

        self.btn_box = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        self.btn_box.set_spacing(5)

        for label, callback in btns.items():
            button = Gtk.Button(label=label)
            button.connect('clicked', callback)
            self.btn_box.add(button)

        self.add(self.btn_box)

    def on_play(self, button):
        print('%s button clicked' % button.get_label())
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_stop(self, button):
        print('%s button clicked' % button.get_label())
        self.pipeline.set_state(Gst.State.READY)

    def on_quit(self, button):
        print('%s button clicked' % button.get_label())
        Gtk.main_quit()

    def inc_vol(self, button):
        vol = self.audiosrc.get_property('volume')

        if vol < 1:
            print('Volume up')
            vol += .1
            self.audiosrc.set_property('volume', vol)
        else:
            print('Volume is alrady max')


    def dec_vol(self, button):
        vol = self.audiosrc.get_property('volume')

        if vol > .1:
            print('Volume down')
            vol -= .1
            self.audiosrc.set_property('volume', vol)
        else:
            print('Volume is alrady min')

start = Main()
Gtk.main()
