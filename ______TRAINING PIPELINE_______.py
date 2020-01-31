#PIPELINE
import cv2
import os
import serial
import matplotlib.pyplot as plt
import numpy as np
import time


arduinoData = serial.Serial('/dev/ttyACM0',9600)
# Playing video from file:
cap = cv2.VideoCapture(0)

try:
    if not os.path.exists('data'):
        os.makedirs('data')
        os.makedirs('data/front/')
        os.makedirs('data/left/')
        os.makedirs('data/right/')
        os.makedirs('data/steepleft/')
        os.makedirs('data/steepright/')
        os.makedirs('data/stopsign/')
        os.makedirs('data/noCrossing/')
        os.makedirs('data/end/')
except OSError:
    print ('Error: Creating directory of data')
k = 119
currentFrame = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret :
        # To stop duplicate images
        currentFrame += 1
        inverted = cv2.flip( frame, 0 )
        
        
       
        ysize = inverted.shape[0]
        xsize = inverted.shape[1]
        color_select = np.copy(inverted)

# Define color selection criteria
###### MODIFY THESE VARIABLES TO MAKE YOUR COLOR SELECTION
        red_threshold = 40
        green_threshold = 50
        blue_threshold = 50



        rgb_threshold = [red_threshold, green_threshold, blue_threshold]

# Do a boolean or with the "|" character to identify
# pixels below the thresholds
        thresholds = (inverted[:,:,0] < rgb_threshold[0]) \
                    | (inverted[:,:,1] < rgb_threshold[1]) \
                    | (inverted[:,:,2] < rgb_threshold[2])
        color_select[thresholds] = [0,0,0]

# Display the image                 


        cv2.imshow('final frame', color_select)
    
        x = cv2.waitKey(100)
        
        if(x == 255):
            key = k
            # Saves image of the current frame in jpg file 
            if(key == 97):
                arduinoData.write(str.encode('a'))
                name = './data/left/frame' + str(currentFrame) + 'l.jpg'
                print ('Creating...' + name)
                cv2.imwrite(name, color_select)
                
            
                
                # Sves image of the current frame in jpg file 
            elif(key == 100):
                arduinoData.write(str.encode('d'))
                name = './data/right/frame' + str(currentFrame) + 'r.jpg'
                print ('Creating...' + name)
                cv2.imwrite(name, color_select)
                
            elif(key == 111): 
                arduinoData.write(str.encode('s'))
                break
                    
            elif (key == 119):
                arduinoData.write(str.encode('w'))
                name = './data/front/frame' + str(currentFrame) + 'f.jpg'
                print ('Creating...' + name)
                cv2.imwrite(name,color_select)
                
            
            elif(key == 115):
                arduinoData.write(str.encode('s'))
                print('stop')
            
            elif(key == 122):                
                arduinoData.write(str.encode('z'))
                name = './data/steepleft/frame' + str(currentFrame) + '_sl.jpg'
                print ('Creating...' + name)
                cv2.imwrite(name, color_select)
                
            elif(key == 99):
                arduinoData.write(str.encode('c'))
                name = './data/steepright/frame' + str(currentFrame) + '_sr.jpg'
                print ('Creating...' + name)
                cv2.imwrite(name, color_select)
            
            elif(key == 110 ):
                name = './data/noCrossing/frame' + str(currentFrame) + 'no_crossing.jpg'
                cv2.imwrite(name, color_select)
                print ('Creating...' + name)
                
            elif(key == 32):
                name = './data/stopsign/frame' + str(currentFrame) + 'stopsign.jpg'
                cv2.imwrite(name, color_select)
                print ('Creating...' + name)
            
            elif(key == 105):
                arduinoData.write(str.encode('c'))
                name = './data/end/frame' + str(currentFrame) + 'end.jpg'
                cv2.imwrite(name, color_select)
                print ('Creating...' + name)
                #f.write("%c\r\n" % (x))
                
        else:
            key = x
            k = x
            
                
                #f.write("%c\r\n" % ('f'))

    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()