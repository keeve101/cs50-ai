from re import I
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

premise_1 = Or(AKnave, AKnight)
premise_2 = Or(BKnave, BKnight)
premise_3 = Or(CKnave, CKnight)
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Implication(AKnight, And(AKnight, AKnave)), Implication(AKnave, Not(And(AKnave, AKnight))),
    Or(AKnave, AKnight)
    
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight,AKnave), Or(BKnave, BKnight), 
    Implication(AKnight, And(AKnave, BKnave)), 
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    premise_1,
    premise_2,
    Implication(AKnight, And(AKnight, BKnight)),

    Implication(AKnave, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    Implication(BKnight, And(AKnave, BKnight)),

    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.

# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    premise_1,
    premise_2,
    premise_3,
    Biconditional(BKnight, CKnave),
    Biconditional(BKnave, CKnight),
    Biconditional(CKnight, AKnight),
    Biconditional(CKnave, AKnave),
    Implication(AKnight, BKnave),
    Implication(AKnave, BKnave)


)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
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
