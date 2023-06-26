##################
# import section #
##################

# PiCar
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
# OpenCV
import cv2
# Flask
from flask import Flask, render_template, Response, request
# Time
import time
# Lane Detection
from lane_detection import lanedetect_steer


#####################
# initialize camera #
#####################

pi_camera = cv2.VideoCapture(-1)
pi_camera.set(3,160) #SCREEN_WIDTH
pi_camera.set(4,120) #SCREEN_HEIGHT

####################
# initialize picar #
####################

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
bw.speed = 0
pan_servo.offset = 10
tilt_servo.offset = 0

fw.turn(90)
pan_servo.write(90)
tilt_servo.write(90)
# motor_speed = 60

#################################
# initialize Monitoring Website #
#################################

app = Flask(__name__)

#############################
# defining helper functions #
#############################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/objects')
def index2():
    return render_template('index2.html')

def gen(camera):
    while True:
        # get frame from VideoCamera-instance
        ret, frame = pi_camera.read()
        if ret == False:
            print("Failed to read image")

        try:
            
            # Get steering input instruction from lanedetect_steer
            frame, canny, steering=lanedetect_steer.lane_detection(frame,"outdoor")
            # frame, canny, steering=lanedetect_steer.lane_detection(frame,"indoor")
            
            # Give the steering instruction from lanedetect_steer to the Car-instance
            #car.steer(steering)
            #time.sleep(0.0125)

        except Exception as e:
            print("Error in detection")
            print(e)

        # Convert the processed frame to show it in the browser
        ret, frame = cv2.imencode(".jpg",frame) 
        frame = frame.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

######################################################################################################
'''
def nothing(x):
    pass

def destroy():
    bw.stop()
    pi_camera.release()

def test():
    fw.turn(90)

def main():
    pan_angle = 90              # initial angle for pan
    tilt_angle = 90             # initial angle for tilt
    fw_angle = 90
'''