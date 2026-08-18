import numpy as np
from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='4-PAM Hard Decision',
            in_sig=[np.float32],
            out_sig=[np.uint8]
        )

    def work(self, input_items, output_items):
        x = input_items[0]
        y = output_items[0]

        n = min(len(x), len(y))

        for i in range(n):
            if x[i] < -2:
                y[i] = 0
            elif x[i] < 0:
                y[i] = 1
            elif x[i] < 2:
                y[i] = 2
            else:
                y[i] = 3

        return n