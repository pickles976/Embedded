; Comment to disable echo
(defvar MPU_6050 #x68)

(defvar PWR_MGMT #x6B)

(defvar ACCEL_OFFSET_REGISTER #x06)
(defvar ACCEL_REGISTER #x3B)
(defvar ACCEL_SCALE 16384)

(defvar GYRO_REGISTER #x43)
(defvar GYRO_SCALE 131)

(defvar dt 20)
(defvar time 0.0)

; Write the register we want to read from
(defun set-i2c-register (address byte)
    (with-i2c (str address)
        (write-byte byte str)))

(defun wake-up-mpu ()
    (with-i2c (str MPU_6050)
        (write-byte PWR_MGMT str)
        (write-byte #x00 str)))

(defun bytes-to-signed (hi lo)
  (let ((val (logior (ash hi 8) lo)))
    (if (>= val 32768)
        (- val 65536)
        val))) 

(defun bytes-to-integers-signed (byte-list)
  (if (or (null byte-list) (null (cdr byte-list)))
      '()
      (cons (bytes-to-signed (car byte-list) (cadr byte-list))
            (bytes-to-integers-signed (cddr byte-list)))))

(defun read-imu-raw (register)
    (set-i2c-register MPU_6050 register)
    (with-i2c (str MPU_6050 6) ; read 6 bytes from MPU
        (list
            (read-byte str) ; X hi
            (read-byte str) ; X lo
            (read-byte str) ; Y hi
            (read-byte str) ; Y lo
            (read-byte str) ; Z hi
            (read-byte str)))) ; Z lo 

; Read a 6 bytes of EEPROM memory starting at the specified register
(defun read-imu (scale register)
    (mapcar
        (lambda (entry) (/ entry scale)) ; divide by the scale
        (bytes-to-integers-signed (read-imu-raw register)))) ; read bytes and convert to signed integers

(defun read-accel ()
    (read-imu ACCEL_SCALE ACCEL_REGISTER))

(defun read-gyro ()
    (read-imu GYRO_SCALE GYRO_REGISTER))

(defun get-x (items) (car items))
(defun get-y (items) (cadr items))
(defun get-z (items) (caddr items))

(defun angle (opp adj)
    (/ (* (atan opp adj) 180) 3.14159))

(defun print-format (readings)
  (apply #'format t "~g,~g,~g~%" readings))

(defun main () 
    (wake-up-mpu)
    (loop
        (setq time (+ time (/ dt 1000)))
        (let ((accel (read-accel)))
            (print-format 
                (list 
                    time
                    (angle (get-y accel) (get-z accel)) ; angle
                    (get-x (read-gyro)))))) ; gryo rotation amount
        (delay dt))

(main)