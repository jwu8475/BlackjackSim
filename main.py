# Importing the random library for generating a random number.
import random

# Generates a deck of 52 cards with appropriate suits as a set
def generateDeck():
    deck = set()
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    for card in cards:
        deck.add(f"{card}♦")
        deck.add(f"{card}♥")
        deck.add(f"{card}♣")
        deck.add(f"{card}♠")
    return deck

# Function that counts the cards
# If a card that is 2,3,4,5,6 is revealed, add 1
# If a card that is 7,8,9 is revealed, nothing happens
# If a card that is A,J,Q,K is revealed, subtract 1
def countCards(hand):
    counter = 0
    for card in hand:
        cardValue = card[:-1]
        positive = ["2", "3", "4", "5", "6"]
        negative = ["A", "10", "J", "Q", "K"]
        if cardValue in positive:
            counter += 1
        elif cardValue in negative:
            counter -= 1
    return counter

# Function that has 20% chance of quizzing the user at certain points in the game
def quiz(counter):
    randomInt = random.randint(1,5)
    if randomInt == 5:
        while True:
            try:
                answer = int(input("\nCurrent Count: "))
            except ValueError:
                print("Please enter a number.")
            else:
                if answer == counter:
                    print("You are correct!")

                else:
                    print(f"Incorrect. Current Count: {counter}")
                return answer == counter

# Counts the amount of correct and incorrect answers from the user and tallies it
def quizTally(right, wrong, counter):
    result = quiz(counter)
    if result == True:
        right += 1
    elif result == False:
        wrong += 1
    return [right, wrong]

# Converts the hand of cards into integer values
def convertHand(hand):
    for i in range(len(hand)):
        # Slices the suit
        hand[i] = hand[i][:-1]
        # 10,J,Q,K all have a value of 10
        if hand[i] in ["10", "J", "Q", "K"]:
            hand[i] = 10
        # If card is an Ace, value is an 11 if user only has two cards in the hand and there is only 1 Ace in the hand
        elif hand[i] == "A":
            if i in [0, 1] and len(hand) == 2 and hand[0] != hand[1]:
                    hand[i] = 11
            else:
                hand[i] = 1
        else:
            hand[i] = int(hand[i])
    return hand

# Gameplay logic (Hit, Stand, Split) of the players and dealer
def play(hand, deck, counter, split = False, dealer = False):
    # create shallow copy of hand
    originalHand = hand[:]
    action = ''

    # call function to convert hand into integers
    if type(hand[0]) == str:
        convertHand(hand)
    
    # Calculates current hand value
    handVal = 0
    for card in hand:
        if card == 11 and len(hand) > 2:
            card = 1
        handVal += card

    # Only print when it is a player to avoid cluttering the terminal
    if dealer == False:
        print("\nCurrent hand: ", handVal)

    # Check for >= 21
    if handVal >= 21:
        if handVal == 21:
            print("\n21!")
        else:
            print("\nBusted!")
        return [handVal], counter
    
    # If it is a dealer, no need to require user input
    # Dealers also cannot split
    while dealer == True:
        if handVal < 17:
            action = "H"
        else:
            action = "S"
        break

    # If it is a player, ask if they want to hit, stand or split (if available).
    while dealer == False:
        if len(hand) == 2 and hand[0] == hand[1] and split == False:
            action = input("Would you like to hit(H), stand(S), or split(SP)? ")
        else:
            action = input("Would you like to hit(H) or stand(S)? ")
        
        if action in ["H", "S"]:
            break
        if action == "SP" and split == False:
            break
        else:
            print("Invalid Action.")

    # Hit, Stand, Split logic
    match action:
        # Grab new card from deck -> count the card -> convert new card to integer -> recursively call play function for next action
        case "H":
            newCard = deck.pop()
            counter += countCards([newCard])
            print(f"\n{newCard}")
            hand += convertHand([newCard])
            # If it is a dealer, must make sure dealer parameter is TRUE.
            if dealer == True:
                return play(hand, deck, counter, False, True)
            return play(hand, deck, counter)
        # Stand action means the current hand is complete.
        # Returns hand value and card counter.
        case "S":
            return [handVal], counter
        # Split requires splitting hand into two hand, which means one new card per hand.
        case "SP":
            # Similar to Hit; no dealer logic because dealer can't split
            print("First Hand: ")
            newCard = deck.pop()
            counter += countCards([newCard])
            print([originalHand[0], newCard])
            firstHand, counter = play([originalHand[0], newCard], deck, counter, True)

            # Similar to Hit; no dealer logic because dealer can't split
            print("Second Hand: ")
            newCard = deck.pop()
            counter += countCards([newCard])
            print([originalHand[1], newCard])
            secondHand, counter = play([originalHand[1], newCard], deck, counter, True)

            # Returns both hands in a list and counter
            return firstHand + secondHand, counter

# Function for defining amount of players at the table.        
def definePlayerCount():
    players = 0
    while True:
        try:
            players = int(input("Please enter the amount of players at the table: "))
        except ValueError:
            print("Please a valid number.")
        else:
            break
    return players

