# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Alex and Carlos                                              #
# 	Created:      9/13/2025, 1:03:13 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

# Brain configuration
brain = Brain()

# EXP Controller configuration
controller = Controller(PRIMARY)

# Inertial sensor configuration (CRITICAL FOR AUTONOMOUS!)
inertial_sensor = Inertial(Ports.PORT12)

# Motor configuration (6 motors on different ports)
# Left motors: Ports 13-15, Right motors: Ports 16-18 for better wire management
# FIXED: Using external gears (36-tooth to 48-tooth = 1.33:1 ratio)
motor1 = Motor(Ports.PORT13, False, True)   # Left front (reversed, no cartridge)
motor2 = Motor(Ports.PORT16, False, False)  # Right front (no cartridge)
motor3 = Motor(Ports.PORT14, False, True)   # Left middle (reversed, no cartridge)
motor4 = Motor(Ports.PORT17, False, False)  # Right middle (no cartridge)
motor5 = Motor(Ports.PORT15, False, True)   # Left back (reversed, no cartridge)
motor6 = Motor(Ports.PORT18, False, False)  # Right back (no cartridge)

# Motor groups for easier control (assuming 6-wheel drive)
left_motors = MotorGroup(motor1, motor3, motor5)   # Ports 13, 14, 15
right_motors = MotorGroup(motor2, motor4, motor6)  # Ports 16, 17, 18

left_motors.set_stopping(BRAKE)
right_motors.set_stopping(BRAKE)
# Intake/Outtake mechanism motors
intake_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)  # Intake mechanism on port 5
intake_motor2 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)   # Secondary intake motor on port 6 (reversed)
outtake_motor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)  # Outtake mechanism on port 4

# Robot physical constants (measured for your specific robot)
WHEEL_DIAMETER = 3.25  # inches - wheel diameter
WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi
TRACK_WIDTH = 12.5  # inches - ACTUAL measured wheel center to center distance

# FIXED: External gear ratio (36-tooth motor gear to 48-tooth wheel gear)
EXTERNAL_GEAR_RATIO = 48.0 / 36.0  # 1.33:1 reduction ratio (corrected!)

# CALIBRATED: Turn calibration factor based on actual test measurements
# Target 90° → Actual 85° = undershooting by 5°, need to increase request
# New factor: 0.875 * (90/85) = 0.927
TURN_CALIBRATION_FACTOR = 0.926  # Calibrated to actual robot performance

# CALIBRATED: Conversion factor based on actual test measurements
# Target 12" → Actual 19.5" = 1.625x too far, so multiply by 1.625
DEGREES_TO_INCHES = (WHEEL_CIRCUMFERENCE / 360.0) * EXTERNAL_GEAR_RATIO * 1.625

# Driver control sensitivity settings
TURN_SENSITIVITY = 0.8  # Increased for better responsiveness (was 0.6)
DEADBAND = 0  # No deadband - any stick movement causes robot movement per request of captian drayke

# PID Controller Class
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain  
        self.kd = kd  # Derivative gain
        
        self.previous_error = 0
        self.integral = 0
        
    def calculate(self, target, current):
        # Calculate error
        error = target - current
        
        # Calculate integral (sum of all errors)
        self.integral += error
        
        # Calculate derivative (change in error)
        derivative = error - self.previous_error
        
        # Calculate PID output
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        # Store error for next calculation
        self.previous_error = error
        
        return output
    
    def reset(self):
        self.previous_error = 0
        self.integral = 0


    
# Create PID controllers - BALANCED GAINS FOR STABLE COMPLETION
drive_pid = PIDController(0.3, 0.0, 0.05)  # Lowered KP: 0.5→0.3, KD: 0.1→0.05
turn_pid = PIDController(1.2, 0.0, 0.1)    # Increased KP: 0.6→1.2 (enough power to reach target)

