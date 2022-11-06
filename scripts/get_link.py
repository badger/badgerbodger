""" MIT License

Copyright (c) 2022 Krishna Prajapati - @KrisPrajapati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. """

import qrcode
from lib import convert


# Generate QR code
def generate_qr_code():
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=3, border=3,)
    qr.add_data(f"https://github.co/badger2040")
    png = qr.make_image()
    pngfilename = f"generated/gh_qrcode.png"
    png.save(pngfilename)
    convert.convert(pngfilename)

generate_qr_code()
