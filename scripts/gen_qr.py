import qrcode

latin= " !\"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"


# Generate QR code
def generate_qr_code():
    qr = qrcode.QRCode(version=1, box_size=3, border=3)

    # loop through the latin string and create a qr code for each character
    # called latin-<character>.png
    for c in latin:
        qr.clear()
        qr.add_data(c)
        png = qr.make_image()
        if c == '\\':
            c = 'backslash'
        elif c == '/':
            c = 'forwardslash'
        elif c == ':':
            c = 'colon'
        elif c == '*':
            c = 'asterisk'
        elif c == '?':
            c = 'questionmark'
        elif c == '"':
            c = 'doublequote'
        elif c == '<':
            c = 'lessthan'
        elif c == '>':
            c = 'greaterthan'
        elif c == '|':
            c = 'pipe'
        elif c == '.':
            c = 'period'
        elif c == ',':
            c = 'comma'
        elif c == ';':
            c = 'semicolon'
        elif c == '[':
            c = 'leftbracket'
        elif c == ']':
            c = 'rightbracket'
        elif c == '{':
            c = 'leftbrace'
        elif c == '}':
            c = 'rightbrace'
        elif c == '~':
            c = 'tilde'
        elif c == '!':
            c = 'exclamation'
        elif c == '@':
            c = 'at'
        elif c == '#':
            c = 'hash'
        elif c == '$':
            c = 'dollar'
        elif c == '%':
            c = 'percent'
        elif c == '^':
            c = 'caret'
        elif c == '&':
            c = 'ampersand'
        elif c == '(':
            c = 'leftparen'
        elif c == ')':
            c = 'rightparen'
        elif c == '-':
            c = 'minus'
        elif c == '_':
            c = 'underscore'
        elif c == '=':
            c = 'equals'
        elif c == '+':
            c = 'plus'
        elif c == '`':
            c = 'backtick'
        elif c == "'":
            c = 'singlequote'
        elif c == ' ':
            c = 'space'
 
        pngfilename = f"generated/latin-{c}.png"
        png.save(pngfilename)

    qr.clear()
    qr.add_data(latin)
    png = qr.make_image()
    png.save("generated/latin.png")

generate_qr_code()
