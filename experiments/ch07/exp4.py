#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Noise Power vs Bandwidth
# Author: Dhrubjun
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
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



class exp4(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Noise Power vs Bandwidth", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Noise Power vs Bandwidth")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp4")

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
        self.cutoff = cutoff = 1000
        self.avg_len = avg_len = 10000

        ##################################################
        # Blocks
        ##################################################

        self._cutoff_range = qtgui.Range(500, 4000, 500, 1000, 200)
        self._cutoff_win = qtgui.RangeWidget(self._cutoff_range, self.set_cutoff, "LPF Cutoff Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._cutoff_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                cutoff,
                500,
                window.WIN_HAMMING,
                6.76))
        self.input_noise_power = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.input_noise_power.set_update_time(0.10)
        self.input_noise_power.set_title('Input Noise Power')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.input_noise_power.set_min(i, -1)
            self.input_noise_power.set_max(i, 1)
            self.input_noise_power.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.input_noise_power.set_label(i, "Data {0}".format(i))
            else:
                self.input_noise_power.set_label(i, labels[i])
            self.input_noise_power.set_unit(i, units[i])
            self.input_noise_power.set_factor(i, factor[i])

        self.input_noise_power.enable_autoscale(False)
        self._input_noise_power_win = sip.wrapinstance(self.input_noise_power.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._input_noise_power_win)
        self.filtered_noise_power = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.filtered_noise_power.set_update_time(0.10)
        self.filtered_noise_power.set_title('Filtered Noise Power')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.filtered_noise_power.set_min(i, -1)
            self.filtered_noise_power.set_max(i, 1)
            self.filtered_noise_power.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.filtered_noise_power.set_label(i, "Data {0}".format(i))
            else:
                self.filtered_noise_power.set_label(i, labels[i])
            self.filtered_noise_power.set_unit(i, units[i])
            self.filtered_noise_power.set_factor(i, factor[i])

        self.filtered_noise_power.enable_autoscale(False)
        self._filtered_noise_power_win = sip.wrapinstance(self.filtered_noise_power.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._filtered_noise_power_win)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(avg_len, (1/avg_len), 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(avg_len, (1/avg_len), 4000, 1)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.filtered_noise_power, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.input_noise_power, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_throttle2_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "exp4")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, 500, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, 500, window.WIN_HAMMING, 6.76))

    def get_avg_len(self):
        return self.avg_len

    def set_avg_len(self, avg_len):
        self.avg_len = avg_len
        self.blocks_moving_average_xx_0.set_length_and_scale(self.avg_len, (1/self.avg_len))
        self.blocks_moving_average_xx_0_0.set_length_and_scale(self.avg_len, (1/self.avg_len))




def main(top_block_cls=exp4, options=None):

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
