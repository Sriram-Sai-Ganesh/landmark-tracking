# TODO: replace calculate-template with this file, after fixing image scaling issues.

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import utils
from skimage import io
class ImageSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Selector")

        root.title("Region selection")
        root.focus()
        HEIGHT = root.winfo_screenwidth()
        WIDTH = root.winfo_screenheight()
        RESOL = str(HEIGHT) + "x" + str(WIDTH+7) + "+" + str(45) + "+" + str(0)
        root.geometry(RESOL)
        # root.tk.call('tk', 'scaling', 2.0)


        self.canvas = tk.Canvas(self.root, cursor="cross", width=600, height=800)
        self.canvas.pack()

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selection = None

        self.load_button = tk.Button(self.root, text="Open Image", command=self.load_image)
        self.load_button.pack()

        self.save_button = tk.Button(self.root, text="Save Selection", command=self.save_selection, state=tk.DISABLED)
        self.save_button.pack()

        self.image = None
        self.img_path = None
        self.crop_count=0

    def load_image(self):
        self.img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if self.img_path:
            self.image = Image.open(self.img_path)
            # self.resize_image()
            self.photo = ImageTk.PhotoImage(self.image)
            # self.photo = self.photo.subsample(2, 2)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.canvas.bind("<ButtonPress-1>", self.start_selection)
            self.canvas.bind("<B1-Motion>", self.draw_selection)
            self.canvas.bind("<ButtonRelease-1>", self.end_selection)

    def start_selection(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        print(f'started drawing at {(event.x, event.y)}')

    def resize_image(self):
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            self.image = self.image.resize((canvas_width, canvas_height), Image.ANTIALIAS)

    def draw_selection(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        if self.selection:
            self.canvas.delete(self.selection)

        self.selection = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", width=2)

    def end_selection(self, event):
        self.save_button.config(state=tk.NORMAL)
        print(f'ended drawing at {(event.x, event.y)}')

    def save_selection(self):
        if self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            x1, y1, x2, y2 = (
                int(min(self.start_x, self.end_x)),
                int(min(self.start_y, self.end_y)),
                int(max(self.start_x, self.end_x)),
                int(max(self.start_y, self.end_y))
            )

            selected_region = self.image.crop((x1, y1, x2, y2))
            save_path = './output/regions/crop_'+str(self.crop_count)+'.png'

            if save_path:
                selected_region.save(save_path)
                self.crop_count+=1
                self.save_button.config(state=tk.DISABLED)

def runImageSelector():
    root = tk.Tk()
    
    app = ImageSelector(root)
    root.mainloop()


def save_template_from_image(imgpath, startx, starty, endx, endy, origin='tl', savepath='./output/regions/cropped.png'):
    img=io.imread(imgpath)
    template=utils.get_image_region(img, startx, starty, endx, endy, 'tl')
    io.imsave(savepath, template)


if __name__ == "__main__":
    runImageSelector()