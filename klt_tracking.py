# code modified from 
# Python OpenCV: Optical Flow with Lucas-Kanade method

# future work on tracking is at https://github.com/Sriram-Sai-Ganesh/landmark-tracking

import numpy as np
import cv2

# webcam feed
cap = cv2.VideoCapture(0)

# params for corner detection
feature_params = dict( maxCorners = 100,
                    qualityLevel = 0.3,
                    minDistance = 7,
                    blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize = (15, 15), 
                    maxLevel = 2, 
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
                    10, 0.03)
                )

# Create some random colors
color = np.random.randint(0, 255, (100, 3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
num_points=5
while(1):
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1[st == 1][:num_points]
    good_old = p0[st == 1][:num_points]

    # draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = map(int, new.ravel())
        c, d = map(int, old.ravel())
        mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
        
    img = cv2.add(frame, mask)

    cv2.imshow('frame', img)
    

    # Updating Previous frame and points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    key = cv2.waitKey(1) & 0xFF
    if key==ord('r'):            # reset and re-acquire points on 'r' keypress
        # Take first frame and find corners in it
        ret, old_frame = cap.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        # Create a mask image for drawing purposes
        mask = np.zeros_like(old_frame)
    
    elif key == ord('q'):        # Break the loop on 'q' keypress
        break

cv2.destroyAllWindows()
cap.release()