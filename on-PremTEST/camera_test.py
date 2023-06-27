# OpenCV
import cv2
# Flask
from flask import Flask, render_template, Response, request
# Time
import time

#####################
# initialize camera #
#####################

pi_camera = cv2.VideoCapture(0)

#################################
# initialize Monitoring Website #
#################################

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

def gen(camera):
    while True:
            # get frame from VideoCamera-instance
            ret, frame = pi_camera.read()
            if ret == False:
                print("Failed to read image")

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


### for running localy
'''
while(True):
    
    ret, frame = pi_camera.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
pi_camera.release()
# Destroy all the windows
cv2.destroyAllWindows()

'''