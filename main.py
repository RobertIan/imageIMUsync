import camera, checkdisk, checkbattery, RTIMU
import multiprocessing
import math

logging.basicConfig(filename='../log/divelog.log', level=logging.INFO)
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s', "%H-%M-%S-%f")
hdlr.setFormatter(formatter)
datlog.addHandler(hdlr)
datlog.setLevel(logging.INFO)

SETTINGS_FILE = "RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
if not os.path.exists(SETTINGS_FILE + ".ini"):
    logging.info('Settings file does not exist, will be created')
imu = RTIMU.RTIMU(s)


logging.info('IMU Name: %f' % imu.IMUName())
if (not imu.IMUInit()):
    logging.info('IMU Init Failed')
else:
    logging.info('IMU Init Succeeded')
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)


kamera = camera.App('yuv', 'yuv' '1920x1080', 'sports', '30', '1', 'outfile')


if imu.IMURead():
    kamera.capraw()
    data = imu.getIMUData()
    logging.info(data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure$
    fusionPose = data["fusionPose"]
    logging.info("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),
    math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
    if (data["pressureValid"]):
        logging.info("Pressure: %f" % data["pressure"])
    if (data["temperatureValid"]):
        logging.info("Temperature: %f" % (data["temperature"]))



