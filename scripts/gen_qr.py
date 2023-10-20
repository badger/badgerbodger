import qrcode

# Generate QR code
def generate_qr_code():
    qr = qrcode.QRCode(version=1, box_size=3, border=3)
    qr.add_data(f"007aBc^Mona^Lisa^GitHub^^Octocat^@mona^")
    png = qr.make_image()
    pngfilename = f"generated/gh_qrcode.png"
    png.save(pngfilename)

generate_qr_code()
