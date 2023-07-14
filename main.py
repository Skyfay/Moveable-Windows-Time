import customtkinter
import time
import pkg_resources
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("")
        self.configure(bg="#2b2d30")
        self.configure(background="#2b2d30")
        self.minsize(100, 100)
        # Setzen des Fenstericons
        customtkinter.set_default_color_theme("green")

        # Pfad zum Icon innerhalb der ausführbaren Datei
        icon_path = pkg_resources.resource_filename(__name__, "assets/time.ico")

        # Setzen des Fenstericons
        self.iconbitmap(icon_path)


        # Zeitlabel erstellen
        self.time_label = customtkinter.CTkLabel(self, font=("Arial", 40))
        self.time_label.pack(padx=20, pady=10)

        # Datumslabel erstellen
        self.date_label = customtkinter.CTkLabel(self, font=("Arial", 15), fg_color="#4d5056", corner_radius=10)
        self.date_label.pack(padx=20, pady=10)

        # Button erstellen
        self.fix_position_button = customtkinter.CTkButton(self, text="Fix window", command=self.fix_position)
        self.fix_position_button.pack(pady=10)

        self.window_fixed = False

        # Uhr starten
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
            self.fix_position_button.configure(text="Fix Window")
        else:
            self.attributes("-topmost", True)
            self.attributes("-toolwindow", True)
            self.overrideredirect(True)
            self.attributes("-alpha", 0.8)
            self.fix_position_button.configure(text="Detach")

        self.window_fixed = not self.window_fixed


if __name__ == "__main__":
    app = App()
    app.mainloop()
