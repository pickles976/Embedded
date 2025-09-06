; begin program
(defvar angle 0.0)
(defvar rate 0.0)

(defvar q-angle 0.0001)
(defvar q-bias 0.03)
(defvar r-measure 0.0002)
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

(kalman-update 0.1 0.1 0.02)