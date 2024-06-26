# NOTE: It is recommended to run this code onto Robot Mesh Studio python environment

# Import required modules
from vex import (
    Ports, BrakeType, FORWARD, PERCENT, REVERSE, SECONDS, DEGREES
)
import timer
import vex

# Initialize robot parts
brain = vex.Brain()
ctl = vex.Controller()
ctl.set_deadband(3)

bumper = vex.Bumper(Ports.PORT5)
color = vex.Colorsensor(Ports.PORT3)
touchled = vex.Touchled(Ports.PORT2)

left_motor = vex.Motor(Ports.PORT1)          # left motor
right_motor = vex.Motor(Ports.PORT6, True)   # right motor, reverse polarity

timer_catapult = timer.Timer()

catapult_motor = vex.Motor(Ports.PORT4)



isLoaded = False

def display(statusText=None):
    print
    global isLoaded
    status = ''
    
    if (isLoaded): status = 'Loaded'
    elif (not statusText == None): status = statusText
    else: status = 'Launched'
    
    brain.screen.print_line(1, "FLING v2.0")
    brain.screen.print_line(2, "Status: " + status)
    brain.screen.print_line(4, "DOWN/F Down: Load")
    brain.screen.print_line(5, "CHECK/F Up: Launch")
    pass

def stop_drivetrain():
    left_motor.stop()
    right_motor.stop()


def lower_or_raise_catapult_by_controller(catapult_motor_velocity_percent=50):
    global isLoaded
    if (not isLoaded) and (ctl.buttonFDown.pressing() or brain.buttonDown.pressing()):
        stop_drivetrain()
        while not bumper.pressing():
            catapult_motor.spin(REVERSE, catapult_motor_velocity_percent)
        catapult_motor.stop(BrakeType.HOLD)
        isLoaded = True
        pass
    if (isLoaded) and (ctl.buttonFUp.pressing() or brain.buttonCheck.pressing()):
        stop_drivetrain()
        catapult_motor.spin_for(REVERSE, 490, DEGREES, catapult_motor_velocity_percent)
        isLoaded = False
        pass

# Use controller to drive with 2 joysticks A and D
def drive_by_controller():
    left_motor.spin(FORWARD, ctl.axisA.position(), PERCENT)
    right_motor.spin(FORWARD, ctl.axisD.position(), PERCENT)
    pass



while True:
    display()
    lower_or_raise_catapult_by_controller()
    drive_by_controller()