# Main program
def main():

    # Defining variables
    turn = 1
    playerCount = 0
    gameInProgress = False
    cardCount = 0
    deck = generateDeck()
    correctGuess = 0
    incorrectGuess = 0

    # Print a message to greet the user
    # Print rules and constraints of the blackjack program
    print("Welcome to this simulated blackjack where you can practice card counting!\n")
    print("Here are the card counting rules that are followed: ")
    print("  2, 3, 4, 5, 6 -> +1")
    print("  7, 8, 9 -> 0")
    print("  10, J, Q, K, A -> -1\n")
    print("This simulation also has a few constraints: ")
    print(" - No Double Down")
    print(" - Max one split per hand")
    print(" - Max 3 players per table\n")

    # The number of players at the table defined.
    playerCount = definePlayerCount()

    # Handles edge cases for player count (0 < player count < 4)
    if playerCount == 0:
        print("\nI cannot start a game of blackjack without any players.")
    elif playerCount > 3:
        print("\nI cannot start a game of blackjack with more than 3 players.")
    else:
        print(f"\nI have confirmed that there will be {playerCount} player{'s' if playerCount > 1 else ''} in the game.\n")

        # Determines whether to start the game or not.
        confirmStart = ""
        while confirmStart != "Y" and confirmStart != "N":
            confirmStart = input("Would you like to start the game? (Y/N) ")
            if confirmStart == "Y":
                gameInProgress = True
            elif confirmStart == "N":
                print("Please come back when you are ready to play.")
            else:
                print("Please enter either Y or N.")

    # Loops while game in progress
    while gameInProgress:
        # Game Start
        print(f"\nRound {turn}")

        # Set dealer hand to two values from the deck
        dealerHand = [deck.pop(), deck.pop()]

        # Card counting functionality
        cardCount += countCards([dealerHand[0]])

        # Dealer hand displayed to user.
        # Second card hidden till all players stand
        print(f"Dealer's hand: {dealerHand[0]}, _")

        # Potential Random quiz
        [correctGuess, incorrectGuess] = quizTally(correctGuess, incorrectGuess, cardCount)

        # Each player at the table plays their blackjack hand.
        # Includes: counting card internally, potential quiz, and tally of whether the user answered the quiz correctly.
        playerHands = {}
        for i in range(playerCount):
            initialHand = [deck.pop(), deck.pop()]
            cardCount += countCards(initialHand)
            print(f"\nPlayer {i+1}'s hand: \n", initialHand)
            [correctGuess, incorrectGuess] = quizTally(correctGuess, incorrectGuess, cardCount)
            finalScores, cardCount = play(initialHand, deck, cardCount)
            playerHands[f"Player {i+1}"] = finalScores
        
        # Summary of current state of the board.
        # Player hands are shown as the total value of their hand(s).
        print("  _________________________")
        print("||Summary:")
        print(f"||Dealer's hand: [{dealerHand[0]}, _]")
        for player in playerHands:
            print(f"||{player}: {playerHands[player]}")
        print("||")
        print("||")
        print("||_________________________")

        # Dealer reveals their second card and plays their hand
        # Dealers must hit until their have is > 16
        # Includes: counting card internally, potential quiz, and tally of whether the user answered the quiz correctly.
        print(f"\nDealer: \n{dealerHand}")
        cardCount += countCards([dealerHand[1]])
        [correctGuess, incorrectGuess] = quizTally(correctGuess, incorrectGuess, cardCount)
        [dealerSum], cardCount = play(dealerHand, deck, cardCount, False, True)
        print(f"\nDealer's Hand Value: \n{dealerSum}")

        # Determines which player won and how many hands they won.
        if dealerSum > 21:
            print("\nDealer Busted!")
        for player in playerHands:
            handsWon = 0
            for hands in playerHands[player]:
                if hands > dealerSum and hands < 22:
                    handsWon += 1
                # If dealer busted, players that have not busted automatically win!
                elif hands < 22 and dealerSum > 21:
                    handsWon += 1
            if handsWon > 0:
                print(f"\n{player} wins {handsWon} hand{'s' if handsWon > 1 else ''}!")
            else:
                print(f"\n{player} was not a winner.")

        # Asks the user if they want to continue playing
        # The deck also gets reshuffled if
        #   - Players at the table are changed
        #   - Deck has less than 21 cards remaining
        while True:
            cont = input("\nContinue playing? (Y/N) ")
            if cont == "Y":
                turn += 1
                while True:
                    samePlayers = input("Would you like to keep the same amount of players ('Y' prompts a reshuffling of the deck)? (Y/N) ")
                    if samePlayers == "Y" or samePlayers == "N":
                        break
                    else:
                        print("Please enter either Y or N.")
                if len(deck) < 21 or samePlayers == "N":
                    if samePlayers == "N":
                        playerCount = definePlayerCount()
                    print("\nReshuffling...")
                    cardCount = 0
                    # Reshuffling is simply regenerating a new deck of cards
                    deck = generateDeck()
                break

            # If user wants to stop playing blackjack, game ends.
            # User is informed of how many card counting quizzes they got right.
            # User is informed of their final accuracy.
            # User is thanked for playing the game.
            elif cont == "N":
                gameInProgress = False
                print("Your Score:")
                print(f"{correctGuess}/{correctGuess + incorrectGuess} correct")
                print("\nFinal Accuracy:")
                print(f"{round((correctGuess/(correctGuess + incorrectGuess))*100, 2)}%")
                print("\nThank you for playing blackjack simulation.")
                break
            else:
                print("Please enter either Y or N.")

main()
