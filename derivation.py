every = (
    lambda noun: (
        lambda noun1: (
            every(lambda x: noun(x)->noun1(x)))))

some = (
    lambda noun: (
        lambda noun1: (
            some(lambda x: noun(x) and noun1(x)))))

pawn = (lambda x: pawn(x))

square = (lambda x: square(x))

moves = (
    lambda subject_np: (
        subject_np(lambda x: moves(x))))

is_on1 = (
    lambda object_np: (
        lambda subject_np: (
            subject_np(lambda x: object_np(lambda y: on(x, y))))))

is_on2 = (
    lambda object_np: (
        lambda subject_np: (
            object_np(lambda y: subject_np(lambda x: on(x, y))))))

on = (
    lambda np: (
        lambda noun: (
            lambda x: (
                noun(x) and np(lambda y: on(x, y))))))

is1 = (
    lambda object_pp: (
        lambda subject_np: (
            subject_np(object_pp(lambda y: True)))))

# every pawn

every(pawn) = (
    (
        lambda noun: (
            lambda noun1: (
                every(lambda x: noun(x)->noun1(x)))))
    (lambda x: pawn(x))
)

every(pawn) = (
    (
        lambda noun: (
            lambda noun1: (
                every(lambda x: noun(x)->noun1(x)))))
    (lambda y: pawn(y))
)

every(pawn) = (
    (lambda noun1: (
            every(lambda x: ((lambda y: pawn(y))(x))->noun1(x)))))

every(pawn) = (
    lambda noun1: (
        every(lambda x: pawn(x)->noun1(x))))

# every pawn moves

moves(every(pawn)) = (
    (lambda subject_np: (
        subject_np(lambda x: moves(x))))
    (lambda noun1: (
        every(lambda x: pawn(x)->noun1(x)))))

moves(every(pawn)) = (
    (lambda subject_np: (
        subject_np(lambda x: moves(x))))
    (lambda noun1: (
        every(lambda y: pawn(y)->noun1(y)))))

moves(every(pawn)) = (
    ((lambda noun1: (
        every(lambda y: pawn(y)->noun1(y))))
     (lambda x: moves(x))))

moves(every(pawn)) = (
    every(lambda y: pawn(y)->
          ((lambda x: moves(x))
           (y))))

moves(every(pawn)) = (every(lambda y: pawn(y)->moves(y)))

# some square

some(square) = (
    (lambda noun: (
        lambda noun1: (
            some(lambda x: noun(x) and noun1(x)))))
    (lambda x: square(x)))

some(square) = (
    (lambda noun: (
        lambda noun1: (
            some(lambda x: (
                noun(x) and noun1(x))))))
    (lambda y: square(y)))

some(square) = (
    lambda noun1: (
        some(lambda x: (
            ((lambda y: square(y))(x)) and noun1(x)))))

every(pawn) = (
    lambda noun1: (
        every(lambda x: pawn(x)->noun1(x))))

some(square) = (
    lambda noun1: (
        some(lambda x: square(x) and noun1(x))))

is_on1 = (
    lambda object_np: (
        lambda subject_np: (
            subject_np(lambda x: object_np(lambda y: on(x, y))))))

# is_on1 some square

is_on1(some(square)) = (
    (lambda object_np: (
        lambda subject_np: (
            subject_np(lambda x: object_np(lambda y: on(x, y))))))
    (lambda noun1: (
        some(lambda x: square(x) and noun1(x)))))

is_on1(some(square)) = (
    (lambda object_np: (
        lambda subject_np: (
            subject_np(lambda x: object_np(lambda y: on(x, y))))))
    (lambda noun1: (
        some(lambda w: square(w) and noun1(w)))))

is_on1(some(square)) = (
    lambda subject_np: (
        subject_np(lambda x:
                   ((lambda noun1: (
                       some(lambda w: square(w) and noun1(w))))
                    (lambda y: on(x, y))))))

is_on1(some(square)) = (
    lambda subject_np: (
        subject_np(
            lambda x: (
                some(lambda w: square(w) and
                     ((lambda y: on(x, y))
                      (w)))))))

is_on1(some(square)) = (
    lambda subject_np: (
        subject_np(
            lambda x: (
                some(lambda w: square(w) and on(x, w))))))

# every pawn is_on1 some square

is_on1(some(square))(every(pawn)) = (
    (lambda subject_np: (
        subject_np(
            lambda x: (
                some(lambda w: square(w) and on(x, w))))))
    (lambda noun1: (
        every(lambda x: pawn(x)->noun1(x)))))

is_on1(some(square))(every(pawn)) = (
    (lambda subject_np: (
        subject_np(
            lambda x: (
                some(lambda w: square(w) and on(x, w))))))
    (lambda noun1: (
        every(lambda z: pawn(z)->noun1(z)))))

is_on1(some(square))(every(pawn)) = (
    ((lambda noun1: (
        every(lambda z: pawn(z)->noun1(z))))
     (lambda x: (
         some(lambda w: square(w) and on(x, w))))))

is_on1(some(square))(every(pawn)) = (
    every(lambda z: pawn(z)->
          ((lambda x: (
            some(lambda w: square(w) and on(x, w))))
           (z))))

is_on1(some(square))(every(pawn)) = (
    every(lambda z: pawn(z)->some(lambda w: square(w) and on(z, w))))

# is_on2 some square

is_on2(some(square)) = (
    (lambda object_np: (
        lambda subject_np: (
            object_np(lambda y: subject_np(lambda x: on(x, y))))))
    (lambda noun1: (
            some(lambda w: square(w) and noun1(w)))))

is_on2(some(square)) = (
    lambda subject_np: (
        ((lambda noun1: (
            some(lambda w: square(w) and noun1(w))))
         (lambda y: subject_np(lambda x: on(x, y))))))

