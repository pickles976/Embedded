

; A = [[1,2,3],
;      [4,5,6]]
; B = [[1],
;      [2],
;      [3]]
; 1. Map over each row in A
; 2. Map over each each row in transposed B
; 3. Take dot product (first iteration would be [1,2,3] . [1,2,3] )
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


(defvar A '((1 2 3)
            (4 5 6)))

(defvar B '((1)
            (2)
            (3)))

(matmul A B)