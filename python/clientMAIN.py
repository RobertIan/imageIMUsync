import RPi.GPIO as GPIO
import os
import io
import softresetClient as softreset
from compoundpi.client import CompoundPiClient

# waitfor pi function
def waitforpisignal(GPIOPINNo, wait):
    while wait:
        print 'waiting'
        if GPIO.input(GPIOPINNo):
            print' waiting'
	    pass
        else:
            wait = False
            print 'message recieved'

## variables defined
wait = True
triggerGPIO = 23
pi2piGPIO = 24
network = '128.83.0.0/16' #IP range for pis connected to network
stacksize = 10 #number of images to grab in each stack
memthreshold = 2000 #memmory threshold, in kbs

##trigger and switch inputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP) # interrupt
GPIO.setup(pi2piGPIO, GPIO.IN) # switch

## wait for pi2server to come online
waitforpisignal(pi2piGPIO, wait)

## set directory so we can run from rc.local or the local folder
os.chdir('/')

## turn on shutdown switch listening
down = softreset.App()

## cameras
cameraclient = CompoundPiClient()
cameraclient.servers.network = network
cameraclient.servers.find() #should return 2 cameras
cameraclient.resolution(1920, 1080)
cameraclient.agc('auto')
cameraclient.awb('off', 1.5, 1.3)
cameraclient.iso(100)
cameraclient.metering('spot')
cameraclient.brightness(50)
cameraclient.contrast(0)
cameraclient.saturation(0)
cameraclient.denoise(False)
cameraclient.identify() #simultaneous blinking camera lights = ready to go
responses = cameraclient.status()
min_time = min(status.timestamp for status in responses.values())
for address, status in responses.items():
        if (status.timestamp - min_time).total_seconds() > 0.3:
            print('Warning: time on %s deviates from minimum '
                'by >0.1 seconds' % address)

while True:
    #availmem, usedmem, totatl = disk.checkds(memthreshold)
    try:
        GPIO.wait_for_edge(triggerGPIO, GPIO.FALLING)
        cameraclient.capture(5, delay=0.25) #record synchronized image stack
        #cameraclient.record(10, format=u'h264', delay=0.5) #record synchronized video
        print cameraclient.status().items()
        try:
            for addr, files in cameraclient.list().items():
                for f in files:
                    assert f.filetype == 'IMAGE'
                    print f
                    print addr
                    print f.timestamp
                    with io.open('%s_%s.jpg' % (addr,f.timestamp), 'wb') as output: #need to change timestamp format (currently includes spaces/not scp-usable)
                        cameraclient.download(addr, f.index, output)
        finally:
            cameraclient.clear()
    except KeyboardInterrupt:
        cameraclient.clear()
        cameraclient.close()
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
        break

cameraclient.close()
GPIO.cleanup()
exit()
