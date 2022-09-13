from machine import Pin, I2C, ADC, SPI
import os
import ssd1306
import gc
import sys
import wifi
import ujson
import urequests
from wavplayer import WavPlayer
from sdcard import SDCard

import time

from random import randrange
from random import randint

import uos
fs_stat = uos.statvfs('/')
fs_size = fs_stat[0] * fs_stat[2]
fs_free = fs_stat[0] * fs_stat[3]
print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))

THUNDER_ICON = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

WIDTH = 128
HEIGHT = 32

mp3Files = ["thunder3_mono.wav", "thunder1.wav", "thunder2.wav", "thunder4_mono.wav"]

i2s = None
vfs = None
sd = None
spi = None
oled = None

SDA_DISPLAY = Pin(14) # board.GP14
SCL_DISPLAY = Pin(15) # board.GP15

MOSI = Pin(11) # board.GP11
MISO = Pin(8) # board.GP8
SCK = Pin(10) # board.GP10
CS = Pin(13, machine.Pin.OUT) # board.GP9

BCK_PIN = Pin(16) # board.GP16
LCK_PIN = Pin(17) # board.GP17
DIN_PIN = Pin(18) # board.GP18

BGLIGHT = Pin(0, Pin.OUT) 
#digitalio.DigitalInOut(board.GP0)
#BGLIGHT.direction = digitalio.Direction.OUTPUT

THLIGHT =  Pin(1, Pin.OUT) 
#digitalio.DigitalInOut(board.GP1)
#PIN01.direction = digitalio.Direction.OUTPUT

LED = Pin("LED", Pin.OUT) # digitalio.DigitamicrpomlInOut(board.LED)
# led.direction = digitalio.Direction.OUTPUT
LED.on()

potentiometer = ADC(26) #analogio.AnalogIn(board.GP26)

def readSecrets():
    print("reading Wifi secrets")    
    
    with open('secrets.json') as fp:
        secrets = ujson.loads(fp.read())
        return secrets

def wifiConnect():
    print("Tryin to create Wifi connection")    
        
    if not wifi.wlan.isconnected():                    
        # wifi.printStatusCodes()
        
        try:            
            secrets = readSecrets()
            wifi.connect(secrets['wifi']['ssid'], secrets['wifi']['pass'])            
        except Exception as e:            
            print("Exception when trying to connect " + secrets['wifi']['ssid'])
            print(repr(e))
            sys.print_exception(e)

        if wifi.wlan.isconnected():
            LED.on()
            status = wifi.wlan.ifconfig()
            print('wifi_management IP = ' + status[0])          
        else:
            LED.off()
    else:        
        LED.on()

def getPropRemoteStatus():
    activatePropStatus = False
    propId = 1
    urlBase = "http://192.168.123.60:8080/api/v1/props/"
    url = urlBase + str(propId)
        
    try:
        # Make GET request
        print("Making GET request: {0}".format(url))
        res = urequests.get(url)
        print(res.json()['running'])
        activatePropStatus = res.json()['running']
    except Exception as e:
        print("Exception occurs when GET " + url)
        print(repr(e))
        sys.print_exception(e)
        showLEDError()
    finally:
        try:
            res.close()
        except:
            print("Skipping response closing")

    gc.collect()  
    
    return activatePropStatus

def showLEDError():
    print("Show error")
    
    LED.toggle()
    time.sleep(0.15)
    LED.toggle()
    time.sleep(0.15)
    LED.toggle()
    time.sleep(0.15)
    LED.toggle()
    time.sleep(0.15)
    LED.toggle()
    time.sleep(0.15)
    LED.toggle()
    time.sleep(0.15)
    LED.toggle()
    time.sleep(0.15)
    LED.toggle()

def init():
    initAudioI2S0()
    initSDCardI2S1()
    initThunder()
    initOled()

def initOled():
    i2c = I2C(1, scl=Pin(15), sda=Pin(14))
    print(i2c.scan())
    #i2c = I2C(0, SCL_DISPLAY, SDA_DISPLAY)
    global oled
    oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
    oled.fill(0)
    oled.show()
    
def initSDCardI2S1():
    spi = SPI(
        1,
        baudrate=40000000,  # this has no effect on spi bus speed to SD Card
        #polarity=0,
        #phase=0,
        #bits=8,
        #firstbit=machine.SPI.MSB,
        sck=Pin(10), #SCK,
        mosi=Pin(11), #MOSI,
        miso=Pin(8) #MISO
    )
    
    # ======= SD CARD CONFIGURATION =======
    sd = SDCard(spi, CS)
    # sd.init_spi(25_000_000)  # increase SPI bus speed to SD card
    vfs=os.VfsFat(sd)
    os.mount(sd, "/sd")
    # ======= SD CARD CONFIGURATION =======
    
    print(os.listdir('/sd'))

