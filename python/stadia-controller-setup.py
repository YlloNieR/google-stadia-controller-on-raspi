import evdev
import uinput
from evdev import InputDevice, categorize, ecodes

# Uses '/dev/input/event5' for the Stadia controller
controller = InputDevice("/dev/input/event5")

# uinput setup for mouse control (left/right mouse button and movements)
device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT])

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

        # Exit with the ESC key for a clean termination
        if event.code == ecodes.KEY_ESC and event.value == 1:
            print("ESC key pressed -> Exiting")
            break
