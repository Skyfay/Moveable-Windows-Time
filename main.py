import customtkinter
import time
import pkg_resources
from PIL import Image, ImageTk


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("")
        self.configure(bg="#2b2d30")
        self.configure(background="#2b2d30")
        self.minsize(225, 175)  # minimum size from the window length, height
        self.geometry("225x175")  # startup size from the window
        customtkinter.set_default_color_theme("green")

        # images
        settings_image = pkg_resources.resource_filename(__name__, "assets/settings_light.png")
        # Öffnen des Bildes mit PIL und Erzeugen des Image-Objekts
        settings_image = Image.open(settings_image)
        self.settings_image = customtkinter.CTkImage(settings_image, size=(20, 20))

        # icon
        icon_path = pkg_resources.resource_filename(__name__, "assets/time.ico")
        self.iconbitmap(icon_path)

        self.time_label = customtkinter.CTkLabel(self, font=("Arial", 40))
        self.time_label.pack(padx=20, pady=10)

        self.date_label = customtkinter.CTkLabel(self, font=("Arial", 15), fg_color="#4d5056", corner_radius=10)
        self.date_label.pack(padx=20, pady=10)

        self.settings_button = customtkinter.CTkButton(self, text="Fix window", command=self.fix_position)
        self.settings_button.pack(side="right", padx=10, pady=10)

        self.fix_position_button = customtkinter.CTkButton(self, text="", image=self.settings_image)
        self.fix_position_button.pack(side="left", padx=10, pady=10)

        self.window_fixed = False

        self.update_clock()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d-%m-%Y")
        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)
        self.after(1000, self.update_clock)

    def fix_position(self):
        if self.window_fixed:
            self.attributes("-topmost", False)
            self.attributes("-toolwindow", False)
            self.overrideredirect(False)
            self.attributes("-alpha", 1.0)
            self.settings_button.configure(text="Fix Window")
            self.settings_button.pack(side="right")
            self.fix_position_button.pack(side="right", padx=10, pady=10) # add the button again

        else:
            self.attributes("-topmost", True)
            self.attributes("-toolwindow", True)
            self.overrideredirect(True)
            self.attributes("-alpha", 0.8)
            self.settings_button.configure(text="Detach")
            self.settings_button.pack(side="bottom")
            self.fix_position_button.pack_forget()

        self.window_fixed = not self.window_fixed


if __name__ == "__main__":
    app = App()
    app.mainloop()
