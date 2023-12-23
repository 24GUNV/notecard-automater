from PIL import Image, ImageTk
import tkinter as tk
from tkfontchooser import askfont
from tkinter.colorchooser import askcolor
from tkinter import ttk
from ttkthemes import ThemedStyle

class ImageClickApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Image Click App")

        self.load_image(image_path)
        self.create_widgets()

        self.selected_value = None
        self.text_boxes = {}  # Dictionary to store text box widgets

    def load_image(self, image_path):
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(root, image=self.photo)
        self.label.grid(row=0, column=0, columnspan=7)

    def create_widgets(self):
        style = ThemedStyle(self.root)
        style.set_theme("arc")  # Choose a theme from the available options

        self.create_buttons()

        self.create_font_buttons()

        self.create_done_button()

    def create_buttons(self):
        self.value_buttons = {}
        values = [
            "Receiver Line",
            "Sender Line",
            "1st Message Line",
            "2nd Message Line",
            "Max Length per Line",  
        ]
        for i, value in enumerate(values):
            button = self.create_button(value)
            self.value_buttons[value] = button
            row = i // 3 + 1
            col = i % 3
            button.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def create_font_buttons(self):
        self.font_button = ttk.Button(self.root, text="Choose Font", command=self.choose_font)
        self.font_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.font_color_button = ttk.Button(self.root, text="Choose Font Color", command=self.choose_font_color)
        self.font_color_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    def create_button(self, text, command=None):
        button = ttk.Button(self.root, text=text, command=command)
        return button

    def create_done_button(self):
        self.done_button = ttk.Button(root, text="Done", command=self.root.quit)
        self.done_button.grid(row=3, column=6, padx=10, pady=20, sticky="e")

    def choose_font(self):
        font = askfont(self.root)
        if font:
            self.font = (font['family'], font['size'])
            if self.selected_value:
                self.update_text_box(self.selected_value)

    def choose_font_color(self):
        color = askcolor(color=self.font_color)[1]
        if color:
            self.font_color = color
            if self.selected_value:
                self.update_text_box(self.selected_value)

    def update_text_box(self, button_name):
        if button_name in self.text_boxes:
            text_box = self.text_boxes[button_name]
            text_box.configure(font=self.font, fg=self.font_color)
            text_box.delete(0, tk.END)
            text_box.insert(0, button_name)

    def start_app(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")

    # Provide the path to your image
    image_path = "templates/note-card-template-resized.png"

    app = ImageClickApp(root, image_path)
    app.start_app()
