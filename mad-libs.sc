(define (a-common-noun)
 (either '(dog) '(cat) '(bus) '(pair) '(apple) '(keyboard) '(book) '(weed)
	 '(microphone)))

(define (a-proper-noun)
 (either '(Lafayette) '(Apple) '(Professor-Siskind) '(Mitch-Daniels)
	 '(Taylor-Swift) '(Lady-Gaga)))

(define (a-determiner)
 (either '(the) '(a) '(some) '(every) '(forty-two)))

;;; NP -> Nprop
;;;    |  DET Ncommon

(define (a-noun-phrase)
 (either (a-proper-noun)
	 (append (a-determiner) (a-common-noun))))

(define (an-intransitive-verb)
 (either '(dies) '(runs) '(ate) '(smoked) '(typed) '(fell) '(jumped)
	 '(happened)))

(define (a-transitive-verb)
 (either '(ate) '(smoked) '(drank) '(sang) '(kissed) '(fired) '(took)))

;;; VP -> Vintans
;;;  |    Vtrans NP

(define (a-verb-phrase)
 (either (an-intransitive-verb)
	 (append (a-transitive-verb) (a-noun-phrase))))

;;; S -> NP VP

(define (a-sentence)
 (append (a-noun-phrase) (a-verb-phrase)))
