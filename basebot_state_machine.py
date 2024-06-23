# NOTE: It is recommended to run this code onto Robot Mesh Studio python environment

# Import required components from Library
from vex import (
    Motor,
    Touchled,
    Bumper,
    Ports,
    DistanceUnits,
    ColorHue
)
from vex import (FORWARD, RIGHT, LEFT, REVERSE, DEGREES)
from drivetrain import Drivetrain
import sys


# Initialize the motors plugged into ports 1 & 2 of the brain
motor_right  = Motor(Ports.PORT1, True)  # Reverse Polarity
motor_left   = Motor(Ports.PORT2)

# Initialize Drivetrain
drivetrain = Drivetrain(
    motor_left, motor_right, 
    200, 202, DistanceUnits.MM
)

# Initialize the touch LED
touch_led = Touchled(Ports.PORT10) 
# Initialize the front bumper sensor
bumper_front = Bumper(Ports.PORT6)


state = "IDLE"
while True:
    if state == "IDLE":
        drivetrain.stop()
        touch_led.on_hue(ColorHue.RED)
        
        while True:
            # Change state when the touch LED is pressed
            if touch_led.pressing():
                state = "FORWARD"
                print("Touch LED is pressed.")
                break
    elif state == "FORWARD":
        print("Bot is now on forward state.")
        touch_led.on_hue(ColorHue.GREEN)
        drivetrain.start_drive_for(FORWARD, 50, DistanceUnits.CM, 50)
        
        while True:
            # Change state when driving is done
            if drivetrain.is_done():
                state = "IDLE"
                break
            
            # Change state when the bumper sensor hits an obstacle
            if bumper_front.pressing():
                state = "TURN"
                break
    elif state == "TURN":
        # Stop the drivetrain
        drivetrain.stop()
        # Start turning left 90 degrees
        drivetrain.start_turn_for(LEFT, 90, DEGREES)

        while True:
            # Change state when turning is done
            if drivetrain.is_done():
                state = "IDLE"
                break