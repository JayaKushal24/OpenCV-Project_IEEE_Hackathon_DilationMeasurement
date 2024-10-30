import cv2
import numpy as np
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import time
import csv

# Conversion factor (adjust based on your calibration)
conversion_factor = 0.0166666666666667  # Example: 1 cm = 60 pixels => 0.0167 cm/pixel

class OpenCVCircleDetection(Image):
    def __init__(self, **kwargs):
        super(OpenCVCircleDetection, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)  # Start video capture
        self.frame_width = 640
        self.frame_height = 480
        self.capture.set(3, self.frame_width)
        self.capture.set(4, self.frame_height)

        # Default thresholds
        self.threshold1 = 63
        self.threshold2 = 113
        self.show_radius = False  # Toggle for showing radius
        self.current_radius = None  # Store current radius for CSV writing

        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update at 30 FPS

    def set_threshold1(self, value):
        self.threshold1 = int(value)

    def set_threshold2(self, value):
        self.threshold2 = int(value)

    def toggle_radius(self, instance):
        self.show_radius = not self.show_radius  # Toggle radius display on/off

        # Write to CSV only if the radius is available
        if self.show_radius and self.current_radius is not None:
            self.write_to_csv(self.current_radius)  # Write to CSV if radius is available
            print(f"Writing to CSV: Time - {time.strftime('%H:%M')}, Radius - {self.current_radius:.2f} cm")  # Debug statement

    def write_to_csv(self, radius):
        # Get the current time in "HH:MM" format
        current_time = time.strftime("%H:%M")

        # File path for the CSV file
        csv_file = "output.csv"

        # Open the CSV file in append mode
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the current time and radius into the CSV
            writer.writerow([current_time, radius])

        print(f"Data written to {csv_file}: Time - {current_time}, Radius - {radius:.2f} cm")  # Confirm data write

    def getcontours(self, img, imgcontour):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 5000:
                cv2.drawContours(imgcontour, cnt, -1, (255, 0, 255), 7)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                # Circle detection using minEnclosingCircle
                if len(approx) > 4:
                    (x_center, y_center), radius = cv2.minEnclosingCircle(cnt)
                    center = (int(x_center), int(y_center))
                    radius = int(radius)

                    self.current_radius = radius * conversion_factor  # Store radius in cm

                    # Debug print to see the current radius
                    # print(f"Detected Radius: {self.current_radius:.2f} cm")  # Debug statement

                    if self.show_radius:
                        # Draw the center point and the radius
                        cv2.circle(imgcontour, center, 5, (0, 0, 255), -1)
                        endpoint = (int(x_center + radius), int(y_center))
                        cv2.line(imgcontour, center, endpoint, (0, 255, 0), 2)

                        # Display radius in cm at the bottom of the image
                        height = imgcontour.shape[0]
                        cv2.putText(imgcontour, f"Radius: {self.current_radius:.2f} cm", (50, height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            imgBlur = cv2.GaussianBlur(frame, (7, 7), 1)
            imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
            imgCanny = cv2.Canny(imgGray, self.threshold1, self.threshold2)
            kernel = np.ones((5, 5))
            imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

            imgContour = frame.copy()
            self.getcontours(imgDil, imgContour)

            # Convert image to Kivy texture
            buf = cv2.flip(imgContour, 0).tostring()
            texture = Texture.create(size=(imgContour.shape[1], imgContour.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture

class CircleDetectionApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Create the OpenCV detection widget
        self.img_widget = OpenCVCircleDetection()

        # Create sliders and labels for threshold1 and threshold2
        threshold1_label = Label(text='Threshold 1')
        self.threshold1_slider = Slider(min=0, max=255, value=63)
        self.threshold1_slider.bind(value=lambda instance, value: self.img_widget.set_threshold1(value))

        threshold2_label = Label(text='Threshold 2')
        self.threshold2_slider = Slider(min=0, max=255, value=113)
        self.threshold2_slider.bind(value=lambda instance, value: self.img_widget.set_threshold2(value))

        # Create the "Radius" button
        self.radius_button = Button(text="Radius")
        self.radius_button.bind(on_press=self.img_widget.toggle_radius)

        # Layout for sliders and button
        control_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        # Add the sliders and button to the control layout
        control_layout.add_widget(threshold1_label)
        control_layout.add_widget(self.threshold1_slider)
        control_layout.add_widget(threshold2_label)
        control_layout.add_widget(self.threshold2_slider)
        control_layout.add_widget(self.radius_button)

        # Add widgets to the main layout
        layout.add_widget(self.img_widget)
        layout.add_widget(control_layout)

        return layout

if __name__ == '__main__':
    CircleDetectionApp().run()
