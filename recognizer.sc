(define (strip-a-word words lexicon)
 (if (null? words)
     (fail)
     (if (not (member (first words) lexicon))
	 (fail)
	 ;; words[1:]
	 (rest words))))

(define (strip-a-common-noun words)
 (strip-a-word words '(dog cat bus pair apple keyboard book weed microphone)))

(define (strip-a-proper-noun words)
 (strip-a-word
  words
  '(Lafayette Apple Professor-Siskind Mitch-Daniels Taylor-Swift Lady-Gaga)))

(define (strip-a-determiner words)
 (strip-a-word words '(the a some every forty-two)))

;;; NP -> Nprop
;;;    |  DET Ncommon

(define (strip-a-noun-phrase words)
 (either (strip-a-proper-noun words)
	 (strip-a-common-noun (strip-a-determiner words))))

(define (strip-an-intransitive-verb words)
 (strip-a-word words '(dies runs ate smoked typed fell jumped happened)))

(define (strip-a-transitive-verb words)
 (strip-a-word words '(ate smoked drank sang kissed fired took)))

;;; VP -> Vintans
;;;  |    Vtrans NP

(define (strip-a-verb-phrase words)
 (either (strip-an-intransitive-verb words)
	 (strip-a-noun-phrase (strip-a-transitive-verb words))))

;;; S -> NP VP

(define (strip-a-sentence words)
 (strip-a-verb-phrase (strip-a-noun-phrase words)))

(define (sentence? words)
 (not (not (member #t (all-values (null? (strip-a-sentence words)))))))
