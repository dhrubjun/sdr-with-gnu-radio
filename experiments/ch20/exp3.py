#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Adaptive LMS Equalization
# Author: Dhrubjun
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
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
import numpy as np
import sip
import threading



class exp3(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Adaptive LMS Equalization", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Adaptive LMS Equalization")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp3")

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
        self.a = a = 0.70710678
        self.symbol_rate = symbol_rate = 1000
        self.samp_rate = samp_rate = 32000
        self.qpsk_points = qpsk_points = [a-1j*a, -a+1j*a, -a-1j*a, a+1j*a]
        self.payload_indices = payload_indices = list(np.random.default_rng(20).integers(0, 4, 256))
        self.training_symbols = training_symbols = [a+1j*a, a-1j*a, -a+1j*a, -a-1j*a, a-1j*a, -a-1j*a, a+1j*a, -a+1j*a]
        self.sps = sps = int(samp_rate / symbol_rate)
        self.span = span = 8
        self.qpsk = qpsk = digital.constellation_rect([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j], [0, 1, 2, 3],
        4, 2, 2, 1, 1).base()
        self.payload_symbols = payload_symbols = [qpsk_points[i] for i in payload_indices]
        self.ntaps = ntaps = span * sps + 1
        self.lms = lms = digital.adaptive_algorithm_lms( qpsk, 0.005).base()
        self.frame_symbols = frame_symbols = training_symbols + payload_symbols
        self.echo_gain = echo_gain = 0.5
        self.echo_delay = echo_delay = 32
        self.alpha = alpha = 0.35

        ##################################################
        # Blocks
        ##################################################

        self._echo_gain_range = qtgui.Range(0, 1, 0.05, 0.5, 200)
        self._echo_gain_win = qtgui.RangeWidget(self._echo_gain_range, self.set_echo_gain, "Echo Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._echo_gain_win)
        self._echo_delay_range = qtgui.Range(0, 32, 1, 32, 200)
        self._echo_delay_win = qtgui.RangeWidget(self._echo_delay_range, self.set_echo_delay, "Echo Delay (samples)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._echo_delay_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            'Adaptive LMS Equalization (Threshold = 0.5)', #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['Before Equalization', 'After LMS Equalization', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccf(sps, firdes.root_raised_cosine(sps, samp_rate, symbol_rate, alpha, ntaps))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(1, samp_rate, symbol_rate, alpha, ntaps))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_linear_equalizer_0 = digital.linear_equalizer(5, 1, lms, True, training_symbols, 'corr_est')
        self.digital_corr_est_cc_0 = digital.corr_est_cc(training_symbols, 1, 1, 0.5, digital.THRESHOLD_ABSOLUTE)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(frame_symbols, True, 1, [])
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(echo_gain)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, sps)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, echo_delay)
        self.blocks_add_xx_0 = blocks.add_vcc(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.digital_linear_equalizer_0, 0))
        self.connect((self.digital_linear_equalizer_0, 0), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_throttle2_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp3")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_a(self):
        return self.a

    def set_a(self, a):
        self.a = a
        self.set_qpsk_points([self.a-1j*self.a, -self.a+1j*self.a, -self.a-1j*self.a, self.a+1j*self.a])
        self.set_training_symbols([self.a+1j*self.a, self.a-1j*self.a, -self.a+1j*self.a, -self.a-1j*self.a, self.a-1j*self.a, -self.a-1j*self.a, self.a+1j*self.a, -self.a+1j*self.a])

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

    def get_qpsk_points(self):
        return self.qpsk_points

    def set_qpsk_points(self, qpsk_points):
        self.qpsk_points = qpsk_points
        self.set_payload_symbols([self.qpsk_points[i] for i in self.payload_indices])

    def get_payload_indices(self):
        return self.payload_indices

    def set_payload_indices(self, payload_indices):
        self.payload_indices = payload_indices
        self.set_payload_symbols([self.qpsk_points[i] for i in self.payload_indices])

    def get_training_symbols(self):
        return self.training_symbols

    def set_training_symbols(self, training_symbols):
        self.training_symbols = training_symbols
        self.set_frame_symbols(self.training_symbols + self.payload_symbols)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_ntaps(self.span * self.sps + 1)
        self.blocks_keep_one_in_n_0.set_n(self.sps)
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))

    def get_span(self):
        return self.span

    def set_span(self, span):
        self.span = span
        self.set_ntaps(self.span * self.sps + 1)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_payload_symbols(self):
        return self.payload_symbols

    def set_payload_symbols(self, payload_symbols):
        self.payload_symbols = payload_symbols
        self.set_frame_symbols(self.training_symbols + self.payload_symbols)

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))

    def get_lms(self):
        return self.lms

    def set_lms(self, lms):
        self.lms = lms

    def get_frame_symbols(self):
        return self.frame_symbols

    def set_frame_symbols(self, frame_symbols):
        self.frame_symbols = frame_symbols
        self.blocks_vector_source_x_0.set_data(self.frame_symbols, [])

    def get_echo_gain(self):
        return self.echo_gain

    def set_echo_gain(self, echo_gain):
        self.echo_gain = echo_gain
        self.blocks_multiply_const_vxx_0.set_k(self.echo_gain)

    def get_echo_delay(self):
        return self.echo_delay

    def set_echo_delay(self, echo_delay):
        self.echo_delay = echo_delay
        self.blocks_delay_0.set_dly(int(self.echo_delay))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))




def main(top_block_cls=exp3, options=None):

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
