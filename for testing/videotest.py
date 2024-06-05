import cv2

# Open the video file
# video_path = "path/to/video.mp4"
cap = cv2.VideoCapture(1)

# Loop through the video frames
r = int(input("Radius: "))
frame_width = 1200
frame_height = 600
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:

        # Display the annotated frame
        result = cv2.resize(frame,(frame_width,frame_height))
        result = cv2.circle(result, (int(frame_width//2),int(frame_height//2)), radius=10, color=(0, 0, 0), thickness=-1)
        result = cv2.circle(result, (int(frame_width//2),int(frame_height//2)), radius=r, color=(0, 255, 100), thickness=2)
        result = cv2.line(result, (int(frame_width//2),int(frame_height//2)-r), (int(frame_width//2),int(frame_height//2)+r), (0,255,100), 2)
        result = cv2.line(result, (int(frame_width//2)-r,int(frame_height//2)), (int(frame_width//2)+r,int(frame_height//2)), (0,255,100), 2)
        cv2.imshow("YOLOv8 Tracking", result)

        # Break the loop if 'esc' is pressed
        if (cv2.waitKey(30) == 27):
            break
    else:
        # Break the loop if the end of the video is reached
        break
cap.release()
cv2.destroyAllWindows()