def calibrate_inertial():
    """Calibrate inertial sensor - CRITICAL for accurate autonomous!"""
    brain.screen.clear_screen()
    brain.screen.print("Calibrating IMU...")
    brain.screen.new_line()
    brain.screen.print("DO NOT MOVE ROBOT!")
    
    inertial_sensor.calibrate()
    while inertial_sensor.is_calibrating():
        wait(50, MSEC)
    
    brain.screen.new_line()
    brain.screen.print("IMU Calibrated!")
    wait(100, MSEC)  # Reduced delay from 500ms to 100ms

# Autonomous movement functions
def drive_distance(distance_inches, max_speed=30, timeout_ms=3000):
    """Drive forward/backward a specific distance using PID - FIXED FOR BACKWARD MOVEMENT!"""
    # Safety bounds - prevent driving too far (max ~60 inches based on field size)
    max_distance_inches = 60
    if abs(distance_inches) > max_distance_inches:
        brain.screen.print("ERROR: Distance too far!")
        return False
    
    # Determine direction and use absolute distance for PID
    is_forward = distance_inches > 0
    abs_distance = abs(distance_inches)
    
    # Reset PID and encoders
    drive_pid.reset()
    left_motors.reset_position()
    right_motors.reset_position()
    
    # Always use positive target for stable PID
    target_degrees = abs_distance / DEGREES_TO_INCHES
    start_time = brain.timer.time(MSEC)
    
    while True:
        # Safety timeout check
        if brain.timer.time(MSEC) - start_time > timeout_ms:
            brain.screen.print("Drive timeout!")
            break
            
        # Get current position (always positive for PID)
        current_degrees = abs((left_motors.position(DEGREES) + right_motors.position(DEGREES)) / 2.0)
        
        # Calculate PID output (always positive values)
        speed = drive_pid.calculate(target_degrees, current_degrees)
        
        # Limit speed
        if speed > max_speed:
            speed = max_speed
        elif speed < -max_speed:
            speed = -max_speed
            
        # Check if we're close enough to target
        if abs(target_degrees - current_degrees) < 5:  # Within 5 degrees
            break
            
        # Apply direction to speed
        if not is_forward:  # Backward movement
            speed = -speed
            
        # Drive motors
        left_motors.spin(FORWARD, speed, PERCENT)
        right_motors.spin(FORWARD, speed, PERCENT)
        
        wait(20, MSEC)
    
    # Stop motors
    left_motors.stop()
    right_motors.stop()
    return True

def turn_degrees(degrees, max_speed=30, timeout_ms=3000):
    """Turn a specific number of degrees using INERTIAL SENSOR - SIMPLE FIXED VERSION!"""
    # Reset PID controller
    turn_pid.reset()
    
    # Safety bounds - prevent excessive turning
    if abs(degrees) > 180:
        brain.screen.print("ERROR: Turn too large!")
        return False
    
    # Get starting heading and apply calibration
    #start_heading = inertial_sensor.heading(DEGREES)
    #calibrated_degrees = degrees * TURN_CALIBRATION_FACTOR  # Apply calibration
    target_heading = degrees
    
    # Normalize target heading to 0-360 range
    while target_heading >= 360:
        target_heading -= 360
    while target_heading < 0:
        target_heading += 360
    
    start_time = brain.timer.time(MSEC)
    
    while True:
        # Safety timeout check
        if brain.timer.time(MSEC) - start_time > timeout_ms:
            brain.screen.print("Turn timeout!")
            break
            
        # Get current heading
        current_heading = inertial_sensor.heading(DEGREES)
        
        # Calculate error (shortest angular distance)
        error = target_heading - current_heading
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360
        
        # FIXED: Correct PID calculation (error as input, target 0)
        speed = turn_pid.calculate(error, 0)  # Want error to be 0
        
        # Limit speed
        if speed > max_speed:
            speed = max_speed
        elif speed < -max_speed:
            speed = -max_speed
            
        # Exit condition (within 5 degrees)
        if abs(error) < 5:
            break
            
        # Turn motors (positive speed = right turn)
        left_motors.spin(FORWARD, speed, PERCENT)
        right_motors.spin(FORWARD, -speed, PERCENT)
        
        wait(20, MSEC)
    
    # Stop motors
    left_motors.stop()
    right_motors.stop()
    return True

