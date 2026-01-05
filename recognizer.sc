(define (strip-a-word words lexicon)
 (if (null? words)
     (fail)
     (if (not (member (first words) lexicon))
	 (fail)
	 (rest words))))

(define (strip-a-common-noun words)
 (strip-a-word words
	       '(cat chair blueberry ice-cream dumpster computer weed hair)))

(define (strip-a-proper-noun words)
 (strip-a-word
  words
  '(Japan Purdue Chipotle Yosemite Donald-Trump Mung-Chiang Elon-Musk
	  Bradon-Smith Taylor-Swift)))

(define (strip-a-determiner words)
 (strip-a-word words '(the a some every forty-two)))

;;; NP -> Nprop
;;;    | DET Ncommon

(define (strip-a-noun-phrase words)
 (either (strip-a-proper-noun words)
	 (strip-a-common-noun (strip-a-determiner words))))

(define (strip-an-intransitive-verb  words)
 (strip-a-word words '(ran spoke ate swam juggled failed passed vomited slept
			   screwed-up)))

(define (strip-a-transitive-verb words)
 (strip-a-word words '(pushed pulled slapped kissed smoked fought fired)))

;;; VP -> Vintrans
;;;    |  Vtrans NP

(define (strip-a-verb-phrase words)
 (either (strip-an-intransitive-verb words)
	 (strip-a-noun-phrase (strip-a-transitive-verb words))))

;;; S -> NP VP

(define (strip-a-sentence words)
 (strip-a-verb-phrase (strip-a-noun-phrase words)))

(define (sentence? words)
 (not (not (member #t (all-values (null? (strip-a-sentence words)))))))
