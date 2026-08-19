#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Constructing an Eye Diagram
# Author: Dhrubjun
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
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
import threading



class exp9(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Constructing an Eye Diagram", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Constructing an Eye Diagram")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp9")

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
        self.alpha = alpha = 0.35

        ##################################################
        # Blocks
        ##################################################

        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, firdes.root_raised_cosine(sps, samp_rate, symbol_rate, alpha, ntaps))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, firdes.root_raised_cosine(1, samp_rate, symbol_rate, alpha, ntaps))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf([-1,1], 1)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'ch18-eye-05.dat', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 0.5, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_throttle2_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp9")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_sps(int(self.samp_rate / self.symbol_rate))
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(int(self.samp_rate / self.symbol_rate))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_ntaps(self.span * self.sps + 1)
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))

    def get_span(self):
        return self.span

    def set_span(self, span):
        self.span = span
        self.set_ntaps(self.span * self.sps + 1)

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))




def main(top_block_cls=exp9, options=None):

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
