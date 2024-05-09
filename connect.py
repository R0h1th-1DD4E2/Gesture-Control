import websocket
import time

# Define the WebSocket server URL
ws_url = "ws://192.168.137.13:8080/"

# Number of packets to send
num_packets = 1000

# Counter to keep track of sent packets
packet_count = 0

# Callback function to handle WebSocket messages
def on_message(ws, message):
    print("Received message:", message)

# Callback function to handle WebSocket connection status
def on_open(ws):
    print("WebSocket connection established")
    # Send packets with a delay between each message
    global packet_count
    for i in range(num_packets):
        ws.send("{}".format(packet_count))
        packet_count += 1
        time.sleep(0.02)
        print(packet_count)

# Callback function to handle WebSocket close event
def on_close(ws):
    print("WebSocket connection closed")

# Create a WebSocket connection
ws = websocket.WebSocketApp(ws_url,
                            on_message=on_message,
                            on_open=on_open,
                            on_close=on_close)

# Run the WebSocket client
ws.run_forever()
