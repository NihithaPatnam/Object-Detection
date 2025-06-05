import cv2
from PIL import Image, ImageTk
import tkinter as tk
import turtle

# Function to process the video frame and detect objects with blue circles
def process_frame(frame):
    # Convert frame to grayscale for object detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Simple object detection using thresholding
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Find contours of the detected objects
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw blue circles around the detected objects
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter out small contours
            # Get the center and radius of a circle that encloses the object
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            # Draw the blue circle around the object
            cv2.circle(frame, center, radius, (0, 0, 255), 2)  # blue color (BGR)

    return frame

# Function to display real-time video with object detection
def show_video():
    ret, frame = cap.read()
    if ret:
        processed_frame = process_frame(frame)

        # Convert the processed frame into an image format Tkinter can use
        img = Image.fromarray(processed_frame)
        imgtk = ImageTk.PhotoImage(image=img)

        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # Call this function again after 10ms
    video_label.after(10, show_video)

# Function to visualize objects in 3D space using Turtle
def visualize_3d():
    turtle.setup(800, 600)
    turtle.speed(1)
    turtle.bgcolor("black")
    
    turtle.penup()
    turtle.goto(-200, 100)
    turtle.pendown()

    # Draw a simple 3D object (like a cube) to represent detection
    for i in range(4):
        turtle.forward(200)
        turtle.right(90)

    turtle.right(45)
    turtle.forward(141)
    for i in range(4):
        turtle.forward(200)
        turtle.right(90)

    turtle.done()

# Set up video capture
cap = cv2.VideoCapture(0)

# Create a Tkinter window
window = tk.Tk()
window.title("Real-Time Object Detection and 3D Visualization")

# Create a label to show the video feed
video_label = tk.Label(window)
video_label.pack()

# Create a button to start 3D visualization
visualize_button = tk.Button(window, text="Visualize in 3D", command=visualize_3d)
visualize_button.pack()

# Start showing the video
show_video()

# Start the Tkinter event loop
window.mainloop()

# Release the video capture when window is closed
cap.release()
cv2.destroyAllWindows()
