import socket
import time
from neopixel import *
import argparse
from astar import *
import threading

# LED strip configuration:
LED_COUNT      = 10      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def convertColor(color):
    buff = {"blue": [0,0,255], "yellow": [255,255,0], "red": [0,255,0],
    "green": [204,51,0], "orange": [101,255,0], "brown": [0,51,0]}
    if color in buff:
        c = buff[color]
        return Color(c[0], c[1], c[2])
    return Color(0,102,204)

# def colorWipe(strip, color, wait_ms=50):
def colorWipe3(strip, start, end, color, speed):
    """Wipe color across display a pixel at a time."""
    color = convertColor(color)
    wait_ms = 400*speed
    if start < end:
        # start -= 1
        while start <= end:
            strip.setPixelColor(start, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            strip.setPixelColor(start, Color(0,0,0))
            strip.show()
            print(start+1)
            start += 1
    else:
        while start >= end:
            strip.setPixelColor(start, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            strip.setPixelColor(start, Color(0,0,0))
            strip.show()            
            print(start-1)
            start -= 1

def getBandeDatas(bandes, id):
    for b in bandes:
        if b['id'] == id:
            return b
    return None

def my_thread(strips, data):
    print("received message:"+data.decode())
    datas = loads(data.decode())
    bandeDatas = getBandeDatas(bandes, datas['bandeId'])
    print(bandeDatas)
    #strip = Adafruit_NeoPixel(bandeDatas['ledCount'], bandeDatas['gpio'], LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, bandeDatas['channel'])
    #strip.begin()
    colorWipe3(strips[str(bandeDatas['id'])], datas['startIndex'], datas['endIndex'], datas['color'], datas['speed'])
    print("========")

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-cf', '--config', help='specify a config file')
    args = parser.parse_args()
    bandes = fileToList('bandes.json')
    bandesId = fileToList(args.config)['bandesId']
    strips = {}

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    UDP_IP = "0.0.0.0"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    for b in bandesId:
        datas = getBandeDatas(bandes, b)
        strips[str(b)] = Adafruit_NeoPixel(datas['ledCount'], datas['gpio'], LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, datas['channel'])
        strips[str(b)].begin() 
    # strip2 = Adafruit_NeoPixel(14, 19, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 1)
    # strip1.begin()
    # strip2.begin()

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            x = threading.Thread(target=my_thread, args=(strips, data))
            x.start()
            
    
    except KeyboardInterrupt:
        if args.clear:
            #colorWipe(strip, Color(0,0,0), 10)
            colorWipe(strip1, Color(0,0,0), 10)
            colorWipe(strip2, Color(0,0,0), 10)


    # try:

    #     while True:
    #         print ('Color wipe animations.')
    #         colorWipe2(strip, Color(255, 0, 0))  # Red wipe
    #         colorWipe2(strip, Color(0, 255, 0))  # Blue wipe
    #         colorWipe2(strip, Color(0, 0, 255))  # Green wipe

    # except KeyboardInterrupt:
    #     if args.clear:
    #         colorWipe(strip, Color(0,0,0), 10)