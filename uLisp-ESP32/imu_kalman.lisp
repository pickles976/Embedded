; MEASUREMENTS
(defvar angle 0.0)
(defvar rate 0.0)
(defvar gyro-mean -0.038483)

(defvar dt 20)
(defvar time 0.0)
(defvar accel-angle 0)
(defvar gyro-rate 0)
(defvar timestep (/ dt 1000))

; KALMAN STUFF
(defvar q-angle 0.0013)
(defvar q-bias 0.03)
(defvar r-measure 0.017)
(defvar Q (list 
            (list q-angle 0.0)
            (list 0.0 q-bias)))
(defvar P (list 
            (list 0.0 0.0) 
            (list 0.0 0.0)))
(defvar I (list 
            (list 1 0) 
            (list 0 1)))

(defun matmul (mat1 mat2)
  (let ((mat2T (transpose mat2)))
    (mapcar 
     (lambda (row1)
       (mapcar 
        (lambda (col2)
          (dot row1 col2))
        mat2T))
     mat1)))

(defun matadd (a b)
  (mapcar #'(lambda (rows)
              (mapcar #'+ (car rows) (cadr rows)))
          (mapcar #'list a b)))

(defun matsub (a b)
  (mapcar #'(lambda (rows)
              (mapcar #'- (car rows) (cadr rows)))
          (mapcar #'list a b)))

(defun dot (vec1 vec2)
  (apply #'+ (mapcar #'* vec1 vec2)))

(defun transpose (matrix)
  (if (null (car matrix))
      '()
      (cons (mapcar (lambda (row) (car row)) matrix)
            (transpose (mapcar (lambda (row) (cdr row)) matrix)))))

(defun predict (new-rate dt)
    (setq rate (- new-rate q-bias))
    (setq angle (+ angle (* dt rate))))

; P = FPF^T
(defun update-covariance (dt)
    (let ((Fk (list 
                (list 1 dt) 
                (list 0 1)) ))
        (setq P (matadd (matmul Fk (matmul P(transpose Fk))) Q))))

; y = Z - HX
; S = P + Q
; K = PS^-1
; X = X + Ky
(defun update-measurement (new-angle dt)
    (let ((y (- new-angle angle))
          (S (+ (caar P) r-measure)))
      (let ((K (list 
                  (list (/ (caar P) S))
                  (list (/ (cadar P) S)))))
        (setq angle (+ angle (* (caar K) y)))
        (setq q-bias (+ q-bias (* (caadr K) y)))
        (setq P (matmul (matsub I K) P)))))

; Make sure to subtract mean gyro reading from new-rate before plugging it in here
(defun kalman-update (new-angle new-rate dt)
    (predict new-rate dt)
    (update-covariance dt)
    (update-measurement new-angle dt))

; IMU STUFF
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

(defun get-angle (opp adj)
    (/ (* (atan opp adj) 180) 3.14159))

(defun print-format (readings)
  (apply #'format t "~g,~g,~g,~g~%" readings))

(defun main () 
    (wake-up-mpu)
    (loop ; total loop time 11ms
        (setq time (+ time timestep))
        (time (let ((accel (read-accel)))
            (setq accel-angle (get-angle (get-y accel) (get-z accel)))
            (setq gyro-rate (- (get-x (read-gyro)) gyro-mean))
            (kalman-update accel-angle gyro-rate timestep)
            (print-format (list time accel-angle gyro-rate angle)))) ; print is 2ms
        (delay dt))) ; no way to properly measure elapsed time

(main)