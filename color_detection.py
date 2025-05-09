import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

#Function that runs color picker app after selecting the image
def run_color_detector(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (800, 600))
    clicked = False
    r = g = b = x_pos = y_pos = 0

    def show_color(event, x, y, flags, param):
        nonlocal b, g, r, x_pos, y_pos, clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked = True
            x_pos = x
            y_pos = y
            b, g, r = img[y, x]
            b = int(b)
            g = int(g)
            r = int(r)

    cv2.namedWindow("Color Detector")
    cv2.setMouseCallback("Color Detector", show_color)

    while True:
        display_img = img.copy()
        if clicked:
            cv2.rectangle(display_img, (20, 20), (600, 60), (b, g, r), -1)
            text = f"RGB: ({r}, {g}, {b})"
            hsv = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)
            text += f" | HSV: ({hsv[0][0][0]}, {hsv[0][0][1]}, {hsv[0][0][2]})"
            color = (255, 255, 255) if r + g + b < 400 else (0, 0, 0)
            cv2.putText(display_img, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Color Detector", display_img)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

#Function called when pressing button
def import_image():
    image_path = filedialog.askopenfilename(
        title="Selectează o imagine",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if image_path:
        root.destroy()  # Închide fereastra de start
        run_color_detector(image_path)

#Tkinter Interface
root = tk.Tk()
root.title("Color Detector")
root.geometry("600x600")
root.resizable(False, False)

#Center Button - Import Image
import_btn = tk.Button(root, text="Import Image", font=("Arial", 18), command=import_image)
import_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()
