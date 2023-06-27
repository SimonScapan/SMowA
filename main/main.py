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

pi_camera = cv2.VideoCapture(0)

####################
# initialize picar #
####################

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)  # horizontal
tilt_servo = Servo.Servo(2) # vertical
#picar.setup()

fw.offset = 0
bw.speed = 0
pan_servo.offset = 10 
tilt_servo.offset = 0

fw.turn(100)
tilt_servo.write(60)

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

def gen(camera):
    while True:
        # get frame from VideoCamera-instance
        ret, frame = pi_camera.read()
        if ret == False:
            print("Failed to read image")

        try:
            
            # Get steering input instruction from lanedetect_steer
            #frame, canny, steering=lanedetect_steer.lane_detection(frame,"outdoor")
            frame, canny, steering=lanedetect_steer.lane_detection(frame,"indoor")
            print('steering: ' + str(steering) )
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

@app.route('/video_feed')

def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)


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