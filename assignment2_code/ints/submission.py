############################################################
# Problem 4: Odd and even integers
from typing import Tuple, List
from logic import *


# Return the following 6 laws. Be sure your formulas are exactly in the order specified.
# 0. Each number $x$ has exactly one successor, which is not equal to $x$.
# 1. Each number is either even or odd, but not both.
# 2. The successor number of an even number is odd.
# 3. The successor number of an odd number is even.
# 4. For every number $x$, the successor of $x$ is larger than $x$.
# 5. Larger is a transitive property: if $x$ is larger than $y$ and $y$ is
#    larger than $z$, then $x$ is larger than $z$.
# Query: For each number, there exists an even number larger than it.
def ints() -> Tuple[List[Formula], Formula]:
    def Even(x): return Atom('Even', x)  # whether x is even

    def Odd(x): return Atom('Odd', x)  # whether x is odd

    def Successor(x, y): return Atom('Successor', x, y)  # whether x's successor is y

    def Larger(x, y): return Atom('Larger', x, y)  # whether x is larger than y

    # Note: all objects are numbers, so we don't need to define Number as an
    # explicit predicate.
    #
    # Note: pay attention to the order of arguments of Successor and Larger.
    # Populate `formulas` with the 6 laws above.
    #
    # Hint: You might want to use the Equals predicate, defined in logic.py.  This
    # predicate is used to assert that two objects are the same.
    formulas = []
    # BEGIN_YOUR_CODE (our solution is 16 lines of code, but don't worry if you deviate from this)
    law0 = Forall('$x', Exists('$y',
                               And(
                                   Successor('$x', '$y'),
                                   And(
                                       Not(Equals('$x', '$y')),
                                       Forall('$z',
                                              Implies(
                                                  Successor('$x', '$z'),
                                                  Equals('$z', '$y')
                                                  )
                                                )
                                            )
                                        )
                                    )
                                )
    
    law1 = Forall('$x',
                  And(
                      Or(Odd('$x'), Even('$x')),
                      Not(And(Odd('$x'), Even('$x')))
                      )
                    )
    
    law2 = Forall('$x', Forall('$y',
                               Implies(
                                   And(
                                       Successor('$x', '$y'),
                                       Even('$x')
                                    ),
                                   Odd('$y')
                                   )
                                )
                            )
    
    law3 = Forall('$x', Forall('$y',
                               Implies(
                                   And(
                                       Successor('$x', '$y'),
                                       Odd('$x')
                                    ),
                                   Even('$y')
                                   )
                                )
                            )
    
    law4 = Forall('$x', Forall('$y',
                               Implies(
                                   Successor('$x', '$y'),
                                   Larger('$y', '$x')
                                )
                            )
                        )
    
    law5 = Forall('$x',
                  Forall('$y',
                         Forall('$z', Implies(
                             And(
                                 Larger('$x', '$y'),
                                 Larger('$y', '$z')
                             ),
                             Larger('$x', '$z')
                             )
                        )
                    )
                )
    
    formulas = [law0, law1, law2, law3, law4, law5]
    # END_YOUR_CODE
    query = Forall('$x', Exists('$y', And(Even('$y'), Larger('$y', '$x'))))
    return formulas, query