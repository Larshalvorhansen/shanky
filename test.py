import os

correct = input("Did you get it correct? (n)/Yes (x to exit to menu.): ").strip()

if correct.capitalize() == "YES":  # User got it correct
    print("Correct! Card moved to the next level.")
    print(correct)
    print(correct.capitalize())
elif correct == "x" or correct == "X":
    print("Going back to menu")
else:  # User got it wrong
    print("Incorrect. Card moved back to level 1.")
    writeup = input("Write the answer: ")

print(correct)
print(correct.capitalize())
