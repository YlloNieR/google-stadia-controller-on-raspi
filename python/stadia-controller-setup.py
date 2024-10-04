import evdev
import uinput
from evdev import InputDevice, categorize, ecodes

# Uses '/dev/input/event5' for the Stadia controller
controller = InputDevice("/dev/input/event5")

# uinput setup for mouse control (left/right mouse button and movements)
device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT])

# Define the deadzone for the joystick (how much movement is ignored)
DEADZONE = 10  # Area around the center that is ignored
MOVEMENT_SPEED = 5  # Reduce the movement speed of the mouse

print("Listening for events from the controller...")

for event in controller.read_loop():
    # Movement of the left joystick - X and Y axes
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        if absevent.event.code == ecodes.ABS_X:
            # Left joystick - X-axis (movement left/right)
            if (
                abs(absevent.event.value - 128) > DEADZONE
            ):  # Movement only if outside the deadzone
                if absevent.event.value > 130:  # Movement to the right
                    device.emit(uinput.REL_X, MOVEMENT_SPEED)
                    device.syn()  # Synchronize the input
                elif absevent.event.value < 125:  # Movement to the left
                    device.emit(uinput.REL_X, -MOVEMENT_SPEED)
                    device.syn()  # Synchronize the input
        elif absevent.event.code == ecodes.ABS_Y:
            # Left joystick - Y-axis (movement up/down)
            if (
                abs(absevent.event.value - 128) > DEADZONE
            ):  # Movement only if outside the deadzone
                if absevent.event.value > 130:  # Movement downwards
                    device.emit(uinput.REL_Y, MOVEMENT_SPEED)
                    device.syn()  # Synchronize the input
                elif absevent.event.value < 125:  # Movement upwards
                    device.emit(uinput.REL_Y, -MOVEMENT_SPEED)
                    device.syn()  # Synchronize the input

    # Check for buttons for mouse actions
    elif event.type == ecodes.EV_KEY:
        if (
            event.code == ecodes.BTN_SOUTH and event.value == 1
        ):  # A button (BTN_SOUTH) as left mouse button
            print("A button pressed -> Left click")
            device.emit(uinput.BTN_LEFT, 1)
            device.syn()  # Synchronize the input
        elif event.code == ecodes.BTN_SOUTH and event.value == 0:  # A button released
            print("A button released -> Release left click")
            device.emit(uinput.BTN_LEFT, 0)
            device.syn()  # Synchronize the input

        if (
            event.code == ecodes.BTN_EAST and event.value == 1
        ):  # B button (BTN_EAST) as right mouse button
            print("B button pressed -> Right click")
            device.emit(uinput.BTN_RIGHT, 1)
            device.syn()  # Synchronize the input
        elif event.code == ecodes.BTN_EAST and event.value == 0:  # B button released
            print("B button released -> Release right click")
            device.emit(uinput.BTN_RIGHT, 0)
            device.syn()  # Synchronize the input

        # Exit with the ESC key (Escape) for a clean termination
        if event.code == ecodes.KEY_ESC and event.value == 1:
            print("ESC key pressed -> Exiting")
            break
