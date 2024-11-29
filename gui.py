import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import main

class App:
    def __init__(self, root):
        self.root = root
        root.title("Camera Application")
        root.attributes('-fullscreen', True)
        self.create_buttons()

    def create_buttons(self):
        ft = tkFont.Font(family='Times', size=10)

        button_y = 0.4  # Vertical position of the first button

        GButton_339 = tk.Button(self.root, text="Click a Pic", font=ft, command=main.capture)
        GButton_339.place(relx=0.5, rely=button_y, anchor=tk.CENTER, width=200, height=30)

        GButton_489 = tk.Button(self.root, text="Upload to Google Drive", font=ft, command=main.upload_image)
        GButton_489.place(relx=0.5, rely=button_y + 0.1, anchor=tk.CENTER, width=200, height=30)

        GButton_249 = tk.Button(self.root, text="Generate QR Code", font=ft, command=main.generate_qr)
        GButton_249.place(relx=0.5, rely=button_y + 0.2, anchor=tk.CENTER, width=200, height=30)

        GButton_610 = tk.Button(self.root, text="Exit", font=ft, command=self.exit_app)
        GButton_610.place(relx=0.5, rely=button_y + 0.3, anchor=tk.CENTER, width=200, height=30)

    def exit_app(self):        
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()