__author__ = "YlloNieR"
__version__ = "0.0.1"
__date__ = "2024-10-19"
__description__ = "This script Allows to move the Mouse and click."

import evdev
import time
import uinput
import subprocess
from evdev import InputDevice, categorize, ecodes

# Uses '/dev/input/event5' for the Stadia controller
controller = InputDevice("/dev/input/event5")

# uinput setup for mouse control (left/right mouse button and movements, and keyboard keys)
device = uinput.Device([
    uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT,
    uinput.KEY_LEFTALT, uinput.KEY_TAB
])

# Define the deadzone for the joystick
DEADZONE = 5  # Reduced deadzone for higher sensitivity
MAX_MOVEMENT = 20  # Maximum movement speed

print("Listening for events from the controller...")

def calculate_movement(value, center, deadzone, max_movement):
    # Calculate the offset from the center position
    offset = value - center
    # Ignore movements inside the deadzone
    if abs(offset) <= deadzone:
        return 0
    # Scale the movement speed based on the offset
    # Use a factor to scale smoothly up to the max movement speed
    scale = (abs(offset) - deadzone) / (128 - deadzone)
    movement = int(scale * max_movement)
    # Apply direction based on whether it's positive or negative
    return movement if offset > 0 else -movement

# Center value for analog stick (typically 128 for an 8-bit joystick)
CENTER = 128

for event in controller.read_loop():
    # Movement of the left joystick - X and Y axes
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        if absevent.event.code == ecodes.ABS_X:
            # Calculate the X movement
            movement_x = calculate_movement(absevent.event.value, CENTER, DEADZONE, MAX_MOVEMENT)
            if movement_x != 0:
                device.emit(uinput.REL_X, movement_x)
                device.syn()  # Synchronize the input
        elif absevent.event.code == ecodes.ABS_Y:
            # Calculate the Y movement
            movement_y = calculate_movement(absevent.event.value, CENTER, DEADZONE, MAX_MOVEMENT)
            if movement_y != 0:
                device.emit(uinput.REL_Y, movement_y)
                device.syn()  # Synchronize the input

    # Check for buttons for mouse actions
    elif event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_SOUTH and event.value == 1:  # A button pressed
            print("A button pressed -> Left click")
            device.emit(uinput.BTN_LEFT, 1)
            device.syn()  # Synchronize the input
        elif event.code == ecodes.BTN_SOUTH and event.value == 0:  # A button released
            print("A button released -> Release left click")
            device.emit(uinput.BTN_LEFT, 0)
            device.syn()  # Synchronize the input

        if event.code == ecodes.BTN_EAST and event.value == 1:  # B button pressed
            print("B button pressed -> Right click")
            device.emit(uinput.BTN_RIGHT, 1)
            device.syn()  # Synchronize the input
        elif event.code == ecodes.BTN_EAST and event.value == 0:  # B button released
            print("B button released -> Release right click")
            device.emit(uinput.BTN_RIGHT, 0)
            device.syn()  # Synchronize the input

        # Open Chromium when the START button (BTN_START) is pressed
        if event.code == ecodes.BTN_START and event.value == 1:
            print("Start button pressed -> Opening Chromium")
            subprocess.Popen(["chromium-browser"])  # Launch Chromium

        # Simulate ALT + TAB + TAB when BTN_TR is pressed
        if event.code == ecodes.BTN_TR and event.value == 1:
            print("BTN_TR pressed -> Switching window")
            # Simulate ALT + TAB + TAB using uinput
            device.emit(uinput.KEY_LEFTALT, 1)  # Press ALT
            device.emit(uinput.KEY_TAB, 1)      # Press TAB
            time.sleep(0.05)                    # Small delay
            device.syn()                        # Synchronize the input
            device.emit(uinput.KEY_TAB, 0)      # Release TAB
            device.emit(uinput.KEY_LEFTALT, 0)  # Release ALT
            device.syn()                        # Synchronize the input

        # Simulate ALT + SHIFT + TAB for backward (left) window switching
        if event.code == ecodes.BTN_TL and event.value == 1:  # Example button for backward switching
            print("BTN_TL pressed -> Switching to the previous window")
            device.emit(uinput.KEY_LEFTALT, 1)   # Press ALT
            device.emit(uinput.KEY_LEFTSHIFT, 1) # Press SHIFT
            device.emit(uinput.KEY_LEFTALT, 1)   # Hold ALT
            time.sleep(0.05)                     # Small delay

            device.emit(uinput.KEY_TAB, 1)       # Press TAB
            device.emit(uinput.KEY_TAB, 0)       # Release TAB
            device.syn()                         # Synchronize the input

            device.emit(uinput.KEY_LEFTSHIFT, 0) # Release SHIFT
            device.emit(uinput.KEY_LEFTALT, 0)   # Release ALT
            device.emit(uinput.KEY_LEFTALT, 0)   # Release ALT
            device.syn()                         # Synchronize the input


    	# Simulate ALT + F4 when BTN_NORTH is pressed
        # if event.code == ecodes.BTN_NORTH and event.value == 1:
        #     print("BTN_NORTH pressed -> Closing the current window")
        #     # Simulate pressing ALT
        #     device.emit(uinput.KEY_LEFTALT, 1)  # Press ALT

        #     # Simulate pressing F4
        #     device.emit(uinput.KEY_F4, 1)       # Press F4

        #     # Simulate releasing F4
        #     device.emit(uinput.KEY_F4, 0)       # Release F4

        #     # Simulate releasing ALT
        #     device.emit(uinput.KEY_LEFTALT, 0)  # Release ALT
        #     device.syn()                        # Synchronize the input

        # Stop the script when the Assitant button (BTN_TRIGGER_HAPPY1) is pressed
        if event.code == ecodes.BTN_TRIGGER_HAPPY1 and event.value == 1:
            print("Assitant button pressed -> Exiting")
            break

        # Exit with the ESC key for a clean termination
        if event.code == ecodes.KEY_ESC and event.value == 1:
            print("ESC key pressed -> Exiting")
            break
