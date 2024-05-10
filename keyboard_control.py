import keyboard
import time
import websocket

# Custom Functions
import find_ip

class KeyboardController:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.ws = websocket.WebSocket()
        self.ws.connect(ws_url)
        self.pwm = 100

    def increase_pwm(self):
        self.pwm += 10
        if self.pwm > 255:
            self.pwm = 255

    def decrease_pwm(self):
        self.pwm -= 10
        if self.pwm < 50:
            self.pwm = 50

    def send_command(self, command, pwm_values):
        message = f"{command} {' '.join(map(str, pwm_values))}"
        self.ws.send(message)

    def run(self):
        while True:
            if keyboard.is_pressed('q'):
                break
            elif keyboard.is_pressed('w') and keyboard.is_pressed('d'):
                self.send_command('DFRT', [self.pwm, self.pwm, self.pwm, self.pwm])  # Forward Right
            elif keyboard.is_pressed('w') and keyboard.is_pressed('a'):
                self.send_command('DFLT', [self.pwm, self.pwm, self.pwm, self.pwm])  # Forward Left
            elif keyboard.is_pressed('s') and keyboard.is_pressed('d'):
                self.send_command('DWRT', [self.pwm, self.pwm, self.pwm, self.pwm])  # Backward Right
            elif keyboard.is_pressed('s') and keyboard.is_pressed('a'):
                self.send_command('DWLT', [self.pwm, self.pwm, self.pwm, self.pwm])  # Backward Left
            elif keyboard.is_pressed('w'):
                self.send_command('FWD', [self.pwm, self.pwm, self.pwm, self.pwm])  # Forward
            elif keyboard.is_pressed('s'):
                self.send_command('BWD', [self.pwm, self.pwm, self.pwm, self.pwm])  # Backward
            elif keyboard.is_pressed('a'):
                self.send_command('LT', [self.pwm, self.pwm, self.pwm, self.pwm])   # Left
            elif keyboard.is_pressed('d'):
                self.send_command('RT', [self.pwm, self.pwm, self.pwm, self.pwm])   # Right
            elif keyboard.is_pressed(' '):
                self.send_command('STP', [0, 0, 0, 0])   # Stop
            elif keyboard.is_pressed('up'):
                self.increase_pwm()  # Increase PWM
            elif keyboard.is_pressed('down'):
                self.decrease_pwm()  # Decrease PWM

            time.sleep(0.05)

# ESP address
esp_ip = find_ip.find_device_ip("48:55:19:f6:57:34")

# To use Keyboard control
def run(flag=False):
    # Create KeyboardController instance and run it
    if flag:
        controller = KeyboardController(f"ws://{esp_ip}:8080/")
        controller.run()
