from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

#persons = ["A","B","C"]
#title = ["Knight","Knave"]

#Says for puzzle 0
A0says = And(AKnight,AKnave)

#Says for puzzle 1
A1says = And(AKnave,BKnave)

#Says for puzzle 2
A2says = Or(And(AKnave,BKnave),
            And(AKnight,BKnight)
            )

B2says = Or(And(AKnave,BKnight),
            And(AKnight,BKnave)
            )

#Says for puzzle 3
A3says = Or(And(AKnight,Not(AKnave)),
            And(Not(AKnight),AKnave)
            )

B3says = And(And(A3says,BKnave),
            CKnave)   

C3says = AKnight

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
   Biconditional(AKnight,Not(AKnave)),
   Implication(AKnight,A0says),
   Implication(AKnave, Not(A0says)),
   
    
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(AKnight,Not(AKnave)),
    Implication(AKnight,A1says),
    Implication(AKnave, Not(A1says)),
    Biconditional(BKnight,Not(BKnave))
    
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnight,Not(AKnave)),
    Biconditional(BKnight,Not(BKnave)),

    Implication(AKnight,A2says),
    Implication(AKnave, Not(A2says)),

    Implication(BKnight,B2says),
    Implication(BKnave, Not(B2says))
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight,Not(AKnave)),
    Biconditional(BKnight,Not(BKnave)),
    Biconditional(CKnight,Not(CKnave)),

    Implication(AKnight,A3says),
    Implication(AKnave, Not(A3says)),

    Implication(BKnight,B3says),
    Implication(BKnave, Not(B3says)),

    Implication(CKnight,C3says),
    Implication(CKnave, Not(C3says))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]

    print(knowledge0.formula())



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
