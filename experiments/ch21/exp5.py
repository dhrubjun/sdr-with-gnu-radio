#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Ordinary PLL Applied to QPSK
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import math
import numpy as np
import sip
import threading



class exp5(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Ordinary PLL Applied to QPSK", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Ordinary PLL Applied to QPSK")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp5")

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
        self.samp_rate = samp_rate = 32000
        self.phase_offset = phase_offset = 0
        self.loop_bw = loop_bw = math.pi/500

        ##################################################
        # Blocks
        ##################################################

        self._phase_offset_range = qtgui.Range(-180, 180, 5, 0, 200)
        self._phase_offset_win = qtgui.RangeWidget(self._phase_offset_range, self.set_phase_offset, "Carrier Phase Offset (deg)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._phase_offset_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            'Ordinary PLL Applied to QPSK', #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-5), 5)
        self.qtgui_const_sink_x_0.set_x_axis((-5), 5)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['Phase-Offset QPSK', 'Ordinary PLL Output', '', '', '',
            '', '', '', '', '']
        widths = [5, 5, 1, 1, 1,
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
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bf([-1,1], 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf([-1,1], 1)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(np.exp(1j*math.radians(phase_offset)))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_random_source_x_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_pll_refout_cc_0 = analog.pll_refout_cc(loop_bw, (2*math.pi*2000/samp_rate), (-2*math.pi*2000/samp_rate))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pll_refout_cc_0, 0), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.analog_random_source_x_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.analog_pll_refout_cc_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_float_to_complex_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp5")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_pll_refout_cc_0.set_max_freq((2*math.pi*2000/self.samp_rate))
        self.analog_pll_refout_cc_0.set_min_freq((-2*math.pi*2000/self.samp_rate))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_phase_offset(self):
        return self.phase_offset

    def set_phase_offset(self, phase_offset):
        self.phase_offset = phase_offset
        self.blocks_multiply_const_vxx_0.set_k(np.exp(1j*math.radians(self.phase_offset)))

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw
        self.analog_pll_refout_cc_0.set_loop_bandwidth(self.loop_bw)




def main(top_block_cls=exp5, options=None):

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
