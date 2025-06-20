import csv
import os
import time

# Directory where decks are stored
DECKS_DIR = "./decks"

ascii_art = """

███████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗██╗   ██╗
██╔════╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝╚██╗ ██╔╝
███████╗███████║███████║██╔██╗ ██║█████╔╝  ╚████╔╝ 
╚════██║██╔══██║██╔══██║██║╚██╗██║██╔═██╗   ╚██╔╝  
███████║██║  ██║██║  ██║██║ ╚████║██║  ██╗   ██║   
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   

"""


def load_deck(deck):
    """Loads a deck (CSV file) and returns a list of cards."""
    deck_path = os.path.join(DECKS_DIR, f"{deck}.csv")
    if not os.path.exists(deck_path):
        print(f"Error: Deck '{deck}' does not exist.")
        return []
    try:
        with open(deck_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            cards = []
            for row in reader:
                # Ensure a default "score" field exists for sorting and tracking
                row.setdefault("score", "1")
                # Validate and ensure "score" is at least 1
                try:
                    if int(row["score"]) < 1:
                        row["score"] = "1"
                except ValueError:
                    row["score"] = "1"
                cards.append(row)
            if not cards:
                print(f"Error: Deck '{deck}' is empty or corrupt.")
            return cards
    except Exception as e:
        print(f"Error loading deck '{deck}': {e}")
        return []


def print_card(content):
    """Prints content surrounded by ASCII art to look like a card."""
    border = "┌" + "─" * (len(content) + 4) + "┐"
    padding = "│" + " " * (len(content) + 4) + "│"
    content_line = f"│  {content}  │"
    bottom_border = "└" + "─" * (len(content) + 4) + "┘"

    print(border)
    print(padding)
    print(content_line)
    print(padding)
    print(bottom_border)


def practice(deck, num_cards="10"):
    """Starts a practice session for a specific deck using the Leitner system."""
    cards = load_deck(deck)
    if not cards:
        return

    # Dynamically get field names from the first card
    if cards:
        fields = list(cards[0].keys())
    else:
        print(f"Error: Deck '{deck}' is empty.")
        return

    # Exclude the "score" field from practice questions
    fields.remove("score")

    # Check if all cards are perfect (score 5)
    if all(int(card.get("score", 1)) == 5 for card in cards):
        print(
            "All the cards in this deck are practiced to perfection! You can reset the deck if you want to practice it again."
        )
        return

    # Parse the number of cards to practice
    if num_cards.lower() == "a":  # 'a' for all cards
        num_cards = len(cards)
    elif num_cards.isdigit():
        num_cards = int(num_cards)
    else:  # Default to 10 if input is invalid
        num_cards = 10

    # Ensure cards are sorted by score (lower scores are reviewed first)
    try:
        cards.sort(
            key=lambda x: int(x.get("score", 1))
        )  # Default score is 1 if missing
    except ValueError:
        print("Error: Invalid score value in deck.")
        return

    practiced = 0
    total_cards = len(cards)

    while practiced < num_cards:
        breakflag = False
        for card in cards:
            if practiced >= num_cards:
                break

            # Determine if the card should be reviewed based on its score
            score = int(card.get("score", 1))  # Default score is 1
            if should_review_score(score):
                # Display the first field dynamically in a card format
                question_field = fields[0]
                info = "What is the capital of:"
                print()
                print(info)
                print_card(card[question_field])

                input("Press Enter when ready to see the answer... ")
                # Show the "answer" by displaying all fields except the question
                print("Answer:")
                for field in fields:
                    if field != question_field:
                        answer = card[field]
                        print(f"  {field.capitalize()}: {answer}")
                print(f"  Score: {card['score']}")

                # Ask if the user got it correct
                correct = input(
                    "Did you get it correct? (n)/Yes (x to exit to menu.): "
                ).strip()

                if correct.capitalize() == "Yes":  # User got it correct
                    card["score"] = str(
                        min(5, score + 1)
                    )  # Move to the next Leitner box (up to 5)
                    print("Correct! Card moved to the next level.")
                elif correct == "x" or correct == "X":
                    print("Going back to menu")
                    return
                else:  # User got it wrong
                    card["score"] = "1"  # Reset to Box 1
                    print("Incorrect. Card moved back to level 1.")
                    writeup = input("Feel free to type the answer: ")
                    if writeup.capitalize() == answer:
                        print("Correct")

                # Save the card's updated state immediately
                save_deck(deck, cards)

                practiced += 1

    print(
        f"\nPractice session complete for deck '{deck}'. You practiced {practiced} card(s)."
    )
    input("Press enter to go back to the menu.")


def should_review_score(score):
    """Determines if a card with the given score should be reviewed."""
    import random

    score = max(int(score), 1)  # Ensure score is at least 1 to avoid division by zero
    return random.random() < (1 / score)  # Higher scores are less likely to be reviewed


def save_deck(deck, cards):
    """Saves a list of cards back to the CSV file."""
    deck_path = os.path.join(DECKS_DIR, f"{deck}.csv")
    try:
        if cards:
            # Dynamically determine fieldnames from the card keys
            fieldnames = list(cards[0].keys())
        else:
            print(f"Error: No cards to save for deck '{deck}'.")
            return

        with open(deck_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cards)
    except Exception as e:
        print(f"Error saving deck '{deck}': {e}")


def reset_decks():
    """Sets all card scores in all decks to 0."""
    for file in os.listdir(DECKS_DIR):
        if file.endswith(".csv"):
            deck = file[:-4]  # Remove '.csv' extension
            reset_deck(deck)


def reset_deck(deck):
    """Sets all card scores in a specific deck to 1."""
    cards = load_deck(deck)
    if not cards:
        return
    for card in cards:
        card["score"] = "1"  # Reset the score
    save_deck(deck, cards)
    print(f"All cards in deck '{deck}' have been reset to score 1.")
    input("Press enter to go back to the menu.")


def spaced_repetition_score_update(score, rating):
    """
    Updates the score of a card using spaced repetition principles.
    Higher scores mean the card is shown less frequently.
    """
    try:
        score = int(score)
        rating = int(rating)

        # Adjust score based on rating (simplified SRS logic)
        if rating == 5:
            score += 2  # Easy card, less frequent review
        elif rating == 4:
            score += 1  # Somewhat easy, slightly less frequent
        elif rating == 3:
            pass  # Neutral rating, no change
        elif rating == 2:
            score = max(score - 1, 0)  # Slightly difficult, more frequent
        elif rating == 1:
            score = max(score - 2, 0)  # Very difficult, much more frequent
        elif rating == 0:
            score = max(score - 3, 0)  # Forgotten card, immediate review

        return score
    except ValueError:
        print("Error: Invalid score or rating value.")
        return 0


def generate_statistics(deck_name):
    """Loads a deck (CSV file) and prints statistics."""
    # Ensure the deck file has the .csv extension
    deck_path = os.path.join(DECKS_DIR, f"{deck_name}.csv")

    if not os.path.exists(deck_path):
        print(f"Error: Deck '{deck_name}' does not exist.")
        return

    # Initialize score counts for 1-5
    scores_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_cards = 0
    total_score = 0  # Calculated based on completeness percentages

    # Map scores to their corresponding completeness percentages
    score_completeness = {
        1: 0,  # 20%
        2: 0.25,  # 40%
        3: 0.5,  # 60%
        4: 0.75,  # 80%
        5: 1,  # 100%
    }

    with open(deck_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            score = int(row["score"])
            if score not in scores_count:
                print(f"Warning: Invalid score '{score}' in data.")
                continue
            scores_count[score] += 1
            total_cards += 1
            # Add the percentage completeness for this card's score
            total_score += score_completeness[score]

    print("Number of cards with score:")
    for score in range(1, 6):  # Loop through scores 1-5
        print(f"{score}: {scores_count[score]}")

    print(f"Number of cards in deck: {total_cards}")

    # Overall completeness in percentage
    overall_completeness = (total_score / total_cards) * 100 if total_cards > 0 else 0
    print(f"Overall completeness: {overall_completeness:.2f}%")
    input("Press enter to go back to the menu.")


def list_available_decks():
    """Lists all available decks in the DECKS_DIR directory."""
    print("\nAvailable decks:")
    decks = [file[:-4] for file in os.listdir(DECKS_DIR) if file.endswith(".csv")]
    if decks:
        for deck in decks:
            print(f"  - {deck}")
    else:
        print("No decks available.")
    return decks


def printWelcomeScreen():
    print()
    print("Welcome to")
    print(ascii_art)
    print("A simple flascard app")
    print("for the terminal!")


def main():
    """Main function to handle commands."""
    printWelcomeScreen()
    while True:
        print("\nAvailable Commands:")
        print("  practice (p)           - Starts practice session for chosen deck.")
        print("  reset-deck (r)         - Sets all card scores in chosen deck to 1.")
        print("  reset-all-decks (ra)   - Sets all card scores in all decks to 1.")
        print("  get-statistics (gs)    - Prints statistics for a specified deck.")
        print("  quit (q)               - Exit the program.")
        print("  help (h)")

        # Strip whitespace from the input command
        command = input("\nEnter a command: ").strip()

        # Normalize shorthand commands to their full versions
        if command == "ra":
            command = "reset-all-decks"
        elif command == "r":
            command = "reset-deck"
        elif command == "p":
            command = "practice"
        elif command == "gs":
            command = "get-statistics"
        elif command == "q":
            command = "quit"
        elif command == "h":
            command = "help"

        # Handle the normalized commands
        if command == "reset-all-decks":
            if (
                input(
                    "Are you sure you want to reset the score of all the decks?(yes/no) "
                )
                == "yes"
            ):
                reset_decks()
            else:
                print("All your decks have been reset! ...")
                time.sleep(2)
                print("Prank! They are all good.")
                time.sleep(1)
        elif command.startswith("reset-deck"):
            args = command.split(" ", 1)
            if len(args) > 1:
                reset_deck(args[1])
            else:
                deck = input("Which deck would you like to reset? ").strip()
                if deck:
                    reset_deck(deck)
                else:
                    print("Error: No deck specified. Reset aborted.")
        elif command.startswith("practice"):
            # List available decks
            available_decks = list_available_decks()
            if not available_decks:
                print("No decks available for practice.")
                continue

            # Ask the user to select a deck
            deck = input("Which deck would you like to practice? ").strip()
            if deck in available_decks:
                num_cards = input(
                    "How many cards would you like to practice? (Press Enter for default 10, 'a' for all cards): "
                ).strip()
                practice(deck, num_cards)
            else:
                print("Error: Specified deck does not exist. Practice session aborted.")
        elif command.startswith("get-statistics"):
            args = command.split(" ", 1)
            if len(args) > 1:
                generate_statistics(args[1])
            else:
                deck = input("Enter the name of the deck to analyze: ").strip()
                if deck:
                    generate_statistics(deck)
                else:
                    print("Error: No deck specified. Statistics request aborted.")
        elif command == "help":
            print("Sorry, no help to be found here!")
            print("However, you could shoot me an email")
            print("and I might have look at it!")
            print("larshalvorhansen1@gmail.com")
            input("Press enter to go back to the menu.")
        elif command == "quit":
            print("Exiting program. Goodbye!")
            break
        else:
            print(f"Error: '{command}' is not a valid command.")


# Run the program
if __name__ == "__main__":
    main()
