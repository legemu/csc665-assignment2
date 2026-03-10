###### --------------------------------------------
## The author of these scripts is T. D. Devlin 
###### --------------------------------------------

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 1
# A says "I am both a knight and a knave."
# ----------------------------------------
##   write the statement(s) in PL 
stat = And(AKnight, AKnave)

##   Fill in the knowledge base
knowledge1 = And(
    Xor(AKnight, AKnave),
    Implication(AKnight, stat),
    Implication(AKnave, Not(stat))
)
# ----------------------------------------

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# ----------------------------------------
##   write the statement(s) in PL 
A_stat = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave)
    )
B_stat = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight)
    )

##   Fill in the knowledge base
knowledge2 = And(
    # world rules
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),

    # A's truth rules
    Implication(AKnight, A_stat),
    Implication(AKnave, Not(A_stat)),

    # B's truth rules
    Implication(BKnight, B_stat),
    Implication(BKnave, Not(B_stat))
)
# ----------------------------------------

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# ----------------------------------------
##   write the statement(s) in PL 

# A's possible statements
A_possible_knight = Symbol("A_possible_knight")
A_possible_knave = Symbol("A_possible_knave")

# The truth values of A's possible statements
A_knight_claim = AKnight
A_knave_claim = AKnave

B_stat1 = A_possible_knave
B_stat2 = CKnave

C_stat = AKnight

##   Fill in the knowledge base
knowledge3 = And(
    # world rules
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    Xor(CKnight, CKnave),

    # A said exactly one of these two statements
    Xor(A_possible_knight, A_possible_knave),

    # A's truth rules
    Implication(AKnight, Implication(A_possible_knight, A_knight_claim)),
    Implication(AKnight, Implication(A_possible_knave, A_knave_claim)),
    Implication(AKnave, Implication(A_possible_knight, Not(A_knight_claim))),
    Implication(AKnave, Implication(A_possible_knave, Not(A_knave_claim))),

    # B's truth rules
    Implication(BKnight, B_stat1),
    Implication(BKnight, B_stat2),
    Implication(BKnave, Not(B_stat1)),
    Implication(BKnave, Not(B_stat2)),

    # C's truth rules
    Implication(CKnight, C_stat),
    Implication(CKnave, Not(C_stat))
)
# ----------------------------------------


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
