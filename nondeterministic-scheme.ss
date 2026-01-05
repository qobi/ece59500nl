(define first car)

(define second cadr)

(define rest cdr)

(define (a-boolean)
 (call-with-current-continuation
  (lambda (c)
   (let ((saved-fail fail))
    (set! fail
          (lambda ()
           (set! fail saved-fail)
           (c #f)))
    #t))))

(define (fail) (error "Top-level fail"))

(define-syntax either (syntax-rules () ((either e1 e2) (if (a-boolean) e1 e2))))

(define (a-member-of x)
 (if (null? x) (fail) (either (first x) (a-member-of (rest x)))))

(define (an-integer-between i j)
 (if (> i j) (fail) (either i (an-integer-between (+ i 1) j))))

(define (a-subset-of l)
 (if (null? l)
     '()
     (let ((y (a-subset-of (rest l)))) (either (cons (first l) y) y))))

(define (a-split-of l)
 (let loop ((x '()) (y l))
  (if (null? y)
      (list x y)
      (either (list x y) (loop (append x (list (first y))) (rest y))))))

(define (a-permutation-of l)
 (if (null? l)
     l
     (let ((split (a-split-of (a-permutation-of (rest l)))))
      (append (first split) (cons (first l) (second split))))))

(define-syntax all-values
 ;; all-values is bagof, not setof.
 ;; But it doesn't matter except for model counting since except for efficiency
 ;; you can say a list is just a representation of a set with duplicates
 ;; implicitly removed.
 (syntax-rules ()
  ((all-values e)
   (call-with-current-continuation
    (lambda (c)
     (let ((values '())
           (saved-a-boolean a-boolean)
           (saved-fail fail))
      (set! a-boolean
            (lambda ()
             (call-with-current-continuation
              (lambda (c)
               (let ((saved-fail fail))
                (set! fail
                      (lambda ()
                       (set! fail saved-fail)
                       (c #f)))
                #t)))))
      (set! fail
            (lambda ()
             (set! a-boolean saved-a-boolean)
             (set! fail saved-fail)
             (c (reverse values))))
      (set! values (cons e values))
      (fail)))))))

(define-syntax possible?
 ;; satisfiability
 (syntax-rules () ((possible? e) (not (null? (all-values (if e #t (fail))))))))

(define-syntax necessary?
 (syntax-rules () ((necessary? e) (not (possible? (not e))))))

(define-syntax how-many
 ;; model counting
 (syntax-rules () ((how-many e) (length (all-values (if e #t (fail)))))))