def run_intake(time_ms, speed=100):
    """Run intake for specified time"""
    intake_motor.spin(FORWARD, speed, PERCENT)
    intake_motor2.spin(FORWARD, speed, PERCENT)
    wait(time_ms, MSEC)
    intake_motor.stop()
    intake_motor2.stop()

def run_outtake(time_ms, speed=100):
    """Run outtake for specified time"""
    outtake_motor.spin(FORWARD, speed, PERCENT)
    wait(time_ms, MSEC)
    outtake_motor.stop()



# COMPLEX AUTONOMOUS (COMMENTED OUT FOR TESTING):
# def autonomous():
#     """Red Alliance Right Side - Start at Park Goal Wall → Red Blocks → Center Goal → Match Loader → Long Goal"""
#     # CRITICAL: Calibrate inertial sensor first!
#     calibrate_inertial()
#
#     brain.screen.clear_screen()
#     brain.screen.print("Park Wall Start Auton")
#
#     # Step 1: Drive forward to collect red blocks (FIXED undershooting)
#     brain.screen.new_line()
#     brain.screen.print("1. Forward to Red Blocks")
#     drive_distance(24)   # INCREASED from 8" to 24" to reach blocks properly
#     run_intake(2000)     # Extended intake time for better collection
#
#     # Step 2: Navigate to Center Goal for scoring
#     brain.screen.new_line()
#     brain.screen.print("2. To Center Goal")
#     drive_distance(-10)  # Back up for maneuvering room
#     turn_degrees(-90)    # Turn left toward center field
#     drive_distance(32)   # Drive to center area
#     turn_degrees(-90)    # Turn to position rear outtake toward Center Goal
#     drive_distance(-18)  # Back up to Center Goal for scoring
#     run_outtake(1000)    # Score in Center Goal
#
#     # Step 3: Navigate to Match Loader
#     brain.screen.new_line()
#     brain.screen.print("3. To Match Loader")
#     drive_distance(15)   # Move away from Center Goal
#     turn_degrees(180)    # Turn around to face match loader area
#     drive_distance(35)   # Drive to Match Loader
#     run_intake(2000)     # Collect from Match Loader
#
#     # Step 4: Navigate to Long Goal and score
#     brain.screen.new_line()
#     brain.screen.print("4. To Long Goal")
#     drive_distance(-12)  # Back away from loader
#     turn_degrees(-90)    # Turn to position rear toward Long Goal
#     drive_distance(-28)  # Drive backward to Long Goal
#     run_outtake(1200)    # Score in Long Goal
#
#     # Step 5: Safe position
#     brain.screen.new_line()
#     brain.screen.print("5. Safe position")
#     drive_distance(15)   # Drive to safe area
#
#     brain.screen.new_line()
#     brain.screen.print("Park Wall Auton Complete!")

