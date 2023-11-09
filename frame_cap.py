import cv2

# 'Spacebar' to capture and save an image
# 'q' to exit the program without saving


def capture_calibration_image(saveLocation):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return

    result=False

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture an image from the webcam.")
            break

        cv2.imshow("Webcam", frame)

        key = cv2.waitKey(1) & 0xFF

        # 'Spacebar' to capture and save an image
        if key == ord(" "):
            cv2.imwrite(saveLocation, frame)
            print(f"Image saved at {saveLocation}")
            result=True
            break
        # 'q' to exit the program without saving
        elif key == ord("q"):
            break
        
    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    return result

if __name__ == "__main__":
    capture_calibration_image('./output/caps/framecap.png')
