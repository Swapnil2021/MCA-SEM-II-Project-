import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab # type: ignore
import cv2 # type: ignore

class PaintApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Paint App")
        self.setup_ui()
        self.setup_camera_feed()
        self.bind_events()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        toolbar = tk.Frame(self.master)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.color_button = tk.Button(toolbar, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        self.pen_button = tk.Button(toolbar, text="Pen", command=self.use_pen)
        self.pen_button.pack(side=tk.LEFT)

        self.pencil_button = tk.Button(toolbar, text="Pencil", command=self.use_pencil)
        self.pencil_button.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(toolbar, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        self.text_button = tk.Button(toolbar, text="Text", command=self.use_text)
        self.text_button.pack(side=tk.LEFT)

        self.fill_button = tk.Button(toolbar, text="Fill", command=self.fill_canvas)
        self.fill_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(toolbar, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(toolbar, text="Save", command=self.save_traced_image)
        self.save_button.pack(side=tk.LEFT)

        self.size_scale = ttk.Scale(toolbar, from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_pen_size)
        self.size_scale.set(2)
        self.size_scale.pack(side=tk.LEFT)

        self.pen_button.config(relief=tk.SUNKEN)

        self.color = "black"
        self.pen_size = 2
        self.pen_type = "pen"
        self.pen = True
        self.eraser_on = False
        self.text_on = False
        self.fill_on = False
        self.prev_x = None
        self.prev_y = None

    def setup_camera_feed(self):
        self.camera_window = tk.Toplevel(self.master)
        self.camera_window.title("Camera Feed")

        self.camera_canvas = tk.Canvas(self.camera_window, bg="white")
        self.camera_canvas.pack(fill=tk.BOTH, expand=True)

        self.camera_feed()

        add_image_button = tk.Button(self.camera_window, text="Add Image", command=self.add_image)
        add_image_button.pack(side=tk.TOP)

    def bind_events(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.end_paint)
        self.canvas.bind("<Button-1>", self.start_typing)
        self.camera_canvas.bind("<B1-Motion>", self.draw_on_canvas)

    def choose_color(self):
        self.color = colorchooser.askcolor()[1]

    def use_pen(self):
        self.pen_type = "pen"
        self.pen = True
        self.eraser_on = False
        self.text_on = False
        self.fill_on = False
        self.pen_button.config(relief=tk.SUNKEN)
        self.pencil_button.config(relief=tk.RAISED)
        self.eraser_button.config(relief=tk.RAISED)
        self.text_button.config(relief=tk.RAISED)
        self.fill_button.config(relief=tk.RAISED)

    def use_pencil(self):
        self.pen_type = "pencil"
        self.pen = True
        self.eraser_on = False
        self.text_on = False
        self.fill_on = False
        self.pen_button.config(relief=tk.RAISED)
        self.pencil_button.config(relief=tk.SUNKEN)
        self.eraser_button.config(relief=tk.RAISED)
        self.text_button.config(relief=tk.RAISED)
        self.fill_button.config(relief=tk.RAISED)

    def use_eraser(self):
        self.pen = False
        self.eraser_on = True
        self.text_on = False
        self.fill_on = False
        self.pen_button.config(relief=tk.RAISED)
        self.pencil_button.config(relief=tk.RAISED)
        self.eraser_button.config(relief=tk.SUNKEN)
        self.text_button.config(relief=tk.RAISED)
        self.fill_button.config(relief=tk.RAISED)

    def use_text(self):
        self.pen = False
        self.eraser_on = False
        self.text_on = True
        self.fill_on = False
        self.pen_button.config(relief=tk.RAISED)
        self.pencil_button.config(relief=tk.RAISED)
        self.eraser_button.config(relief=tk.RAISED)
        self.text_button.config(relief=tk.SUNKEN)
        self.fill_button.config(relief=tk.RAISED)

    def fill_canvas(self):
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=self.color, outline="")
        self.fill_on = True
        self.pen_button.config(relief=tk.RAISED)
        self.pencil_button.config(relief=tk.RAISED)
        self.eraser_button.config(relief=tk.RAISED)
        self.text_button.config(relief=tk.RAISED)
        self.fill_button.config(relief=tk.SUNKEN)

    def change_pen_size(self, event=None):
        self.pen_size = int(self.size_scale.get())

    def paint(self, event):
        if self.pen:
            x1, y1 = (event.x - self.pen_size), (event.y - self.pen_size)
            x2, y2 = (event.x + self.pen_size), (event.y + self.pen_size)
            if self.pen_type == "pen":
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color, width=self.pen_size)
            elif self.pen_type == "pencil":
                self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill=self.color, width=self.pen_size)
            if self.prev_x is not None and self.prev_y is not None:
                self.camera_canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill=self.color, width=self.pen_size)
            self.prev_x, self.prev_y = event.x, event.y

    def start_typing(self, event):
        if self.text_on:
            self.text_entry = tk.Entry(self.master, bd=0, bg=self.color)
            self.text_entry.place(x=event.x, y=event.y)
            self.text_entry.focus()

    def end_paint(self, event):
        if self.text_on:
            text = self.text_entry.get()
            self.canvas.create_text(event.x, event.y, text=text, fill=self.color)
            self.text_entry.destroy()
        self.prev_x, self.prev_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.camera_canvas.delete("all")

    def save_traced_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            try:
                x = self.canvas.winfo_rootx()
                y = self.canvas.winfo_rooty()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()
                traced_image = ImageGrab.grab(bbox=(x, y, x1, y1))
                traced_image.save(file_path)
                messagebox.showinfo("Success", "Traced image saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving traced image: {e}")

    def camera_feed(self):
        cap = cv2.VideoCapture(0)

        def update():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                self.camera_canvas.img = img
                self.camera_canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.camera_canvas.after(10, update)

        update()

    def draw_on_canvas(self, event):
        if self.pen:
            x1, y1 = (event.x - self.pen_size), (event.y - self.pen_size)
            x2, y2 = (event.x + self.pen_size), (event.y + self.pen_size)
            if self.pen_type == "pen":
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color, width=self.pen_size)
            elif self.pen_type == "pencil":
                self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill=self.color, width=self.pen_size)
            self.prev_x, self.prev_y = event.x, event.y

    def add_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path)
            img = ImageTk.PhotoImage(img)
            self.loaded_image = img  # Store reference to image
            self.camera_canvas.create_image(0, 0, anchor=tk.NW, image=img)

def main():
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
