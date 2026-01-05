(define first car)

(define rest cdr)

(define (flip alpha)
 (unless (<= 0 alpha 1) (error "Alpha not probability"))
 (cond ((= alpha 0) #f)
       ((= alpha 1) #t)
       (else (call-with-current-continuation
	      (lambda (c)
	       (let ((saved-bottom bottom))
		(set! bottom
		      (lambda ()
		       (set! bottom saved-bottom)
		       (c #f)))
		#t))))))

(define (bottom) (error "Top-level bottom"))

(define (sample x)
 (let loop ((x (normalize x)) (p 1))
  (cond ((or (null? x) (zero? p)) (bottom))
	((flip (/ (cdr (first x)) p)) (car (first x)))
	(else (loop (rest x) (- p (cdr (first x))))))))

(define (remove-if-not p l)
 (let loop ((l l) (c '()))
  (cond ((null? l) (reverse c))
	((p (first l)) (loop (rest l) (cons (first l) c)))
	(else (loop (rest l) c)))))

(define (map-reduce g i f l)
 (if (null? l) i (map-reduce g (g i (f (car l))) f (cdr l))))

(define (normalize distribution)
 ;; It doesn't matter that we don't coalesce since except for efficiency
 ;; you can say a distribution with duplicates in its support is just an
 ;; implicit representation of a proper distribution.
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
              (unless (<= 0 alpha 1) (error "Alpha not probability"))
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

(define-syntax probability
 ;; marginal probability
 (syntax-rules ()
  ((probability e) (map-reduce + 0 cdr (remove-if-not car (distribution e))))))

(define-syntax support
 (syntax-rules () ((support e) (map car (distribution e)))))

(define-syntax expected-value
 ;; expectation
 (syntax-rules ()
  ((expected-value e)
   (map-reduce +
	       0
	       (lambda (pair) (* (car pair) (cdr pair)))
	       (distribution e)))))

(define-syntax variance
 (syntax-rules ()
  ((variance e) (- (expected-value (expt e 2)) (expt (expected-value e) 2)))))

(define-syntax raw-moment
 (syntax-rules () ((raw-moment n e) (expected-value (expt e n)))))

(define-syntax central-moment
 (syntax-rules ()
  ((central-moment n e)
   (let ((mu (expected-value e))) (expected-value (expt (- e mu) n))))))

(define (lg x) (/ (log x) (log 2)))

(define-syntax entropy
 (syntax-rules ()
  ((entropy e)
   (- (map-reduce +
		  0
		  (lambda (pair) (* (cdr pair) (lg (cdr pair))))
		  (distribution e))))))

(define-syntax kl-divergence
 ;; Kullback-Leibler divergence
 ;;\needswork: abstract equal?
 ;;            check that (set-equal? equal? (support e1) (support e2))
 (syntax-rules ()
  ((kl-divergence e1 e2)
   (map-reduce +
	       0
	       (lambda (x)
		(let ((p (probability (equal? e1 x)))
		      (q (probability (equal? e2 x))))
		 (* p (lg (/ p q)))))
	       (support e1)))))

(define (product-distribution f d1 d2)
 (distribution (f (sample d1) (sample d2))))

(define (marginal-distribution f d)
 (map (lambda (pair) (cons (f (car pair)) (cdr pair))) d))

(define-syntax mutual-information
 ;;\needswork: abstract car cdr cons
 (syntax-rules ()
  ((mutual-information e)
   (let* ((joint-distribution (distribution e))
	  (marginal-distribution-car
	   (marginal-distribution car joint-distribution))
	  (marginal-distribution-cdr
	   (marginal-distribution car joint-distribution)))
    (kl-divergence
     e
     (sample (product-distribution cons
				   marginal-distribution-car
				   marginal-distribution-cdr)))))))
