import customtkinter
import time
import pkg_resources
import json
import os
from PIL import Image, ImageTk
from version import check_for_updates

class Settings(customtkinter.CTkToplevel):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        check_for_updates(self)

        self.attributes("-topmost", True) # set the window always on top

        # Gui
        self.title("Settings") # Windows titel
        self.minsize(300, 250) # minimum size from the window length, height
        self.geometry("300x300") # startup size from the window
        #window.iconbitmap("assets/icon/ethernet.ico") # set the icon from the window
        #customtkinter.set_default_color_theme("blue") # set default color theme

        # set main grid layout 1x2
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.transparency_label = customtkinter.CTkLabel(self, text="Set the transparency from the window")
        self.transparency_label.grid(row=1, column=0, padx=20, pady=5)

        self.transparency_slider = customtkinter.CTkSlider(self, from_=0.1, to=1.0, number_of_steps=9, orientation="horizontal", hover=bool, command=self.save_transparency_value)
        self.transparency_slider.grid(row=2, column=0, padx=20, pady=5)
        self.load_transparency_value()


    def save_transparency_value(self, value):
        transparency_value = float(value)

        # Speichern des Werts in einer JSON-Datei
        output_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Skyfay', 'MoveableWindowsTime')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'settings.json')

        data = {
            'transparency_value': transparency_value
        }

        with open(output_file, 'w') as f:
            json.dump(data, f)

    def load_transparency_value(self):
        # Laden des Werts aus der JSON-Datei
        output_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Skyfay', 'MoveableWindowsTime')
        output_file = os.path.join(output_dir, 'settings.json')

        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                data = json.load(f)
                transparency_value = data.get('transparency_value', 0.0)

                # Setzen des Werts im Schieberegler
                self.transparency_slider.set(transparency_value)
        else:
            data = {'transparency_value': 0.8}
            os.makedirs(output_dir, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(data, f)

            transparency_value = 0.8
            self.transparency_slider.set(transparency_value)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("")
        self.configure(bg="#2b2d30")
        self.configure(background="#2b2d30")
        self.minsize(225, 175)  # minimum size from the window length, height
        self.maxsize(250, 200)  # Maximale Größe des Fensters (Länge, Höhe)
        self.geometry("225x175")  # startup size from the window
        customtkinter.set_default_color_theme("green")


        # icon
        icon_path = pkg_resources.resource_filename(__name__, "assets/time.ico")
        self.iconbitmap(icon_path)

        # images
        settings_image = pkg_resources.resource_filename(__name__, "assets/settings_light.png")
        # Öffnen des Bildes mit PIL und Erzeugen des Image-Objekts
        settings_image = Image.open(settings_image)
        self.settings_image = customtkinter.CTkImage(settings_image, size=(20, 20))


        self.time_label = customtkinter.CTkLabel(self, font=("Arial", 40))
        self.time_label.pack(padx=20, pady=10)

        self.date_label = customtkinter.CTkLabel(self, font=("Arial", 15), fg_color="#4d5056", corner_radius=10)
        self.date_label.pack(padx=20, pady=10)

        self.fix_position_button = customtkinter.CTkButton(self, text="Fix window", command=self.fix_position)
        self.fix_position_button.pack(side="right", padx=10, pady=10)

        self.settings_button = customtkinter.CTkButton(self, text="", image=self.settings_image, command=self.open_settings_window)
        self.settings_button.pack(side="left", padx=10, pady=10)

        self.window_fixed = False

        self.update_clock()

        self.toplevel_window = None

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d-%m-%Y")
        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)
        self.after(1000, self.update_clock)

    def fix_position(self):
        # Laden des Werts aus der JSON-Datei
        output_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Skyfay', 'MoveableWindowsTime')
        output_file = os.path.join(output_dir, 'settings.json')

        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                data = json.load(f)
                transparency_value = data.get('transparency_value', 0.0)
        else:
            data = {'transparency_value': 0.8}
            os.makedirs(output_dir, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(data, f)

            transparency_value = 0.8

        if self.window_fixed:
            self.attributes("-topmost", False)
            self.attributes("-toolwindow", False)
            self.overrideredirect(False)
            self.attributes("-alpha", 1.0)
            self.fix_position_button.configure(text="Fix Window")
            self.fix_position_button.pack(side="right")
            self.settings_button.pack(side="right", padx=10, pady=10) # add the button again

        else:
            self.attributes("-topmost", True)
            self.attributes("-toolwindow", True)
            self.overrideredirect(True)
            self.attributes("-alpha", transparency_value)
            self.fix_position_button.configure(text="Detach")
            self.fix_position_button.pack(side="bottom")
            self.settings_button.pack_forget()

        self.window_fixed = not self.window_fixed

    def open_settings_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
           self.toplevel_window = Settings(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

if __name__ == "__main__":
    app = App()
    app.mainloop()