import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):
    """Recover 24-bit payload after frame_start tag."""

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="Payload Decoder",
            in_sig=[np.uint8],
            out_sig=None
        )

        self.payload_length = 24
        self.collecting = False
        self.bits = []

        # Print only the first five recovered payloads.
        self.print_count = 0
        self.max_prints = 5

    def work(self, input_items, output_items):
        data = input_items[0]

        # Find frame_start tags in the current input window.
        tags = self.get_tags_in_window(
            0,
            0,
            len(data),
            pmt.intern("frame_start")
        )

        # Convert absolute tag offsets to positions
        # inside the current work() buffer.
        tag_positions = {
            int(tag.offset - self.nitems_read(0))
            for tag in tags
        }

        for i, sample in enumerate(data):

            # A frame_start tag marks the beginning
            # of a new 24-bit payload.
            if i in tag_positions:
                self.collecting = True
                self.bits = []

            # Collect payload bits.
            if self.collecting:
                self.bits.append(int(sample) & 1)

                # Once 24 payload bits have been collected,
                # convert them into three ASCII characters.
                if len(self.bits) == self.payload_length:
                    payload_bits = self.bits[:]

                    chars = []

                    for k in range(0, 24, 8):
                        byte_bits = payload_bits[k:k + 8]

                        bit_string = ''.join(
                            str(bit) for bit in byte_bits
                        )

                        value = int(bit_string, 2)
                        chars.append(chr(value))

                    message = ''.join(chars)

                    # Print only the first five recovered payloads.
                    if self.print_count < self.max_prints:
                        print(
                            "Recovered payload bits:",
                            ''.join(str(b) for b in payload_bits)
                        )
                        print(
                            "Recovered payload:",
                            message
                        )

                        self.print_count += 1

                    self.collecting = False
                    self.bits = []

        return len(data)