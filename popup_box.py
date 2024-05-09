import tkinter as tk

def on_continue_click(window):
    # Close
    window.destroy()

def popup():
    # Create the main window
    root = tk.Tk()
    root.title("Hand Tracking Reminder")

    # Message
    message = "Please keep your hand 25 to 30 cm from the Camera for better tracking."
    label = tk.Label(root, text=message)
    label.pack(padx=20, pady=20)

    # Continue button
    continue_button = tk.Button(root, text="Continue", command=lambda: on_continue_click(root))
    continue_button.pack(padx=20, pady=10)

    # Run window
    root.mainloop()

