import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from vidgear.gears import CamGear

video_path = r"C:\Users\samhp\OneDrive\Desktop\object detection\production_id_5058322 (2160p) (online-video-cutter.com).mp4"
cap = CamGear(source=video_path, logging=True).start()

if cap is None:
    print("Error opening video file")
else:
    screen_width, screen_height = 1920, 1080  

    while True:
        frame = cap.read()

        if frame is None:
            break

        frame = cv2.resize(frame, (screen_width, screen_height))
        bbox, label, conf = cv.detect_common_objects(frame)
        frame = draw_bbox(frame, bbox, label, conf)

        object_counts = {}  

        for obj in label:
            object_counts[obj] = object_counts.get(obj, 0) + 1

        text = ', '.join([f"{obj}={count}" for obj, count in object_counts.items()])
        cv2.putText(frame, text, (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.namedWindow("FRAME", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("FRAME", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("FRAME", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.stop()
    cv2.destroyAllWindows()