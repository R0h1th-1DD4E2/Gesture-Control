import tkinter as tk
from tkinter import messagebox
from hand_control import HandTrackingController
from keyboard_control import KeyboardController

# Import Custom Functions
import find_ip

class ControlGUI:
    def __init__(self, esp_ip):
        self.root = tk.Tk()
        self.root.title("Bot Control")
        self.hand_tracking_controller = HandTrackingController(esp_ip)
        self.keyboard_controller = KeyboardController(esp_ip)

        self.create_widgets()

    def create_widgets(self):
        self.hand_control_button = tk.Button(self.root, text="Hand Gesture Control", command=self.start_hand_control)
        self.hand_control_button.pack(pady=10)

        self.keyboard_control_button = tk.Button(self.root, text="Keyboard Control", command=self.start_keyboard_control)
        self.keyboard_control_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_program)
        self.quit_button.pack(pady=5)

    def start_hand_control(self):
        self.hand_tracking_controller.run(True)
        self.keyboard_controller.run(False)

    def start_keyboard_control(self):
        self.hand_tracking_controller.run(False)
        self.keyboard_controller.run(True)

    def quit_program(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.hand_tracking_controller.stop_gesture_tracking()
            self.root.destroy()

if __name__ == "__main__":
    # ESP address
    esp_ip = find_ip.find_device_ip("48:55:19:f6:57:34")
    app = ControlGUI(f"ws://{esp_ip}:8080/")
    app.root.mainloop()
