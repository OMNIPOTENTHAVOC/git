mport serial
import time
import tkinter as tk

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust as needed
    print(f"Connected to {ser.portstr}")
except serial.SerialException as e:
    print(f"Error: {e}")
    exit(1)

def send_motor_signal(signal):
    try:
        command_byte = bytes([signal])
        ser.write(command_byte)
        print(f"Signal sent: {signal} (0x{signal:02X})")
    except Exception as e:
        print(f"Failed to send signal: {e}")

def get_motor_speed():
    return speed_slider.get()

def drive_forward():
    velocity = get_motor_speed()
    if velocity == 127:
        print("WRONG LEVERRR!")
    print(f"Forward at speed {velocity}")
    send_motor_signal(64 + velocity)
    send_motor_signal(192 + velocity)

def drive_backward():
    velocity = get_motor_speed()
    if velocity == 127:
        print("WRONG LEVERRR!")
    print(f"Backward at speed {velocity}")
    send_motor_signal(64 - velocity)
    send_motor_signal(192 - velocity)

def steer_left():
    velocity = get_motor_speed()
    if velocity == 127:
        print("WRONG LEVERRR!")
    print(f"Left at speed {velocity}")
    send_motor_signal(64 - velocity)
    send_motor_signal(192 + velocity)

def steer_right():
    velocity = get_motor_speed()
    if velocity == 127:
        print("WRONG LEVERRR!")
    print(f"Right at speed {velocity}")
    send_motor_signal(64 + velocity)
    send_motor_signal(192 - velocity)

def halt_motors():
    print("Stopping")
    send_motor_signal(64)
    send_motor_signal(192)

def close_application():
    halt_motors()
    ser.close()
    print("Exiting the program")
    root.quit()

root = tk.Tk()
root.configure(bg="#330000")
root.title("Pull the lever, Kronk")

speed_label = tk.Label(root, text="Lever Kronk")
speed_label.grid(row=0, column=0, padx=15, pady=15)

speed_slider = tk.Scale(root, from_=0, to=63, orient=tk.HORIZONTAL, length=200, bg="#99CCCC")
speed_slider.set(30)
speed_slider.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

forward_btn = tk.Button(root, text="W", command=drive_forward, width=10, height=10, bg="#9999FF")
backward_btn = tk.Button(root, text="S", command=drive_backward, width=10, height=10, bg="#66CCFF")
left_btn = tk.Button(root, text="A", command=steer_left, width=10, height=10, bg="#CCCCFF")
right_btn = tk.Button(root, text="D", command=steer_right, width=10, height=10, bg="#99FF9FF")
halt_btn = tk.Button(root, text="Stop", command=halt_motors, width=10, height=10, bg="#FF0000")
exit_btn = tk.Button(root, text="Exit", command=close_application, width=10, height=10, bg="#FF9900")

forward_btn.grid(row=1, column=1, padx=5, pady=5)
left_btn.grid(row=2, column=0, padx=5, pady=5)
halt_btn.grid(row=2, column=1, padx=5, pady=5)
right_btn.grid(row=2, column=2, padx=5, pady=5)
backward_btn.grid(row=3, column=1, padx=5, pady=5)
exit_btn.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
