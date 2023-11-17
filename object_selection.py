from skimage import io
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


import utils
import frame_cap


img_file_path='./output/caps/baseline.png'
template_file_path='./output/regions/template.png'


class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Selector")

        self.display_scale_factor=0.7
        self.crop_count=0
        # Canvas to display the image:
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)

        # UI elements:
        self.open_button = tk.Button(root, text="Open Image", command=self.open_image)
        
        self.filename_box = tk.Text(root, height = 1, width = 15)
        
        self.save_button = tk.Button(root, text="Save Template", command=self.save_selection)
        self.save_button.config(state=tk.DISABLED)
        
        self.recapture_button = tk.Button(root, text="Recapture imge", command=self.recapture)
        self.recapture_button.config(state=tk.ACTIVE)

        self.open_button.pack()
        self.filename_box.pack()
        self.save_button.pack()
        self.recapture_button.pack()

        self.img_file_path=img_file_path
        self.template_file_path=template_file_path

        # Binding mouse events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)


    def open_image(self):
        # Open a file dialog to choose an image
        self.img_file_path = filedialog.askopenfilename()
        
        # If a file is selected, load and display the image
        if self.img_file_path:
            image = Image.open(self.img_file_path)


            image = image.resize((int(image.width*self.display_scale_factor), int(image.height*self.display_scale_factor)), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(image=image)

            self.canvas.config(width=self.img.width(), height=self.img.height())
            self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    # save rectangle created by user
    def save_selection(self):
        if self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            self.save_button.config(state=tk.DISABLED)

            x1, y1, x2, y2 = map(lambda x:int(x/self.display_scale_factor), [
                min(self.start_x, self.end_x),
                min(self.start_y, self.end_y),
                max(self.start_x, self.end_x),
                max(self.start_y, self.end_y)
            ])
            save_path = './output/regions/'
            user_input=self.filename_box.get("1.0",'end-1c').replace(' ','_')
            
            if not user_input:
                save_path+='crop_'+str(self.crop_count)
                self.crop_count+=1
            else:
                save_path+=user_input

            save_path+='.png'
            origin='tl'
            img=io.imread(self.img_file_path)
            template=utils.get_image_region(img, x1, y1, x2, y2, origin)
            io.imsave(save_path, template)


    def on_press(self, event):
        # Record the starting coordinates of the rectangle
        self.save_button.config(state=tk.DISABLED)
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_drag(self, event):
        # Update the end coordinates of the rectangle while dragging
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        # Delete any previous rectangle and draw the new one
        self.canvas.delete("rect")
        self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline="green", tags="rect"
        )

    def on_release(self, event):
        # image is saved only if the 'save' button is pressed, not on mouse button release.
        self.save_button.config(state=tk.ACTIVE)

    def recapture(self):
        print('recapturing...')
        frame_cap.capture_calibration_image(self.img_file_path)
        self.open_image()


def run():
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()