def autonomous():
    """Simple Square Test - Drive 12" x 4 sides, turn right 90° each time to return to start"""
    calibrate_inertial()
    brain.screen.clear_screen()
    brain.screen.print("Square Test Autonomous")
    brain.screen.new_line()
    
    # Side 1
    brain.screen.print("Side 1: Forward 12\"")
    drive_distance(12)    # 12 inches forward
    brain.screen.new_line()
    brain.screen.print("Turn right 90°")
    turn_degrees(90)      # Turn right 90 degrees
    
    # Side 2
    brain.screen.new_line()
    brain.screen.print("Side 2: Forward 12\"")
    drive_distance(12)    # 12 inches forward
    brain.screen.new_line()
    brain.screen.print("Turn right 90°")
    turn_degrees(180)      # Turn right 90 degrees
    
    # Side 3
    brain.screen.new_line()
    brain.screen.print("Side 3: Forward 12\"")
    drive_distance(12)    # 12 inches forward
    brain.screen.new_line()
    brain.screen.print("Turn right 90°")
    turn_degrees(270)      # Turn right 90 degrees
    
    # Side 4 (return to start)
    #brain.screen.new_line()
    #brain.screen.print("Side 4: Forward 12\"")
    #drive_distance(12)    # 12 inches forward
    #brain.screen.new_line()
    #brain.screen.print("Final turn to start")
    #turn_degrees(90)      # Turn right 90 degrees - back to starting orientation
    
    brain.screen.new_line()
    brain.screen.print("Square Complete!")
    brain.screen.new_line()
    brain.screen.print("Back at start position")

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("Driver Control - High Responsiveness Mode")
    
    # Counter for display updates (reduced frequency to minimize delays)
    display_counter = 0
    
    # place driver control in this while loop
    while True:
        # Reduced display updates to minimize control loop interference
        display_counter += 1
        if display_counter >= 500:  # Update display every 500 loops (~5 seconds)
            brain.screen.set_cursor(1, 1)
            brain.screen.print("Driver Control Active   ")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("High Responsiveness Mode")
            display_counter = 0  # Reset counter
        
        # Get raw controller inputs
        axis1_raw = controller.axis1.position()
        axis3_raw = controller.axis3.position()
        
        # Apply deadband filtering to prevent drift and unwanted movements
        axis1 = axis1_raw if abs(axis1_raw) > DEADBAND else 0
        axis3 = axis3_raw if abs(axis3_raw) > DEADBAND else 0
        
        # Apply turn sensitivity scaling
        axis1 = axis1 * TURN_SENSITIVITY
        
        # Drive motors with improved responsiveness
        left_motors.spin(FORWARD, axis3 + axis1, PERCENT)
        right_motors.spin(FORWARD, axis3 - axis1, PERCENT)
        
        # Optimized intake control with R1 and R2 buttons
        r1_pressed = controller.buttonR1.pressing()
        r2_pressed = controller.buttonR2.pressing()
        
        if r1_pressed:
            intake_motor.spin(REVERSE, 100, PERCENT)  # Run intake in reverse
            intake_motor2.spin(REVERSE, 100, PERCENT)  # Run secondary intake in reverse
        elif r2_pressed:
            intake_motor.spin(FORWARD, 100, PERCENT)  # Run intake forward
            intake_motor2.spin(FORWARD, 100, PERCENT)  # Run secondary intake forward
        else:
            intake_motor.stop()  # Stop intake when neither button is pressed
            intake_motor2.stop()  # Stop secondary intake when neither button is pressed
        
        # Optimized outtake control with L1 and L2 buttons
        l1_pressed = controller.buttonL1.pressing()
        l2_pressed = controller.buttonL2.pressing()
        
        if l1_pressed:
            outtake_motor.spin(FORWARD, 100, PERCENT)  # Run outtake forward
        elif l2_pressed:
            outtake_motor.spin(REVERSE, 100, PERCENT)  # Run outtake in reverse
        else:
            outtake_motor.stop()  # Stop outtake when neither button is pressed
        
        # Reset encoder positions with X button (for testing) - optimized to prevent delay
        if controller.buttonX.pressing():
            left_motors.reset_position()
            right_motors.reset_position()
            brain.screen.clear_screen()
            brain.screen.print("Encoders Reset!")
            wait(100, MSEC)  # Reduced delay to minimize control interruption
            brain.screen.clear_screen()
        
        # Removed autonomous keybinds - use competition system "Timed Run" instead
        # Manual autonomous testing available through competition control only
      
        # Controller is automatically handled by VEX system
        
        wait(5, MSEC)  # Reduced from 20ms to 5ms for maximum responsiveness

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
