import cv2

def save_webcam_images():
    cap = cv2.VideoCapture(0)
    img_folder_path='output/'
    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return

    image_counter = 0

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
            image_counter += 1
            image_filename = f"img_{image_counter}.jpg"
            cv2.imwrite(img_folder_path+image_filename, frame)
            print(f"Image saved as {image_filename}")
        # 'q' to exit the program
        elif key == ord("q"):
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    save_webcam_images()
