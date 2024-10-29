import random

# Function generate deck()
def generateDeck():
    deck = set()
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    for card in cards:
        deck.add(f"{card}♦")
        deck.add(f"{card}♥")
        deck.add(f"{card}♣")
        deck.add(f"{card}♠")
    return deck

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

# Function quiz(current count)
def quiz(counter):
    randomInt = random.randint(5,5)
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

def quizTally(right, wrong, counter):
    result = quiz(counter)
    if result == True:
        right += 1
    elif result == False:
        wrong += 1
    return [right, wrong]

# Function play(current hand and current deck)
def convertHand(hand):
    for i in range(len(hand)):
        hand[i] = hand[i][:-1]
        if hand[i] in ["10", "J", "Q", "K"]:
            hand[i] = 10
        elif hand[i] == "A":
            if i in [0, 1] and len(hand) == 2 and hand[0] != hand[1]:
                    hand[i] = 11
            else:
                hand[i] = 1
        else:
            hand[i] = int(hand[i])
    return hand

def play(hand, deck, counter, split = False, dealer = False):
    originalHand = hand[:]
    action = ''
    # Convert
    if type(hand[0]) == str:
        convertHand(hand)
    
    handVal = 0
    for card in hand:
        if card == 11 and len(hand) > 2:
            card = 1
        handVal += card

    if dealer == False:
        print("\nCurrent hand: ", handVal)

    # check for >= 21
    if handVal >= 21:
        if handVal == 21:
            print("\n21!")
        else:
            print("\nBusted!")
        return [handVal], counter
    
    while dealer == True:
        if handVal < 17:
            action = "H"
        else:
            action = "S"
        break

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

    match action:
        case "H":
            newCard = deck.pop()
            counter += countCards([newCard])
            print(f"\n{newCard}")
            hand += convertHand([newCard])
            if dealer == True:
                return play(hand, deck, counter, False, True)
            return play(hand, deck, counter)
        case "S":
            return [handVal], counter
        case "SP":
            print("First Hand: ")
            newCard = deck.pop()
            counter += countCards([newCard])
            print([originalHand[0], newCard])
            firstHand, counter = play([originalHand[0], newCard], deck, counter, True)

            print("Second Hand: ")
            newCard = deck.pop()
            counter += countCards([newCard])
            print([originalHand[1], newCard])
            secondHand, counter = play([originalHand[1], newCard], deck, counter, True)

            return firstHand + secondHand, counter
            
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

def main():

    turn = 1
    playerCount = 0
    gameInProgress = False
    cardCount = 0
    deck = generateDeck()
    correctGuess = 0
    incorrectGuess = 0

    # Print a message to greet the user
    # Print rules and restraints of the blackjack program
    print("Welcome to this simulated blackjack where you can practice card counting!\n")
    print("Here are the card counting rules that are followed: ")
    print("  2, 3, 4, 5, 6 -> +1")
    print("  7, 8, 9 -> 0")
    print("  10, J, Q, K, A -> -1\n")
    print("This simulation also has a few constraints: ")
    print(" - No Double Down")
    print(" - Max one split per hand")
    print(" - Max 3 players per table\n")

    playerCount = definePlayerCount()

    if playerCount == 0:
        print("\nI cannot start a game of blackjack without any players.")
    # User Input of confirmation to start the game (sets game in progress to true)
    elif playerCount > 3:
        print("\nI cannot start a game of blackjack with more than 3 players.")
    else:
        print(f"\nI have confirmed that there will be {playerCount} player{'s' if playerCount > 1 else ''} in the game.\n")

        confirmStart = ""
        while confirmStart != "Y" and confirmStart != "N":
            confirmStart = input("Would you like to start the game? (Y/N) ")
            if confirmStart == "Y":
                gameInProgress = True
            elif confirmStart == "N":
                print("Please come back when you are ready to play.")
            else:
                print("Please enter either Y or N.")

    # Loop while the game in progress is true
    while gameInProgress:
        # Set dealer hand to two popped values from the deck
        print(f"\nRound {turn}")
        dealerHand = [deck.pop(), deck.pop()]
        cardCount += countCards([dealerHand[0]])
        print(f"Dealer's hand: {dealerHand[0]}, _")
        [correctGuess, incorrectGuess] = quizTally(correctGuess, incorrectGuess, cardCount)
        playerHands = {}
        for i in range(playerCount):
            initialHand = [deck.pop(), deck.pop()]
            cardCount += countCards(initialHand)
            print(f"\nPlayer {i+1}'s hand: \n", initialHand)
            [correctGuess, incorrectGuess] = quizTally(correctGuess, incorrectGuess, cardCount)
            finalScores, cardCount = play(initialHand, deck, cardCount)
            playerHands[f"Player {i+1}"] = finalScores
        
        # Summary
        print("  _________________________")
        print("||Summary:")
        print(f"||Dealer's hand: [{dealerHand[0]}, _]")
        for player in playerHands:
            print(f"||{player}: {playerHands[player]}")
        print("||")
        print("||")
        print("||_________________________")

        # Dealer plays
        print(f"\nDealer: \n{dealerHand}")
        cardCount += countCards([dealerHand[1]])
        [correctGuess, incorrectGuess] = quizTally(correctGuess, incorrectGuess, cardCount)
        [dealerSum], cardCount = play(dealerHand, deck, cardCount, False, True)
        print(f"\nDealer's Hand Value: \n{dealerSum}")

        # which players win?
        for player in playerHands:
            handsWon = 0
            for hands in playerHands[player]:
                if hands > dealerSum and hands < 22:
                    handsWon += 1
            if handsWon > 0:
                print(f"\n{player} wins {handsWon} hand{'s' if handsWon > 1 else ''}!")
            else:
                print(f"\n{player} was not a winner.")

        # Check deck to see if there are enough cards
        while True:
            cont = input("\nContinue playing? (Y/N) ")
            if cont == "Y":
                turn += 1
                while True:
                    samePlayers = input("Would you like to keep the same amount of players (changing player count reshuffles the deck)? (Y/N) ")
                    if samePlayers == "Y" or samePlayers == "N":
                        break
                    else:
                        print("Please enter either Y or N.")
                if len(deck) < 21 or samePlayers == "N":
                    if samePlayers == "N":
                        playerCount = definePlayerCount()
                    print("\nReshuffling...")
                    cardCount = 0
                    deck = generateDeck()
                break
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
