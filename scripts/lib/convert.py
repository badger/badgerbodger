#!/usr/bin/env python3
"""

Modified version of examples/badger2040/image_convert/convert.py

Converts images into a format suitable for display on Badger 2040.

Crunches images down to dithered, 1bit colour depth.

Outputs in raw binary format

"""

import io
from PIL import Image, ImageEnhance
from pathlib import Path

class ByteWriter(object):
    bytes_per_line = 16

    def __init__(self, stream, varname):
        self.stream = stream
        self.stream.write('{} =\\\n'.format(varname))
        self.bytecount = 0  # For line breaks

    def _eol(self):
        self.stream.write("'\\\n")

    def _eot(self):
        self.stream.write("'\n")

    def _bol(self):
        self.stream.write("b'")

    # Output a single byte
    def obyte(self, data):
        if not self.bytecount:
            self._bol()
        self.stream.write('\\x{:02x}'.format(data))
        self.bytecount += 1
        self.bytecount %= self.bytes_per_line
        if not self.bytecount:
            self._eol()

    # Output from a sequence
    def odata(self, bytelist):
        for byt in bytelist:
            self.obyte(byt)

    # ensure a correct final line
    def eot(self):  # User force EOL if one hasn't occurred
        if self.bytecount:
            self._eot()
        self.stream.write('\n')


def convert_image(img):
    img = img.resize((105, 105))
    try:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
    except ValueError:
        pass
    img = img.convert("1")  # convert to black and white
    return img


def write_stream(header, footer, ip_stream, op_stream):
    op_stream.write(header)
    op_stream.write('\n')
    data = ip_stream.read()
    bw_data = ByteWriter(op_stream, '_data')
    bw_data.odata(data)
    bw_data.eot()
    op_stream.write(footer)


# create map of images based on input filenames
def convert(input_filename):
    with Image.open(input_filename) as img:
        img = convert_image(img)

        image_name = Path(input_filename).stem

        w, h = img.size

        output_data = [~b & 0xff for b in list(img.tobytes())]
        
        output_filename = Path(input_filename).with_suffix(".bin")
        # print(f"Saving to {output_filename}, {w}x{h}")
        with open(output_filename, "wb") as out:
            out.write(bytearray(output_data))