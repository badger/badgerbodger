Images must be 296x128 pixel NON-PROGRESSIVE jpegs

The badge can only dsplay at 1-bit color depth, so any colour
will be dithered to black and white.

For best results, create a 1-bit PNG file and then use an
application like ImageMagick to convert it to a jpeg.  By
default many graphics applications will create a progressive
jpeg which the JPEGDEC library in PicoGraphics does not support.

You can convert using a command like:

> convert in.png -monochrome out.jpg
