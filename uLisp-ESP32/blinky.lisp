(defun b ()   
    (pinmode 2 t)   ; sets pinmode of pin 2 to true
    (loop    
        (digitalwrite 2 t)    
        (delay 1000)    
        (digitalwrite 2 nil)     
        (delay 1000)))