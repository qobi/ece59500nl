(define-macro possible?
 (lambda (form expander) (expander `(possible ,(second e)))) expander)))

(define-macro how-many
 (lambda (form expander)
  (expander `(length (all-values (if ,(second e) #t (fail)))) expander)))
