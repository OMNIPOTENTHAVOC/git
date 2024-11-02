import serial
import time
import pygame
import math

# Attempt to create a serial connection
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    print(f"Connected to {ser.portstr}")
except serial.SerialException as e:
    print(f"Error: {e}")
    exit(1)

def send_command(command):
    try:
        # Ensure command is sent as a single byte
        command_byte = bytes([command])
        ser.write(command_byte)
        print(f"DATA SENT: {command} (0x{command:02X})")  
    except Exception as e:
        print(f"Failed to send command: {e}")

pygame.init()
pygame.joystick.init()

# Check if a joystick is connected
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick {joystick.get_name()} initialized")
else:
    print("No joystick connected!")
    exit()

def joystick_to_motor_power(x, y, max_motor_power=100, max_joystick=1.0):
    # Calculate the angle (theta) in radians between the joystick position and the x-axis
    theta = math.atan2(y, x)

    # Calculate the magnitude (how far the joystick is pushed from the origin)
    magnitude = math.sqrt(x**2 + y**2)
    magnitude = min(magnitude, 1.0)

    x_cartesian = magnitude * math.cos(theta)
    y_cartesian = magnitude * math.sin(theta)

    x_scaled = (max_motor_power * x_cartesian) / max_joystick
    y_scaled = (max_motor_power * y_cartesian) / max_joystick

    right_motor_power = y_scaled - x_scaled
    left_motor_power = x_scaled + y_scaled

    return left_motor_power, right_motor_power

def control_motors(y_axis, x_axis):
    # Invert the y_axis to reverse the forward/backward controls
    y_axis = -y_axis
    x_axis = -x_axis
    left_power, right_power = joystick_to_motor_power(x_axis, y_axis)

    if abs(y_axis) > 0.1 or abs(x_axis) > 0.1:
        left_speed = int(left_power * 63 / 100)
        right_speed = int(right_power * 63 / 100)

        send_command(64 + left_speed if left_power >= 0 else 64 - abs(left_speed))  # Motor 1
        send_command(192 + right_speed if right_power >= 0 else 192 - abs(right_speed))  # Motor 2
    else:
        send_command(64)  # Stop motor 1
        send_command(192)  # Stop motor 2
        print("")

# Main loop to read joystick input
try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get joystick axis values (e.g., left stick axes)
        x_axis = joystick.get_axis(0)  # Left stick X-axis
        y_axis = joystick.get_axis(1)  # Left stick Y-axis

        control_motors(y_axis, x_axis)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    send_command(64)  # Stop motor 1
    send_command(192)  # Stop motor 2
    ser.close()
    pygame.quit()

