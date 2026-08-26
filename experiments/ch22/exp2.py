#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Early-Late Timing Error Detector
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
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
import math
import sip
import threading



class exp2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Early-Late Timing Error Detector", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Early-Late Timing Error Detector")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp2")

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
        self.symbol_rate = symbol_rate = 4000
        self.samp_rate = samp_rate = 32000
        self.sps = sps = int(samp_rate / symbol_rate)
        self.span = span = 8
        self.timing_offset = timing_offset = 0
        self.ntaps = ntaps = span * sps + 1
        self.delta = delta = 1
        self.base_delay = base_delay = sps
        self.alpha = alpha = 0.35

        ##################################################
        # Blocks
        ##################################################

        self._timing_offset_range = qtgui.Range(-3, 3, 1, 0, 200)
        self._timing_offset_win = qtgui.RangeWidget(self._timing_offset_range, self.set_timing_offset, "Assumed Timing Offset (samples)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._timing_offset_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title('Average Timing Error')

        labels = ['Error', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_eye_sink_x_0 = qtgui.eye_sink_f(
            1024, #size
            samp_rate, #samp_rate
            1, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0.set_update_time(0.10)
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(sps)
        self.qtgui_eye_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_eye_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_0.enable_tags(True)
        self.qtgui_eye_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0.enable_grid(False)
        self.qtgui_eye_sink_x_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0.enable_control_panel(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_eye_sink_x_0.set_line_label(i, "Eye[Data {0}]".format(i))
            else:
                self.qtgui_eye_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_eye_sink_x_0_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, firdes.root_raised_cosine(sps, samp_rate, symbol_rate, alpha, ntaps))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, firdes.root_raised_cosine(1, samp_rate, symbol_rate, alpha, ntaps))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_vector_source_x_0 = blocks.vector_source_f([1, -1, 1, -1, 1, -1, 1, -1], True, 1, [])
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(32, (1/32), 4000, 1)
        self.blocks_keep_one_in_n_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, sps)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, sps)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, (base_delay + timing_offset + delta))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, (base_delay + timing_offset - delta))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_delay_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_keep_one_in_n_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_eye_sink_x_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_throttle2_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp2")
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
        self.qtgui_eye_sink_x_0.set_samp_rate(self.samp_rate)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_base_delay(self.sps)
        self.set_ntaps(self.span * self.sps + 1)
        self.blocks_keep_one_in_n_0_0.set_n(self.sps)
        self.blocks_keep_one_in_n_0_0_0.set_n(self.sps)
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(self.sps)

    def get_span(self):
        return self.span

    def set_span(self, span):
        self.span = span
        self.set_ntaps(self.span * self.sps + 1)

    def get_timing_offset(self):
        return self.timing_offset

    def set_timing_offset(self, timing_offset):
        self.timing_offset = timing_offset
        self.blocks_delay_0.set_dly(int((self.base_delay + self.timing_offset - self.delta)))
        self.blocks_delay_0_0.set_dly(int((self.base_delay + self.timing_offset + self.delta)))

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))

    def get_delta(self):
        return self.delta

    def set_delta(self, delta):
        self.delta = delta
        self.blocks_delay_0.set_dly(int((self.base_delay + self.timing_offset - self.delta)))
        self.blocks_delay_0_0.set_dly(int((self.base_delay + self.timing_offset + self.delta)))

    def get_base_delay(self):
        return self.base_delay

    def set_base_delay(self, base_delay):
        self.base_delay = base_delay
        self.blocks_delay_0.set_dly(int((self.base_delay + self.timing_offset - self.delta)))
        self.blocks_delay_0_0.set_dly(int((self.base_delay + self.timing_offset + self.delta)))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))
        self.interp_fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.symbol_rate, self.alpha, self.ntaps))




def main(top_block_cls=exp2, options=None):

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
