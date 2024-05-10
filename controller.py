import tkinter as tk
from tkinter import messagebox
from hand_control import HandTrackingController
from keyboard_control import KeyboardController
import popup_box

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
        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        self.root.geometry("350x150")
        # Create a frame inside the root window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Hand Gesture Control Button
        hand_icon = tk.PhotoImage(file="Assets/gesturecontrol.png")
        hand_icon = hand_icon.subsample(2)
        self.hand_control_button = tk.Button(button_frame, image=hand_icon, command=self.start_hand_control, borderwidth=2, relief="solid")
        self.hand_control_button.image = hand_icon
        self.hand_control_button.pack(side=tk.LEFT, padx=5)

        # Keyboard Control Button
        keyboard_icon = tk.PhotoImage(file="Assets/keyboard.png")
        keyboard_icon = keyboard_icon.subsample(2)
        self.keyboard_control_button = tk.Button(button_frame, image=keyboard_icon, command=self.start_keyboard_control, borderwidth=2, relief="solid")
        self.keyboard_control_button.image = keyboard_icon
        self.keyboard_control_button.pack(side=tk.LEFT, padx=5)

        # Quit Button
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
    popup_box.popup()
    esp_ip = find_ip.find_device_ip("48:55:19:f6:57:34")
    app = ControlGUI(f"ws://{esp_ip}:8080/")
    app.root.mainloop()
