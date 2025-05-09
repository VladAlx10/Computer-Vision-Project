import sys

import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk


class SketchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sketch Filter App")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize variables
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.sketch_image = None
        self.display_image = None
        self.photo_image = None
        self.photo_sketch = None

        # Parameters
        self.edge_param1 = tk.IntVar(value=10)
        self.edge_param2 = tk.IntVar(value=50)
        self.blur_size = tk.IntVar(value=7)
        self.texture_amount = tk.IntVar(value=50)
        self.line_thickness = tk.IntVar(value=1)

        # Create UI
        self.create_ui()

        # Initial message
        self.status_label.config(text="Încarcă o imagine pentru a începe.")

    def create_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left control panel
        control_frame = tk.LabelFrame(main_frame, text="Control", bg="#f0f0f0", padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Load image button
        load_btn = tk.Button(control_frame, text="Încarcă Imagine", command=self.load_image,
                             bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                             width=20, height=2, cursor="hand2")
        load_btn.pack(pady=10)

        # Parameters frame
        params_frame = tk.LabelFrame(control_frame, text="Parametri", bg="#f0f0f0", padx=10, pady=10)
        params_frame.pack(fill=tk.X, pady=10)

        # Edge detection parameters
        tk.Label(params_frame, text="Sensibilitate Margini:", bg="#f0f0f0").pack(anchor=tk.W)
        edge1_slider = ttk.Scale(params_frame, from_=5, to=50, variable=self.edge_param1,
                                 command=lambda _: self.update_sketch())
        edge1_slider.pack(fill=tk.X, pady=5)

        tk.Label(params_frame, text="Prag Margini:", bg="#f0f0f0").pack(anchor=tk.W)
        edge2_slider = ttk.Scale(params_frame, from_=30, to=150, variable=self.edge_param2,
                                 command=lambda _: self.update_sketch())
        edge2_slider.pack(fill=tk.X, pady=5)

        tk.Label(params_frame, text="Blur:", bg="#f0f0f0").pack(anchor=tk.W)
        blur_slider = ttk.Scale(params_frame, from_=1, to=15, variable=self.blur_size,
                                command=lambda _: self.update_sketch())
        blur_slider.pack(fill=tk.X, pady=5)

        tk.Label(params_frame, text="Textură:", bg="#f0f0f0").pack(anchor=tk.W)
        texture_slider = ttk.Scale(params_frame, from_=0, to=100, variable=self.texture_amount,
                                   command=lambda _: self.update_sketch())
        texture_slider.pack(fill=tk.X, pady=5)

        tk.Label(params_frame, text="Grosime Linii:", bg="#f0f0f0").pack(anchor=tk.W)
        thickness_slider = ttk.Scale(params_frame, from_=1, to=5, variable=self.line_thickness,
                                     command=lambda _: self.update_sketch())
        thickness_slider.pack(fill=tk.X, pady=5)

        # Effect types
        effect_frame = tk.LabelFrame(control_frame, text="Tip Efect", bg="#f0f0f0", padx=10, pady=10)
        effect_frame.pack(fill=tk.X, pady=10)

        self.effect_type = tk.StringVar(value="crayon")
        tk.Radiobutton(effect_frame, text="Creion colorat", variable=self.effect_type,
                       value="crayon", bg="#f0f0f0", command=self.update_sketch).pack(anchor=tk.W)
        tk.Radiobutton(effect_frame, text="Creion negru", variable=self.effect_type,
                       value="pencil", bg="#f0f0f0", command=self.update_sketch).pack(anchor=tk.W)
        tk.Radiobutton(effect_frame, text="Schițe", variable=self.effect_type,
                       value="sketch", bg="#f0f0f0", command=self.update_sketch).pack(anchor=tk.W)

        # Save button
        save_btn = tk.Button(control_frame, text="Salvează Imaginea", command=self.save_image,
                             bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                             width=20, height=2, cursor="hand2")
        save_btn.pack(pady=20)

        # Reset button
        reset_btn = tk.Button(control_frame, text="Resetează Parametri", command=self.reset_params,
                              bg="#FF5722", fg="white", font=("Arial", 10),
                              width=20, cursor="hand2")
        reset_btn.pack(pady=5)

        # Right panel with images
        image_frame = tk.Frame(main_frame, bg="#f0f0f0")
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Original image
        original_frame = tk.LabelFrame(image_frame, text="Imagine Originală", bg="#f0f0f0")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.original_canvas = tk.Canvas(original_frame, bg="white")
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Sketch image
        sketch_frame = tk.LabelFrame(image_frame, text="Efect Creion", bg="#f0f0f0")
        sketch_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.sketch_canvas = tk.Canvas(sketch_frame, bg="white")
        self.sketch_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Status bar
        status_frame = tk.Frame(self.root, bg="#e0e0e0", height=25)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(status_frame, text="", bg="#e0e0e0", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10)

    def load_image(self):
        # Open file dialog
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]

        filepath = filedialog.askopenfilename(
            title="Selectează o imagine",
            filetypes=filetypes
        )

        if not filepath:
            return

        try:
            # Load image with OpenCV
            self.image_path = filepath
            self.original_image = cv2.imread(filepath)

            if self.original_image is None:
                raise ValueError("Nu s-a putut încărca imaginea")

            # Convert to RGB for display
            self.current_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

            # Update the interface
            self.update_sketch()
            self.display_images()

            self.status_label.config(text=f"Imagine încărcată: {os.path.basename(filepath)}")
        except Exception as e:
            self.status_label.config(text=f"Eroare: {str(e)}")

    def update_sketch(self):
        if self.original_image is None:
            return

        try:
            # Get current parameters
            edge_param1 = self.edge_param1.get()
            edge_param2 = self.edge_param2.get()
            blur_size = self.blur_size.get()
            if blur_size % 2 == 0:  # Ensure odd number for Gaussian blur
                blur_size += 1
            texture = self.texture_amount.get()
            thickness = self.line_thickness.get()
            effect = self.effect_type.get()

            # Create a copy of the original
            image = self.original_image.copy()

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply blur for noise reduction
            blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)

            # Edge detection
            edges = cv2.Canny(blurred, edge_param1, edge_param2)

            # Thicken lines if needed
            if thickness > 1:
                kernel = np.ones((thickness, thickness), np.uint8)
                edges = cv2.dilate(edges, kernel, iterations=1)

            # Invert for pencil effect
            _, sketch = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY_INV)

            # Add texture/noise if desired
            if texture > 0:
                noise = np.zeros(gray.shape, np.uint8)
                cv2.randu(noise, 0, texture)
                sketch = cv2.add(sketch, noise)

            # Apply different effect types
            if effect == "crayon":
                # Colored crayon effect
                sketch_color = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
                # Add subtle color tint
                sketch_color[:, :, 0] = sketch_color[:, :, 0] * 0.9  # Blue tint
                sketch_color[:, :, 1] = sketch_color[:, :, 1] * 0.95  # Green tint
                self.sketch_image = cv2.cvtColor(sketch_color, cv2.COLOR_BGR2RGB)
            elif effect == "pencil":
                # Basic black pencil effect
                self.sketch_image = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
            else:  # sketch
                # More artistic sketch effect
                sketch_inv = 255 - sketch
                blur_amount = int(blur_size * 1.5)
                if blur_amount % 2 == 0:
                    blur_amount += 1
                blur_img = cv2.GaussianBlur(sketch_inv, (blur_amount, blur_amount), 0)
                sketch_final = cv2.divide(gray, 255 - blur_img, scale=256)
                self.sketch_image = cv2.cvtColor(sketch_final, cv2.COLOR_GRAY2RGB)

            # Display the results
            self.display_images()

        except Exception as e:
            self.status_label.config(text=f"Eroare la procesare: {str(e)}")

    def display_images(self):
        if self.current_image is None or self.sketch_image is None:
            return

        # Resize for display while maintaining aspect ratio
        max_height = self.original_canvas.winfo_height() - 10
        max_width = self.original_canvas.winfo_width() - 10

        if max_height <= 1 or max_width <= 1:  # Canvas not yet sized
            self.root.update()
            max_height = self.original_canvas.winfo_height() - 10
            max_width = self.original_canvas.winfo_width() - 10

            if max_height <= 1 or max_width <= 1:  # Still not sized properly
                max_height = 400
                max_width = 400

        # Resize original image
        h, w = self.current_image.shape[:2]
        aspect = w / h

        if w > h:
            new_w = min(w, max_width)
            new_h = int(new_w / aspect)
            if new_h > max_height:
                new_h = max_height
                new_w = int(new_h * aspect)
        else:
            new_h = min(h, max_height)
            new_w = int(new_h * aspect)
            if new_w > max_width:
                new_w = max_width
                new_h = int(new_w / aspect)

        # Resize both images
        resized_original = cv2.resize(self.current_image, (new_w, new_h))
        resized_sketch = cv2.resize(self.sketch_image, (new_w, new_h))

        # Convert to PhotoImage
        self.photo_image = ImageTk.PhotoImage(Image.fromarray(resized_original))
        self.photo_sketch = ImageTk.PhotoImage(Image.fromarray(resized_sketch))

        # Update canvases
        self.original_canvas.config(width=new_w, height=new_h)
        self.sketch_canvas.config(width=new_w, height=new_h)

        self.original_canvas.create_image(new_w // 2, new_h // 2, image=self.photo_image)
        self.sketch_canvas.create_image(new_w // 2, new_h // 2, image=self.photo_sketch)

    def save_image(self):
        if self.sketch_image is None:
            self.status_label.config(text="Nu există imagine de salvat!")
            return

        # Open save dialog
        filetypes = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]

        default_name = "sketch_result.jpg"
        if self.image_path:
            base = os.path.basename(self.image_path)
            name, _ = os.path.splitext(base)
            default_name = f"{name}_sketch.jpg"

        filepath = filedialog.asksaveasfilename(
            title="Salvează imaginea",
            filetypes=filetypes,
            defaultextension=".jpg",
            initialfile=default_name
        )

        if not filepath:
            return

        try:
            # Convert back to BGR for saving with OpenCV
            save_img = cv2.cvtColor(self.sketch_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filepath, save_img)
            self.status_label.config(text=f"Imaginea a fost salvată în: {filepath}")
        except Exception as e:
            self.status_label.config(text=f"Eroare la salvare: {str(e)}")

    def reset_params(self):
        # Reset all parameters to default values
        self.edge_param1.set(10)
        self.edge_param2.set(50)
        self.blur_size.set(7)
        self.texture_amount.set(50)
        self.line_thickness.set(1)
        self.effect_type.set("crayon")

        # Update the sketch
        if self.original_image is not None:
            self.update_sketch()

        self.status_label.config(text="Parametri resetați la valorile implicite.")

    def on_closing(self):
        # Handle window close event
        self.root.destroy()


# Run the application
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SketchApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        # Keep console open on error
        if hasattr(sys, 'ps1') or (hasattr(sys, 'ps1') and not hasattr(sys, 'ps2')):
            # If we're in interactive mode, don't pause
            pass
        else:
            # We're not in interactive mode, pause before exit
            input("Press Enter to exit...")