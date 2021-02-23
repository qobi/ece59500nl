(define (top-down:is-sentence? word-string rules lexicon)
 (define fail-if-not-phrase
  (lambda (word-string category)
   (top-down:display-parse-state word-string category)
   (cond
    ((singleton? word-string)
     (unless (eq? (lookup (head word-string) lexicon) category)
      (fail))
     (message "Base case")
     #t)
    (else (let ((rule (a-member-of rules)))
	   (unless (eq? (rule-lhs rule) category) (fail))
	   (message (string-append "Recursive case: "
				   (drop-parentheses (format #f "~s" rule))))
	   (let ((word-strings (split word-string)))
	    (fail-if-not-phrase (first word-strings) (rule-rhs1 rule))
	    (fail-if-not-phrase (second word-strings) (rule-rhs2 rule))))))))
 (one-value (fail-if-not-phrase word-string 's) #f))

(define (memoized-top-down:is-sentence? word-string rules lexicon)
 (define fail-if-not-phrase
  (memoize
   (lambda (word-string category)
    (top-down:display-parse-state word-string category)
    (cond
     ((singleton? word-string)
      (unless (eq? (lookup (head word-string) lexicon) category)
       (fail))
      (message "Base case")
      #t)
     (else (let ((rule (a-member-of rules)))
	    (unless (eq? (rule-lhs rule) category) (fail))
	    (message (string-append "Recursive case: "
				    (drop-parentheses (format #f "~s" rule))))
	    (let ((word-strings (split word-string)))
	     (fail-if-not-phrase (first word-strings) (rule-rhs1 rule))
	     (fail-if-not-phrase (second word-strings) (rule-rhs2 rule)))))))))
 (one-value (fail-if-not-phrase word-string 's) #f))

(define (recursive-descent:is-sentence? word-string rules lexicon)
 (define peel
  (lambda (word-string category)
   (recursive-descent:display-parse-state word-string category)
   (when (word-string-empty? word-string) (fail))
   (either (begin
	    (unless (eq? (lookup (head word-string) lexicon) category) (fail))
	    (message "Base case")
	    (tail word-string))
	   (let ((rule (a-member-of rules)))
	    (message (string-append "Recursive case: "
				    (drop-parentheses (format #f "~s" rule))))
	    (unless (eq? (rule-lhs rule) category) (fail))
	    (peel (peel word-string (rule-rhs1 rule)) (rule-rhs2 rule))))))
 (one-value (begin (unless (null? (peel word-string 's)) (fail)) #t) #f))

(define (memoized-recursive-descent:is-sentence? word-string rules lexicon)
 (define peel
  (memoize
   (lambda (word-string category)
    (recursive-descent:display-parse-state word-string category)
    (when (word-string-empty? word-string) (fail))
    (either (begin
	     (unless (eq? (lookup (head word-string) lexicon) category) (fail))
	     (message "Base case")
	     (tail word-string))
	    (let ((rule (a-member-of rules)))
	     (message (string-append "Recursive case: "
				     (drop-parentheses (format #f "~s" rule))))
	     (unless (eq? (rule-lhs rule) category) (fail))
	     (peel (peel word-string (rule-rhs1 rule)) (rule-rhs2 rule)))))))
 (one-value (begin (unless (null? (peel word-string 's)) (fail)) #t) #f))

(define (shift-reduce:is-sentence? word-string rules lexicon)
 (define shift-reduce
  (lambda (stack word-string)
   (shift-reduce:display-parse-state stack word-string)
   (either
    (begin (unless (and (word-string-empty? word-string)
			(= (length stack) 1)) (fail))
	   (message "Termination condition")
	   (first stack))
    (begin (when (word-string-empty? word-string) (fail))
	   (message "Shift")
	   (shift-reduce (cons (lookup (head word-string) lexicon) stack)
			 (tail word-string)))
    (begin (when (< (length stack) 2) (fail))
	   (let ((rule (a-member-of rules)))
	    (message (string-append
		      "Reduce: "
		      (drop-parentheses (format #f "~s" rule))))
	    (unless (and (eq? (rule-rhs1 rule) (second stack))
			 (eq? (rule-rhs2 rule) (first stack)))
	     (fail))
	    (shift-reduce (cons (rule-lhs rule) (rest (rest stack)))
			  word-string))))))
 (one-value (begin (unless (eq? (shift-reduce '() word-string) 's) (fail)) #t)
	    #f))

(define (memoized-shift-reduce:is-sentence? word-string rules lexicon)
 (define shift-reduce
  (memoize
   (lambda (stack word-string)
    (shift-reduce:display-parse-state stack word-string)
    (either
     (begin (unless (and (word-string-empty? word-string)
			 (= (length stack) 1)) (fail))
	    (message "Termination condition")
	    (first stack))
     (begin (when (word-string-empty? word-string) (fail))
	    (message "Shift")
	    (shift-reduce (cons (lookup (head word-string) lexicon) stack)
			  (tail word-string)))
     (begin (when (< (length stack) 2) (fail))
	    (let ((rule (a-member-of rules)))
	     (message (string-append
		       "Reduce: "
		       (drop-parentheses (format #f "~s" rule))))
	     (unless (and (eq? (rule-rhs1 rule) (second stack))
			  (eq? (rule-rhs2 rule) (first stack)))
	      (fail))
	     (shift-reduce (cons (rule-lhs rule) (rest (rest stack)))
			   word-string)))))))
 (one-value (begin (unless (eq? (shift-reduce '() word-string) 's) (fail)) #t)
	    #f))

(define (cky:is-sentence? word-string rules lexicon)
 (set! *n* (+ (length word-string) 1))
 (set! *chart* (make-matrix *n* *n* #f))
 (for-effects
  (let* ((i (an-integer-between 0 (- *n* 1)))
	 (j (an-integer-between (+ i 1) (- *n* 1)))
	 (chart-entry
	  (make-chart-entry
	   i
	   j
	   (if (= j (+ i 1))
	       (all-values (lookup (ith-word word-string i) lexicon))
	       '())
	   *thin-gc*)))
   (matrix-set! *chart* i j chart-entry)))
 (redraw-display-pane)
 (for-effects
  (let* ((k (an-integer-between 2 (- *n* 1)))
	 (i (an-integer-between 0 (- *n* k 1)))
	 (j (+ i k)))
   (superhighlight (matrix-ref *chart* i j))
   (step)
   (let ((rule (a-member-of *rules*)))
    (message (drop-parentheses (format #f "~s" rule)))
    (let ((k (an-integer-between (+ i 1) (- j 1))))
     (highlight (matrix-ref *chart* i k))
     (highlight (matrix-ref *chart* k j))
     (step)
     (when (and (memq (rule-rhs1 rule)
		      (chart-entry-contents (matrix-ref *chart* i k)))
		(memq (rule-rhs2 rule)
		      (chart-entry-contents (matrix-ref *chart* k j)))
		(not (memq (rule-lhs rule)
			   (chart-entry-contents (matrix-ref *chart* i j)))))
      (set-chart-entry-contents!
       (matrix-ref *chart* i j)
       (cons (rule-lhs rule) (chart-entry-contents (matrix-ref *chart* i j))))
      (redraw-chart-entry (matrix-ref *chart* i j))
      (step))))))
 (memq 's (chart-entry-contents (matrix-ref *chart* 0 (- *n* 1)))))
