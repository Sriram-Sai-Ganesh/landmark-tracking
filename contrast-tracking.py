import cv2
import numpy as np

# track the high contrast area
def contrast_tracking(frame):
    # Convert the frame to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # uses raw thresholding to identify bright areas; 
    # TODO: switch to a better way.
    # Apply thresholding to create a binary image
    _, binary = cv2.threshold(grayscale, 200, 255, cv2.THRESH_BINARY)

    # identify contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # ID the largest contour (highest contrast area)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        # create and draw bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)
        # bound entire bright area:
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # locate center of bright area
        x+=int(w/2)
        y+=int(h/2)
        # define w and h of bounding rectangle:
        w=h=50
        cv2.rectangle(frame, (int(x-w/2), int(y-w/2)), (x+w, y+h), (0, 255, 0), 2)

    return frame

# loop: capture webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = contrast_tracking(frame)

    # Display the frame with the tracked area
    cv2.imshow('High Contrast Area Tracking', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# end/close windows
cap.release()
cv2.destroyAllWindows()
