(define (a-common-noun)
 (either '(cat) '(chair) '(blueberry) '(ice-cream) '(dumpster) '(computer)
	 '(weed) '(hair)))

(define (a-proper-noun)
 (either '(Japan) '(Purdue) '(Chipotle) '(Yosemite) '(Donald-Trump)
	 '(Mung-Chiang) '(Elon-Musk) '(Bradon-Smith) '(Taylor-Swift)))

(define (a-determiner)
 (either '(the) '(a) '(some) '(every) '(forty-two)))

;;; NP -> Nprop
;;;    | DET Ncommon

(define (a-noun-phrase)
 (either (a-proper-noun)
	 (append (a-determiner) (a-common-noun))))

(define (an-intransitive-verb)
 (either '(ran) '(spoke) '(ate) '(swam) '(juggled) '(failed) '(passed)
	 '(vomited) '(slept) '(screwed-up)))

(define (a-transitive-verb)
 (either '(pushed) '(pulled) '(slapped) '(kissed) '(smoked) '(fought) '(fired)))

;;; VP -> Vintrans
;;;    |  Vtrans NP

(define (a-verb-phrase)
 (either (an-intransitive-verb)
	 (append (a-transitive-verb) (a-noun-phrase))))

;;; S -> NP VP

(define (a-sentence)
 (append (a-noun-phrase) (a-verb-phrase)))

(define (sentence? words)
 (not (not (member words (all-values (a-sentence))))))
