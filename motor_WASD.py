import serial
import time
import keyboard
import tkinter as tk

# Open serial port
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    print("Connected")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

def send_command(motor1_speed, motor2_speed):
    """
    Sends the speed commands for two motors via serial to the Sabertooth 2x60.
    :param motor1_speed: Speed for motor 1 (range 1-127 for forward, 128-255 for reverse)
    :param motor2_speed: Speed for motor 2 (range 1-127 for forward, 128-255 for reverse)
    """
    try:
        # Send speed for motor 1
        ser.write(bytes([motor1_speed]))
        # Send speed for motor 2
        ser.write(bytes([motor2_speed]))
        print(f"Motor 1 command: {motor1_speed}, Motor 2 command: {motor2_speed}")
    except Exception as e:
        print(f"Failed to send command: {e}")

def main():
    print("Use WASD keys to control the motors. Press 'Space' to stop. Press 'X' to exit.")

    try:
        while True:
            if keyboard.is_pressed('w'):
                # Move both motors forward
                send_command(64 + 30, 192 + 30)  # Motor 1 forward, Motor 2 forward
                time.sleep(0.1)

            elif keyboard.is_pressed('s'):
                # Move both motors backward
                send_command(64 - 30, 192 - 30)  # Motor 1 reverse, Motor 2 reverse
                time.sleep(0.1)

            elif keyboard.is_pressed('a'):
                # Turn left (Motor 1 backward, Motor 2 forward)
                send_command(64 - 30, 192 + 30)  # Motor 1 reverse, Motor 2 forward
                time.sleep(0.1)

            elif keyboard.is_pressed('d'):
                # Turn right (Motor 1 forward, Motor 2 backward)
                send_command(64 + 30, 192 - 30)  # Motor 1 forward, Motor 2 reverse
                time.sleep(0.1)

            elif keyboard.is_pressed('space'):
                # Stop both motors
                send_command(64, 192)  # Stop both motors
                time.sleep(0.1)

            elif keyboard.is_pressed('x'):
                # Exit the loop when 'X' is pressed
                print("Exiting...")
                break

    finally:
        # Close the serial connection when done
        ser.close()
        print("Serial port closed")

# Create GUI with tkinter
def create_gui():
    root = tk.Tk()
    root.title("GUI Motherfuckers!")
    root.geometry('800x800')

    button_style = {
       "font": ("Courier", 16, "bold"),
       "fg": "white",  # Text color
       "width": 20,
       "height": 2,
       "borderwidth": 5,
       "relief": "raised",  # 3D look
	     }

	 #Every button = Red, Stop button= Green 
    button_colors = {
        "forward": "#FF0000",  
        "left": "#FF0000",  
        "stop": "#28a745",  
        "right": "#FF0000",  
        "backward": "#dc3545", 
	    }

    # Forward button
    f_but = tk.Button(root, text="I'm straightforward. Try me.", bg=button_colors["forward"], **button_style, command=lambda: keyboard.press('w'))
    f_but.grid(row=0, column=1, padx=20, pady=20)

    # Left button
    l_but = tk.Button(root, text="I just left 'cuz you won't admit I'm right",bg=button_colors["left"], **button_style, command=lambda: keyboard.press('a'))
    l_but.grid(row=1, column=0, padx=20, pady=20)

    # Stop button
    st_but = tk.Button(root, text="Can't stop me",bg=button_colors["stop"], **button_style, command=lambda: keyboard.press('space'))
    st_but.grid(row=1, column=1, padx=20, pady=20)

    # Right button
    r_but = tk.Button(root, text="Treated you right but you still left",bg=button_colors["right"], **button_style, command=lambda: keyboard.press('d'))
    r_but.grid(row=1, column=2, padx=20, pady=20)

    # Backward button
    back_but = tk.Button(root, text="Ain't nobody got my back smh",bg=button_colors["backward"], **button_style, command=lambda: keyboard.press('s'))
    back_but.grid(row=2, column=1, padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
    main()