def initAudioI2S0():
    global i2s
    i2s = WavPlayer(id=0, 
                    sck_pin=BCK_PIN, 
                    ws_pin=LCK_PIN, 
                    sd_pin=DIN_PIN, 
                    ibuf=10000)

def showThunderIcon():
    oled.fill(0)  # Clear the display
    showIcon(5, 0, THUNDER_ICON)
    showIcon(39, 0, THUNDER_ICON)
    showIcon(79, 0, THUNDER_ICON)
    oled.show()

def showIcon(offsetx, offsety, ICON):
    for y, row in enumerate(ICON):
        for x, c in enumerate(row):
            oled.pixel(x + offsetx, y + offsety, c)

def initThunder():
    BGLIGHT.value(0) # = False
    THLIGHT.value(0) # = False

def bgLightOff():
    BGLIGHT.value(1) # = True

def bgLightOn():
    BGLIGHT.value(0) # = False

def thunderLight():
    showThunderIcon()
    THLIGHT.value(1) # = True
    time.sleep(0.05)
    THLIGHT.value(0) # = False
    time.sleep(0.05)
    THLIGHT.value(1) # = True
    time.sleep(0.05)
    THLIGHT.value(0) # = False
    time.sleep(0.05)
    THLIGHT.value(1) # = True
    time.sleep(0.05)
    THLIGHT.value(0) # = False
    time.sleep(0.5)

def getWavFromFlash():
    index = randrange(len(mp3Files))

# https://audio.online-convert.com/convert-to-wav
    print("opennign wav ", mp3Files[index], " from flash...")

    return mp3Files[index]

def getMp3FromFlash():
    index = randrange(len(mp3Files))

    print("opennign mp3 ", mp3Files[index], " from flash...")

    mp3File = open(mp3Files[index], "rb")

    print("decoding mp3 file...")

    return MP3Decoder(mp3File)

def thunderSound():
    # audio = getMp3FromFlash()
    audio = getWavFromFlash()

    # print("starting playing audio...")
    i2s.play(audio)

    # print("playing audio...")

    while i2s.isplaying():
        time.sleep(0.5)
        pass

    # print("sound ends")

def thunder(num_thunders):
    print("thunder: ", num_thunders)
    for x in range(num_thunders):
        thunderLight()
        thunderSound()
        time.sleep(3)

def thunderStorm():
    print("thunderStorm")
    bgLightOff()
    time.sleep(3)
    thunder(randint(1, 5))
    bgLightOn()

def getPotValueSeconds(LAST_THUNDER_TIME):
    #print("getPotValueSeconds(" + str(LAST_THUNDER_TIME) + ")")
    max_pote_value = 65000
    min_time_seconds = 10
    max_time_seconds = 900
    seconds_one_minute = 60

    currentvalue = potentiometer.read_u16()
    seconds = (currentvalue * max_time_seconds) / max_pote_value
    seconds = max(min(max_time_seconds, seconds), min_time_seconds)
    seconds = round(seconds, 0)
    #print('pote = ', currentvalue, ' seconds = ', seconds,
    #      ' minutes = ', seconds / seconds_one_minute, 'time.time= ', time.time())

    text = 'Interval = {}'.format(seconds)
    oled.fill(0)
    oled.text(text, 0, 0, 1)

    #timeleft = round((LAST_THUNDER_TIME + seconds) - time.time(), 0)
    timeleft = LAST_THUNDER_TIME - time.time() + seconds 
    #print('timeleft: ', timeleft, 'AST_THUNDER_TIME + seconds:', LAST_THUNDER_TIME + seconds)
    text = 'Sec.Left = {}'.format(timeleft)
    
    oled.text(text, 0, 10, 1)
    oled.show()

    return seconds

def loop():
    LAST_THUNDER_TIME = time.time()
    LAST_REMOTE_CHECK = time.time()
    REMOTE_INTERVAL_CHECK = 5
    remotePropStatus = False
    while True:
        now = time.time()
        
        if now >= LAST_REMOTE_CHECK + REMOTE_INTERVAL_CHECK:
            if not wifi.wlan.isconnected():
                wifiConnect()
                    
            if wifi.wlan.isconnected():
                remotePropStatus = getPropRemoteStatus()
            
            LAST_REMOTE_CHECK = time.time()
        
        BLINK_OFF_DURATION = getPotValueSeconds(LAST_THUNDER_TIME)
        
#         print("BLINK_OFF_DURATION:" + str(BLINK_OFF_DURATION))
        
        if (now >= LAST_THUNDER_TIME + BLINK_OFF_DURATION) or remotePropStatus:
            thunderStorm()
            LAST_THUNDER_TIME = time.time()
        else:
            time.sleep(1)

init()
loop()