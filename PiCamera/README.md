# Raspberry Pi Zero Camera

### Hardware

[Elegoo ULN2003 stepper motors](https://www.elegoo.com/blogs/arduino-projects/elegoo-uln2003-stepper-motors-and-motor-driver-boards-tutorial) $15

[Raspberry PI Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) $15

[Raspberry Pi Camera](https://www.amazon.com/Camera-Arducam-Raspberry-Raspbian-MotionEye/dp/B01LY05LOE?crid=1SD21BYQMIKZR&dib=eyJ2IjoiMSJ9.CuuGiXKuhG2W8K2-4jb3rHXRw-8Jijh59kVPtHsgtffBVlNs1HjSKyTYJi_UK8gT2tpOXj_gZSOdDCGFyL4Nl-q4prUvLYjk_K2JNu5801q7FSRP0EXWC4FbPKS6YpsezMx-E0nEZr2EB-evG2AFTl0OLzOBX_zsDfjbEQKm-eAq55xlydX0iiyEU2Exhj-LKmR0OjV0Syf72dKpQ3qNjdJ901YsGlgyv0Wl54ltx40.bjqLPOzMPxdDq1TeKZiqSh50URBySySe1jBbR4cIUCA&dib_tag=se&keywords=raspberry+pi+zero+camera&qid=1756229203&sprefix=raspberry+pi+zero+camer%2Caps%2C133&sr=8-3) $12

### Setup



```shell
sudo apt install python3-picamera2 python3-flask open-cv -y
```

```shell
vcgencmd get_camera
```

```shell
sudo apt install rpicam-apps vlc -y
```

```
sudo apt-get update
sudo apt-get install pigpio python-pigpio python3-pigpio
```

### Run on Startup 

sudo pigpiod

```shell
sudo nano /etc/systemd/system/camera-app.service
sudo systemctl daemon-reload
sudo systemctl enable camera-app.service
sudo systemctl start camera-app.service
```