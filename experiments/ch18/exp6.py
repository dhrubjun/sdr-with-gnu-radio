#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RRC Pulse Shape and Roll-Off
# Author: Dhrubjun
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class exp6(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RRC Pulse Shape and Roll-Off", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RRC Pulse Shape and Roll-Off")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp6")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 1000
        self.samp_rate = samp_rate = 32000
        self.sps = sps = int(samp_rate / symbol_rate)
        self.span = span = 8
        self.ntaps = ntaps = span * sps + 1

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            512, #size
            samp_rate, #samp_rate
            'RRC Pulse Shapes for Different Roll-Off Factors', #name
            3, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(2)
        self.qtgui_time_sink_x_0.set_y_axis(-0.2, 1.5)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['α = 0.10', 'α = 0.25', 'α = 0.50', 'α = 1', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.interp_fir_filter_xxx_0_2 = filter.interp_fir_filter_fff(sps, firdes.root_raised_cosine(sps, samp_rate, symbol_rate, 1, ntaps))
        self.interp_fir_filter_xxx_0_2.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0_1 = filter.interp_fir_filter_fff(sps, firdes.root_raised_cosine(sps, samp_rate, symbol_rate, 0.50, ntaps))
        self.interp_fir_filter_xxx_0_1.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, firdes.root_raised_cosine(sps, samp_rate, symbol_rate, 0.10, ntaps))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_vector_source_x_0 = blocks.vector_source_f((0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0), True, 1, [])
        self.blocks_throttle2_0_2 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0_1 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_throttle2_0_1, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_throttle2_0_2, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_vector_source_x_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.interp_fir_filter_xxx_0_1, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.interp_fir_filter_xxx_0_2, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_1, 0), (self.blocks_throttle2_0_1, 0))
        self.connect((self.interp_fir_filter_xxx_0_2, 0), (self.blocks_throttle2_0_2, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp6")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_sps(int(self.samp_rate / self.symbol_rate))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 0.10, self.ntaps))
        self.interp_fir_filter_xxx_0_1.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 0.50, self.ntaps))
        self.interp_fir_filter_xxx_0_2.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 1, self.ntaps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(int(self.samp_rate / self.symbol_rate))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_2.set_sample_rate(self.samp_rate)
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 0.10, self.ntaps))
        self.interp_fir_filter_xxx_0_1.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 0.50, self.ntaps))
        self.interp_fir_filter_xxx_0_2.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 1, self.ntaps))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_ntaps(self.span * self.sps + 1)
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 0.10, self.ntaps))
        self.interp_fir_filter_xxx_0_1.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 0.50, self.ntaps))
        self.interp_fir_filter_xxx_0_2.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 1, self.ntaps))

    def get_span(self):
        return self.span

    def set_span(self, span):
        self.span = span
        self.set_ntaps(self.span * self.sps + 1)

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 0.10, self.ntaps))
        self.interp_fir_filter_xxx_0_1.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 0.50, self.ntaps))
        self.interp_fir_filter_xxx_0_2.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, 1, self.ntaps))




def main(top_block_cls=exp6, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
