# TODO: Develop a console-based Rock Paper Scissors Lizard Spock game in Python
# Game should be modular, allowing for easy updates or rule changes
# Implement game rules:
# - Scissors decapitate lizard
# - Scissors cuts paper
# - Paper covers rock 
# - Rock crushes lizard 
# - Lizard poisons Spock 
# - Spock smashes scissors 
# - Lizard eats paper 
# - Paper disproves Spock 
# - Spock vaporizes rock 
# - Rock crushes scissors
# Include user input for selecting options and display game results

import random
#define global variables
#define dictionary of game options with number to choose from
options = {
    'rock': ['scissors', 'lizard'],
    'paper': ['rock', 'spock'],
    'scissors': ['paper', 'lizard'],
    'lizard': ['spock', 'paper'],
    'spock': ['scissors', 'rock']
}   

#define dictionary of game rules
rules = {
    ('scissors', 'lizard'): 'Scissors decapitate lizard',
    ('scissors', 'paper'): 'Scissors cuts paper',                           
    ('paper', 'rock'): 'Paper covers rock',
    ('rock', 'lizard'): 'Rock crushes lizard',
    ('lizard', 'spock'): 'Lizard poisons Spock',
    ('spock', 'scissors'): 'Spock smashes scissors',
    ('lizard', 'paper'): 'Lizard eats paper',
    ('paper', 'spock'): 'Paper disproves Spock',
    ('spock', 'rock'): 'Spock vaporizes rock',
    ('rock', 'scissors'): 'Rock crushes scissors'
}       

#define dictionary of game results
results = {
    'win': 'You win!',                
    'lose': 'You lose!',
    'tie': "It's a tie!"
}

#define function to get user input
def get_user_choice():
    print("Choose your option:")
    option_list = list(options.keys())
    for idx, option in enumerate(option_list, 1):
        print(f"{idx}. {option}")
    choice = input("Your choice (name or number): ").lower()
    while True:
        if choice in options:
            return choice
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(option_list):
                return option_list[idx]
        print("Invalid choice. Please try again.")
        choice = input("Your choice (name or number): ").lower()

#define fucntion to get computer input
def get_computer_choice():
    print("\nComputer's turn - Choose computer's option:")
    option_list = list(options.keys())
    for idx, option in enumerate(option_list, 1):
        print(f"{idx}. {option}")
    choice = input("Computer's choice (name or number): ").lower()
    while True:
        if choice in options:
            return choice
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(option_list):
                return option_list[idx]
        print("Invalid choice. Please try again.")
        choice = input("Computer's choice (name or number): ").lower()

#define function to determine winner
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie', None
    elif computer_choice in options[user_choice]:
        rule = rules[(user_choice, computer_choice)]
        return 'win', rule
    else:
        rule = rules[(computer_choice, user_choice)]
        return 'lose', rule

#define function to get game result
def get_game_result():
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()
    print("\n" + "="*40)
    print(f"Your choice: {user_choice}")
    print(f"Computer choice: {computer_choice}")
    print("="*40)
    result, rule = determine_winner(user_choice, computer_choice)
    if rule:
        print(rule)
    print(results[result])
    print("\n")
    return result

#Define function to display game results
def display_game_results():
    play_again = 'y'
    while play_again.lower() == 'y':
        get_game_result()
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y' and play_again != 'n':
            print("Invalid input. Please enter 'y' or 'n'.")
            play_again = 'y'
    print("Thanks for playing!")


#define entire main function
def main():
    display_game_results()
if __name__ == "__main__":
    main()


    


