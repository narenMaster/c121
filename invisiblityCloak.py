import cv2
import time 
import numpy as np 

#preparation for writing the output video 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))

# reading from web cam 
cap=cv2.VideoCapture(0)

#allow the system to sleep for 3 secondsbefore the webcam starts
time.sleep(3)
count=0
background=0

#capture the background in range of 60 
for i in range(60) :
    ret,background=cap.read()
background=np.flip(background,axis=1)

#read every frame from the webcam untill the cam is open 
while(cap.isOpened()):
    ret,img=cap.read()
    if not ret :
        break
    count+=1
    img=np.flip(img,axis=1)

    # convert the colour space from rgb to hsv
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # genetrate mask to deducted the read color 
    lower_red=np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask1=cv2.inRange(hsv,lower_red,upper_red)

    lower_red=np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_red,upper_red)
    mask1=mask1+mask2

    #open and dilate the mask image 
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    # create a inverted mask to segment out the red color from the frame
    mask2=cv2.bitwise_not(mask1)

    #segment the red color part out of the frame using bitwise and withe the inverted mask
    res1=cv2.bitwise_and(img,img,mask=mask2)

    #next  create image showing static background frame pixels only for the masked region
    res2=cv2.bitwise_and(background,background,mask=mask1)

    # generating the final output 
    final_output=cv2.addWeighted(res1,1,res2,1,0)
    out.write(final_output)
    cv2.imshow("magic",final_output)
    cv2.waitKey(1)

# release the camera and close all windows in open the process
cap.release()
out.release()
cv2.destroyAllWindows()
   

