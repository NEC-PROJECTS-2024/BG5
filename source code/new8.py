import tkinter as tk
from tkinter import filedialog
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from PIL import Image, ImageTk
from vidgear.gears import CamGear
import os

class ObjectDetectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Object Detection App")

        self.video_path = tk.StringVar()

        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.pack()

        self.upload_button = tk.Button(self.master, text="Upload Video", command=self.upload_video)
        self.upload_button.pack()

        self.play_button = tk.Button(self.master, text="Play Video", command=self.play_video)
        self.play_button.pack()

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.video_path.set(file_path)

    def play_video(self):
        video_path = self.video_path.get()
        if not video_path:
            tk.messagebox.showerror("Error", "Please upload a video first.")
            return

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            tk.messagebox.showerror("Error", "Failed to open video file.")
            return

        screen_width, screen_height = 800, 600
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (screen_width, screen_height))
            bbox, label, conf = cv.detect_common_objects(frame)
            frame = draw_bbox(frame, bbox, label, conf)

            object_counts = {}  

            for obj in label:
                object_counts[obj] = object_counts.get(obj, 0) + 1

            text = ', '.join([f"{obj}={count}" for obj, count in object_counts.items()])
            cv2.putText(frame, text, (50, 60), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            if hasattr(self, 'video_display'):
                self.canvas.delete(self.video_display)

            self.video_display = self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image

            self.master.update_idletasks()
            self.master.update()

        cap.release()

def main():
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()