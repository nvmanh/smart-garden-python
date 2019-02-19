### 1. cài đặt bàn phím ảo

https://raspberrypi.vn/thu-thuat-raspberry-pi/cai-dat-ban-phim-ao-onscreen-keyboard-tren-raspbian-5785.pi
```java
sudo apt-get install matchbox-keyboard -y \
cd Desktop && nano keyboard.sh
```

copy nội dung: 
```java
#!/bin/bash
matchbox-keyboard
```
chmod file:
```java
chmod +x keyboard.sh
```

### 2. Cài đặt hiển thi fullscreen cho màn hình 7inch
(với các loại màn hình khác thì bạn cần chỉnh lại thông số cho phù hợp)

sửa file boot/config.txt
```java
max_usb_current=1
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
```
