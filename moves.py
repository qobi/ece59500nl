typedef S = boolean
typedef N = object->S
typedef D = N->NP
typedef VP = S<-NP
typedef NP = N->S

every = (lambda noun:
         (lambda noun1:
          (all(lambda x: noun(x)->noun1(x)))))

pawn = (lambda x: pawn(x))

moves = (lambda subject_np:
         (subject_np(lambda x: moves(x))))

pawn:N
every:D
moves:VP

every(pawn):NP
moves(every(pawn)):S

every(pawn) = ((lambda noun:
                (lambda noun1:
                 (all(lambda x: noun(x)->noun1(x)))))
               (lambda x: pawn(x)))

every(pawn) = ((lambda noun:
                (lambda noun1:
                 (all(lambda y: noun(y)->noun1(y)))))
               (lambda x: pawn(x)))

every(pawn) = (lambda noun1:
               (all(lambda y: (lambda x: pawn(x))(y)->noun1(y))))

every(pawn) = (lambda noun1:
               (all(lambda y: pawn(y)->noun1(y))))

moves(every(pawn)) = ((lambda subject_np:
                       (subject_np(lambda x: moves(x))))
                      (lambda noun1:
                       (all(lambda y: pawn(y)->noun1(y)))))

moves(every(pawn)) = ((lambda noun1:
                       (all(lambda y: pawn(y)->noun1(y))))
                      (lambda x: moves(x)))

moves(every(pawn)) = (all(lambda y: pawn(y)->(lambda x: moves(x))(y)))

moves(every(pawn)) = (all(lambda y: pawn(y)->moves(y)))
