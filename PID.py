import matplotlib.pyplot as plt
import random
import time

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint):
        # Initialize PID parameters
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.integral = 0
        self.previous_error = 0

    def compute(self, current_angle, dt):
        # Calculate error
        error = self.setpoint - current_angle
        # Proportional term
        proportional = self.Kp * error
        # Integral term
        self.integral += error * dt
        integral = self.Ki * self.integral
        # Derivative term
        derivative = self.Kd * (error - self.previous_error) / dt if dt > 1e-6 else 0
        self.previous_error = error
        # Output
        output = proportional + integral + derivative
        return output


class ServoMotorSimulator:
    def __init__(self, min_angle=0, max_angle=180):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.current_angle = min_angle  # Start at 0 degrees
        self.angular_velocity = 0

    def apply_torque(self, torque, dt):
        # Add torsion error (random noise)
        noise = random.uniform(-0.5, 0.5)  # Simulating torsion error
        self.angular_velocity += (torque + noise) * dt
        self.current_angle += self.angular_velocity * dt

        # Bound the current angle within the servo's range
        if self.current_angle < self.min_angle:
            self.current_angle = self.min_angle
            self.angular_velocity = 0
        elif self.current_angle > self.max_angle:
            self.current_angle = self.max_angle
            self.angular_velocity = 0

    def get_current_angle(self):
        return self.current_angle


def simulate_servo_with_pid(target_angle, Kp, Ki, Kd, duration=5):
    # Simulate servo with PID control
    servo = ServoMotorSimulator()
    pid = PIDController(Kp, Ki, Kd, setpoint=target_angle)
    dt = 0.1
    total_time = 0

    time_data = []
    angle_data = []
    torque_data = []

    while total_time < duration:
        current_angle = servo.get_current_angle()
        torque = pid.compute(current_angle, dt)
        servo.apply_torque(torque, dt)

        time_data.append(total_time)
        angle_data.append(current_angle)
        torque_data.append(torque)

        total_time += dt

    return time_data, angle_data, torque_data


# Parameters for PID
target_angle = 90  # degrees
Kp = 1.5  # Increase to make the system respond faster
Ki = 0.1  # Integral to remove steady-state error
Kd = 0.05  # Derivative to reduce overshoot
duration = 10  # 10 seconds simulation

# Run the simulation
time_data, angle_data, torque_data = simulate_servo_with_pid(target_angle, Kp, Ki, Kd, duration)

# Plot results
plt.figure(figsize=(10, 5))

# Servo angle plot
plt.subplot(2, 1, 1)
plt.plot(time_data, angle_data, label='Servo Angle', color='blue')
plt.axhline(y=target_angle, color='red', linestyle='--', label='Target Angle')
plt.xlabel('Time (s)')
plt.ylabel('Angle (degrees)')
plt.title('Servo Motor Angle with PID Control')
plt.legend()

# Torque plot
plt.subplot(2, 1, 2)
plt.plot(time_data, torque_data, label='Torque', color='green')
plt.xlabel('Time (s)')
plt.ylabel('Torque (arbitrary units)')
plt.title('PID Controller Torque Output')
plt.legend()

plt.tight_layout()
plt.savefig('servo_simulation_with_torsion_error.png')

