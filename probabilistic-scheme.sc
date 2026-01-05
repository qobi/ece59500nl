(define (flip p) (error #f "Top-level flip"))

(define (bottom) (error #f "Top-level bottom"))

(define (sample x)
 (let loop ((x (normalize x)) (p 1))
  (cond ((or (null? x) (zero? p)) (bottom))
	((flip (/ (cdr (first x)) p)) (car (first x)))
	(else (loop (rest x) (- p (cdr (first x))))))))

;;; This does not coalesce the support.
(define (normalize distribution)
 (let ((distribution
	(remove-if-not (lambda (pair) (> (cdr pair) 0)) distribution))
       (sum (map-reduce + 0 cdr distribution)))
  (map (lambda (pair) (cons (car pair) (/ (cdr pair) sum))) distribution)))

(define-syntax distribution
 (syntax-rules ()
  ((distributions e)
   (normalize
    (call-with-current-continuation
     (lambda (c)
      (let ((values '())
            (saved-flip flip)
            (saved-bottom bottom)
            (p 1))
       (set! flip
             (lambda (alpha)
              (unless (<= 0 alpha 1) (error #f "Alpha not probability"))
	      (cond ((= alpha 0) #f)
		    ((= alpha 1) #t)
		    (else (call-with-current-continuation
			   (lambda (c)
			    (let ((saved-bottom bottom)
				  (saved-p p))
			     (set! bottom
				   (lambda ()
				    (set! bottom saved-bottom)
				    (set! p (* (- 1 alpha) saved-p))
				    (c #f)))
			     (set! p (* alpha p))
			     #t)))))))
       (set! bottom
             (lambda ()
              (set! flip saved-flip)
              (set! bottom saved-bottom)
              (c (reverse values))))
       (set! values (cons (cons e p) values))
       (bottom))))))))

;;; marginal probability
(define-macro probability
 (lambda (form expander)
  (expander
   '(map-reduce 0 + cdr (remove-if-not car (distribution ,(second form))))
   expander)))

;;; support
(define-macro support
 (lambda (form expander)
  (expander '(map car (distribution ,(second form))) expander)))

;;; expectation
(define-macro expectation
 (lambda (form expander)
  (expander
   '(map-reduce +
		0
		(lambda (pair) (* (car pair) (cdr pair)))
		(distribution ,(second form)))
   expander)))

(define (lg x) (/ (log x) (log 2)))

;;; entropy
(define-macro entropy
 (lambda (form expander)
  (expander
   '(- (map-reduce +
		   0
		   (lambda (pair) (* (cdr pair) (lg (cdr pair))))
		   (distribution ,(second form))))
   expander)))
