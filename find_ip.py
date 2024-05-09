import subprocess

def get_connected_devices():
    # Run the arp -a command and capture the output
    arp_output = subprocess.run(["arp", "-a"], capture_output=True, text=True)

    # Split the output by interface sections
    interfaces = arp_output.stdout.split("\n\n")

    connected_devices = {}

    for interface in interfaces:
        lines = interface.strip().split("\n")
        if len(lines) < 3:
            continue  # Skip empty or incomplete sections

        # Extract interface IP address
        interface_ip = lines[0].split()[1]

        # Extract connected devices (IP and MAC addresses)
        devices = {}
        for line in lines[2:]:
            parts = line.split()
            if len(parts) >= 2:
                ip_address = parts[0]
                mac_address = parts[1]
                devices[ip_address] = mac_address

        connected_devices[interface_ip] = devices

    return connected_devices

def find_device_ip(mac_address_to_find):
    connected_devices = get_connected_devices()

    for interfaces,devices in connected_devices.items():
        for ip_address, mac_address in devices.items():
            if mac_address.replace("-", ":") == mac_address_to_find:
                return ip_address

    return None