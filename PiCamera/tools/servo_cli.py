import pigpio
import time

SPEED = 18
CENTER = 1530

# Define GPIO pin
AZIMUTH_PIN = 18  # GPIO18, physical pin 12
ELEVATION_PIN = 19

# Create pigpio instance
pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to pigpio daemon. Make sure it's running with 'sudo pigpiod'")
    exit()

def stop_servo(pin: int):
    pi.set_servo_pulsewidth(pin, CENTER)  # Neutral (stop)
    print("Servo stopped")

def rotate_left(speed=SPEED):
    pulse = CENTER + speed  # up to 2000µs
    pi.set_servo_pulsewidth(AZIMUTH_PIN, pulse)
    print(f"Rotating forward: {pulse}µs")

def rotate_right(speed=SPEED):
    pulse = CENTER - speed  # down to 1000µs
    pi.set_servo_pulsewidth(AZIMUTH_PIN, pulse)
    print(f"Rotating backward: {pulse}µs")

def rotate_up(speed=SPEED):
    pulse = CENTER - speed  # down to 1000µs
    pi.set_servo_pulsewidth(ELEVATION_PIN, pulse)
    print(f"Rotating backward: {pulse}µs")

def rotate_down(speed=SPEED):
    pulse = CENTER + speed  # down to 1000µs
    pi.set_servo_pulsewidth(ELEVATION_PIN, pulse)
    print(f"Rotating backward: {pulse}µs")


try:
    while True:
        cmd = input("Command (f=forward, b=backward, s=stop, q=quit): ").strip().lower()
        if cmd == 'l':
            rotate_left()
        elif cmd == 'r':
            rotate_right()
        elif cmd == 'u':
            rotate_up()
        elif cmd == 'd':
            rotate_down()
        elif cmd == 's':
            stop_servo(AZIMUTH_PIN)
            stop_servo(ELEVATION_PIN)
        elif cmd == 'q':
            break
        else:
            print("Invalid command. Try f, b, s, q.")
except KeyboardInterrupt:
    pass
finally:
    stop_servo()
    pi.set_servo_pulsewidth(AZIMUTH_PIN, 0)  # Turn off PWM
    pi.stop()
    print("Cleaned up and exited.")
