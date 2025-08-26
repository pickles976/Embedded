    from picamera2 import Picamera2
    import time

    picam2 = Picamera2()
    picam2.start()
    time.sleep(2) # Give the camera time to adjust
    picam2.capture_file("test.jpg")
    picam2.stop()
    print("Image saved as test.jpg")