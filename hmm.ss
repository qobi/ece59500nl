(define (mixture-model pi distributions)
 (let ((j (sample pi)))
  (sample (list-ref distributions j))))

(define pi '((0 . 0.5) (1 . 0.25) (2 . 0.25)))
(define distributions '(((x . 0.5) (y . 0.5))
			((x . 0.25) (z . 0.75))
			((y . 0.25) (z . 0.75))))

(define (finite-automaton b a c I)
 (let loop ((j (a-member-of b))
	    (output '())
	    (i I))
  (if (zero? i)
      output
      (loop (a-member-of (list-ref a j))
	    (append output (list (a-member-of (list-ref c j))))
	    (- i 1)))))

(define b '(0 2))
(define a '((0 1 2)
	    (1 2)
	    (2)))
(define c '((x y)
	    (y z)
	    (z)))

(define (Markov-process b a I)
 (let loop ((j (sample b))
	    (states '())
	    (i I))
  (if (zero? i)
      states
      (loop (sample (list-ref a j))
	    (append states (list j))
	    (- i 1)))))

(define (HMM b a c I)
 (let loop ((j (sample b))
	    (output '())
	    (i I))
  (if (zero? i)
      output
      (loop (sample (list-ref a j))
	    (append output (list (sample (list-ref c j))))
	    (- i 1)))))

(define b '((0 . 0.5) (1 . 0.25) (2 . 0.25)))
(define a '(((0 . 0.5) (1 . 0.25) (2 . 0.25))
	    ((0 . 0.25) (1 . 0.5) (2 . 0.25))
	    ((0 . 0.25) (1 . 0.25) (2 . 0.5))))
(define c '(((x . 0.5) (y . 0.5))
	    ((x . 0.25) (z . 0.75))
	    ((y . 0.25) (z . 0.75))))

(define (remove-duplicates x)
 (let loop ((x x) (c '()))
  (cond ((null? x) (reverse c))
	((member (first x) c) (loop (rest x) c))
	(else (loop (rest x) (cons (first x) c))))))

(define (map-reduce g i f l)
 (if (null? l)
     i
     (g (f (first l)) (map-reduce g i f (rest l)))))

(define (coalesce x)
 (map (lambda (v)
       (cons v
	     (map-reduce
	      +
	      0
	      (lambda (p)
	       (if (equal? (car p) v)
		   (cdr p)
		   0))
	      x)))
      (remove-duplicates (map car x))))
