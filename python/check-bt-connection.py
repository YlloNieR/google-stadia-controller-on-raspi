__author__ = "YlloNieR"
__version__ = "0.0.1"
__date__ = "2024-10-19"
__description__ = "This script Allows to check if the Stadia Controller is connected with Bluetooth and got an own /dev/input/eventX."

import subprocess

def is_stadia_controller_connected():
    # Run bluetoothctl to list connected devices
    try:
        output = subprocess.check_output(["bluetoothctl", "devices"], text=True)
        stadia_device_name = "Stadia"
        
        # Check if any connected device contains the name "Stadia"
        for line in output.splitlines():
            if stadia_device_name in line:
                device_mac = line.split()[1]  # Extract the MAC address
                # Check if the device is connected
                device_info = subprocess.check_output(["bluetoothctl", "info", device_mac], text=True)
                if "Connected: yes" in device_info:
                    print("🎮 Stadia controller is connected! ✅")
                    return True
        print("❌ Stadia controller is not connected.")
        return False
    except subprocess.CalledProcessError:
        print("⚠️ Error occurred while checking Bluetooth devices.")
        return False

if __name__ == "__main__":
    is_stadia_controller_connected()