is_on2(some(square)) = (
    lambda subject_np: (
        lambda noun1: (
            some(lambda w: square(w) and
                 ((lambda y: subject_np(lambda x: on(x, y)))
                  (w))))))

is_on2(some(square)) = (
    lambda subject_np: (
        lambda noun1: (
            some(lambda w: square(w) and
                 subject_np(lambda x: on(x, w))))))

# every pawn is_on2 some square

is_on2(some(square))(every(pawn)) = (
    (lambda subject_np: (
        lambda noun1: (
            some(lambda w: square(w) and
                 subject_np(lambda x: on(x, w))))))
    (lambda noun1: (
        every(lambda x: pawn(x)->noun1(x)))))

is_on2(some(square))(every(pawn)) = (
    (lambda subject_np: (
        lambda noun1: (
            some(lambda w: square(w) and
                 subject_np(lambda x: on(x, w))))))
    (lambda noun1: (
        every(lambda z: pawn(z)->noun1(z)))))

is_on2(some(square))(every(pawn)) = (
    lambda noun1: (
        some(lambda w: square(w) and
             ((lambda noun1: (
                 every(lambda z: pawn(z)->noun1(z))))
              (lambda x: on(x, w))))))

is_on2(some(square))(every(pawn)) = (
    some(lambda w: square(w) and
         ((lambda noun1: (
             every(lambda z: pawn(z)->
                   ((lambda x: on(x, w))
                    (z))))))))

# every pawn is_on1 some square
is_on1(some(square))(every(pawn)) = (
    every(lambda z: pawn(z)->some(lambda w: square(w) and on(z, w))))

# every pawn is_on2 some square
is_on2(some(square))(every(pawn)) = (
    some(lambda w: square(w) and (every(lambda z: pawn(z)->on(z, w)))))

# on some square

on(some(square)) = (
    (lambda np: (
            lambda noun: (
                lambda x: (
                    noun(x) and np(lambda y: on(x, y))))))
    (lambda noun1: (
        some(lambda x: square(x) and noun1(x)))))

on(some(square)) = (
    (lambda np: (
            lambda noun: (
                lambda x: (
                    noun(x) and np(lambda y: on(x, y))))))
    (lambda noun1: (
        some(lambda w: square(w) and noun1(w)))))

on(some(square)) = (
    lambda noun: (
        lambda x: (
            noun(x) and ((lambda noun1: (
                some(lambda w: square(w) and noun1(w))))
                         (lambda y: on(x, y))))))

on(some(square)) = (
    lambda noun: (
        lambda x: (
            noun(x) and (
                some(lambda w: square(w) and ((lambda y: on(x, y)) (w)))))))

# is1 on some square

is1(on(some(square))) = (
    (lambda object_pp: (
        lambda subject_np: (
            subject_np(object_pp(lambda y: True)))))
    (lambda noun: (
        lambda x: (
            noun(x) and (
                some(lambda w: square(w) and ((lambda y: on(x, y)) (w))))))))

is1(on(some(square))) = (
    (lambda object_pp: (
        lambda subject_np: (
            subject_np(object_pp(lambda w: True)))))
    (lambda noun: (
        lambda x: (
            noun(x) and (
                some(lambda w: square(w) and ((lambda y: on(x, y)) (w))))))))

is1(on(some(square))) = (
    lambda subject_np: (
        subject_np(
            ((lambda noun: (
                lambda x: (
                    noun(x) and (
                        some(lambda w: square(w) and ((lambda y: on(x, y)) (w)))))))
             (lambda w: True)))))

is1(on(some(square))) = (
    lambda subject_np: (
        subject_np(
            (
                lambda x: (
                    ((lambda w: True)
                     (x))
                    and (
                        some(lambda w: square(w) and ((lambda y: on(x, y)) (w)))))))
    ))

is1(on(some(square))) = (
    lambda subject_np: (
        subject_np(
            (
                lambda x: (
                    True
                    and (
                        some(lambda w: square(w) and ((lambda y: on(x, y)) (w)))))))
    ))

is1(on(some(square))) = (
    lambda subject_np: (
        subject_np(
            (
                lambda x: (
                    some(lambda w:
                         square(w) and ((lambda y: on(x, y)) (w))))))))

is1(on(some(square))) = (
    lambda subject_np: (
        subject_np(lambda x: some(lambda w: square(w) and on(x, w)))))

# every pawn is1 on some square

is1(on(some(square)))(every(pawn)) = (
    (lambda subject_np: (
        subject_np(lambda x: some(lambda w: square(w) and on(x, w)))))
    (lambda noun1: (
        every(lambda x: pawn(x)->noun1(x)))))

is1(on(some(square)))(every(pawn)) = (
    (lambda subject_np: (
        subject_np(lambda x: some(lambda w: square(w) and on(x, w)))))
    (lambda noun1: (
        every(lambda z: pawn(z)->noun1(z)))))

is1(on(some(square)))(every(pawn)) = (
    ((lambda noun1: (
        every(lambda z: pawn(z)->noun1(z))))
     (lambda x: some(lambda w: square(w) and on(x, w)))))

is1(on(some(square)))(every(pawn)) = (
    (every(lambda z: pawn(z)->
              ((lambda x: some(lambda w: square(w) and on(x, w)))
               (z)))))

# every pawn is_on1 some square
is_on1(some(square))(every(pawn)) = (
    every(lambda z: pawn(z)->some(lambda w: square(w) and on(z, w))))

# every pawn is1 on some square
is1(on(some(square)))(every(pawn)) = (
    every(lambda z: pawn(z)->some(lambda w: square(w) and on(z, w))))
