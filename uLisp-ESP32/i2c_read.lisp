; Comment to disable echo
(defun scan () 
  (dotimes (p 127)
    (with-i2c 
        (str p)
        (when str (print p)))))

(defvar MPU_6050 #x68)

(defvar PWR_MGMT #x6B)

(defvar ACCEL_OFFSET_REGISTER #x06)
(defvar ACCEL_REGISTER #x3B)
(defvar ACCEL_SCALE 16384)

(defvar GYRO_REGISTER #x43)
(defvar GYRO_SCALE 131)

; Write the register we want to read from
(defun set-i2c-register (address byte)
    (with-i2c (str address)
        (write-byte byte str)))

(defun wake-up-mpu ()
    (with-i2c (str MPU_6050)
        (write-byte PWR_MGMT str)
        (write-byte #x00 str)))

(defun read-sensor-raw (register)
    (set-i2c-register MPU_6050 register)
    (with-i2c (str MPU_6050 6) ; read 6 bytes from MPU
        (list
            (read-byte str) ; X hi
            (read-byte str) ; X lo
            (read-byte str) ; Y hi
            (read-byte str) ; Y lo
            (read-byte str) ; Z hi
            (read-byte str)))) ; Z lo 

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

(defun read-offsets ()
    (mapcar
        (lambda (entry) (/ entry ACCEL_SCALE)) 
        (bytes-to-integers-signed (read-sensor-raw ACCEL_OFFSET_REGISTER))))

(defun read-accel ()
    (mapcar
        (lambda (entry) (/ entry ACCEL_SCALE)) 
        (bytes-to-integers-signed (read-sensor-raw ACCEL_REGISTER))))

(defun read-gyro ()
    (mapcar
        (lambda (entry) (/ entry GYRO_SCALE)) 
        (bytes-to-integers-signed (read-sensor-raw GYRO_REGISTER))))

(defun get-x (items) (car items))
(defun get-y (items) (cadr items))
(defun get-z (items) (caddr items))

(defun angle (opp adj)
    (/ (* (atan opp adj) 180) 3.14159))

(defun main () 
    (wake-up-mpu)
    (loop
        ;; (print (read-accel))
        (let ((accel (read-accel)))
            (print (angle (get-y accel) (get-z accel))))
        (delay 1000)))
