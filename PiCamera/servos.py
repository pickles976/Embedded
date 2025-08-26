import pigpio
import time

SPEED = 18 # microseconds
DURATION = 0.5
CENTER = 1530

AZIMUTH_PIN = 18 
ELEVATION_PIN = 19

pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to pigpio daemon. Make sure it's running with 'sudo pigpiod'")
    exit()

def stop_servo(pin: int):
    pi.set_servo_pulsewidth(pin, 0)
    print("Servo stopped")

def rotate(pin: int, speed: float, duration: float):
    pulse = CENTER + speed 
    pi.set_servo_pulsewidth(pin, pulse)
    print(f"Rotating: {pulse}µs")
    time.sleep(duration)
    stop_servo(pin)

def cleanup_servos():
    stop_servo(AZIMUTH_PIN)
    stop_servo(ELEVATION_PIN)
    pi.set_servo_pulsewidth(AZIMUTH_PIN, 0)  # Turn off PWM
    pi.set_servo_pulsewidth(ELEVATION_PIN, 0)  # Turn off PWM
    pi.stop()
    print("Cleaned up and exited.")
