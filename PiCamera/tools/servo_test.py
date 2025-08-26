# use this to find the center

import pigpio
import time

# Define the servo control pin
SERVO_PIN = 19  # GPIO18 (physical pin 12)

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon. Did you run 'sudo pigpiod'?")
    exit()

# Sweep parameters
start_pulse = 1520  # in microseconds
end_pulse = 1540    # in microseconds
step = 1           # step size in microseconds
delay = 1.0         # delay between steps (seconds)

try:
    print("Sweeping servo from 1400µs to 1600µs...")
    for pulse_width in range(start_pulse, end_pulse + step, step):
        pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
        print(f"Pulse width set to: {pulse_width} µs")
        time.sleep(delay)

    print("Sweep complete.")

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    pi.set_servo_pulsewidth(SERVO_PIN, 0)  # Turn off PWM
    pi.stop()
    print("PWM signal stopped and pigpio cleaned up.")
