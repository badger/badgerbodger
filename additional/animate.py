import badger2040
import jpegdec
import time, os

PLAY_PATH = "/images"

display = badger2040.Badger2040()
jpeg = jpegdec.JPEG(display.display)

display.led(128)
display.clear()

# Get sorted list of jpg files
files = os.listdir(PLAY_PATH)

while True:
    if files:
        # Display first image for 5 seconds with UPDATE_NORMAL
        first_file = files[0]
        display.set_update_speed(badger2040.UPDATE_NORMAL)
        jpeg.open_file(PLAY_PATH + "/" + first_file)
        jpeg.decode(30, 0)
        display.update()
        time.sleep(5)

        # Play the rest of the folder with 0.5 second intervals
        display.set_update_speed(badger2040.UPDATE_TURBO)
        for file in files[1:]:
            jpeg.open_file(PLAY_PATH + "/" + file)
            jpeg.decode(30, 0)
            display.update()
            time.sleep(0.5)
