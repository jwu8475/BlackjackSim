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
    randomInt = random.randint(1,5)
    if randomInt == 5:
        while True:
            try:
                answer = int(input("Current Count: "))
            except ValueError:
                print("Please enter a number.")
            else:
                print(f"Counter: {counter}")
                if answer == counter:
                    print("You are correct!")

                else:
                    print(f"Incorrect. Current Count: {counter}")
                return answer == counter

#      Generate a random number from 1-5
#      If the random number is 5 (20%)
#           Ask the user to input the current count
#           If correct
#               Return and inform the user it is correct
#           Else
#               Input: Ask user if they want to try again
#               If yes
#                     Ask the user to input the current count again
#               If no
#                     Show user the current count

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

    print("Current hand: ", handVal)

    # check for >= 21
    if handVal >= 21:
        if handVal == 21:
            print("21!")
        else:
            print("Busted!")
        return [handVal]
    
    while dealer == True:
        if handVal < 17:
            action = "H"
        else:
            action = "S"
        break

    while dealer == False:
        if len(hand) == 2 and hand[0] == hand[1] and split == False:
            action = input("Would you like to hit(H), stand(S), or split(SP)?\n")
        else:
            action = input("Would you like to hit(H) or stand(S)?\n")
        
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
            print(newCard)
            hand += convertHand([newCard])
            if dealer == True:
                return play(hand, deck, counter, False, True)
            return play(hand, deck, counter)
        case "S":
            print(handVal)
            return [handVal]
        case "SP":
            print("First Hand: ")
            newCard = deck.pop()
            counter += countCards([newCard])
            print([originalHand[0], newCard])
            firstHand = play([originalHand[0], newCard], deck, counter, True)

            print("Second Hand: ")
            newCard = deck.pop()
            counter += countCards([newCard])
            print([originalHand[1], newCard])
            secondHand = play([originalHand[1], newCard], deck, counter, True)

            return firstHand + secondHand
            
def definePlayerCount():
    players = 0
    while True:
        try:
            players = int(input("Please enter the amount of players at the table: "))
        except ValueError:
            # playerCount = int(input("Please a valid number."))
            print("Please a valid number.")
        else:
            break
    return players
# Main Program()

# Set player count = 0
# Set game in progress = false
# Set card count = 0
def main():

    round = 1
    playerCount = 0
    gameInProgress = False
    cardCount = 0
    deck = generateDeck()
    playerCount = definePlayerCount()
    correctGuess = 0
    incorrectGuess = 0

    # Print a message to greet the user
    # Print rules and restraints of the blackjack program
    print("Welcome to this simulated blackjack where you can practice card counting")
    print("Due to constraints, players cannot double down and can only split a maximum of once per hand!")
    print("There can also only be a maximum of 3 players at the table.")

    if playerCount == 0:
        print("I cannot start a game of blackjack without any players.")
    # User Input of confirmation to start the game (sets game in progress to true)
    elif playerCount > 3:
        print("I cannot start a game of blackjack with more than 3 players.")
    else:
        print(f"I have confirmed that there will be {playerCount} player{'s' if playerCount > 1 else ''} in the game.")

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
        print(f"Round {round}")
        dealerHand = [deck.pop(), deck.pop()]
        cardCount += countCards([dealerHand[0]])
        print(f"Dealer's hand: {dealerHand[0]}, _")
        playerHands = {}
        for i in range(playerCount):
            initialHand = [deck.pop(), deck.pop()]
            cardCount += countCards(initialHand)
            print(f"Player {i+1}'s hand: \n", initialHand)
            finalScores = play(initialHand, deck, cardCount)
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
        print("Dealer:\n", f"{dealerHand}")
        cardCount += countCards([dealerHand[1]])
        dealerSum = play(dealerHand, deck, cardCount, False, True)
        print("Dealer's Hand Value: \n", dealerSum)

        # which players win?
        for player in playerHands:
            handsWon = 0
            for hands in player:
                if player[hands] > dealerHand and player[hands] < 22:
                    handsWon += 1
            if handsWon > 0:
                print(f"{playerHands[player]} wins {handsWon} hand{'s' if handsWon > 1 else ''}!")
            else:
                print(f"{playerHands[player]} was not a winner.")

        # Check deck to see if there are enough cards
        while True:
            cont = input(print("Continue playing? (Y/N)"))
            if cont == "Y":
                while True:
                    samePlayers = input(print("Would you like to keep the same amount of players (changing player count reshuffles the deck)? (Y/N)"))
                    if samePlayers == "Y" or samePlayers == "N":
                        break
                    else:
                        print("Please enter either Y or N.")
                if len(deck) < 21 or samePlayers == "N":
                    if samePlayers == "N":
                        playerCount = definePlayerCount()
                    print("Reshuffling.")
                    cardCount = 0
                    deck = generateDeck()
                break
            elif cont == "N":
                gameInProgress = False
                print("Thank you for playing blackjack simulation.")
                break
            else:
                print("Please enter either Y or N.")

main()
#               20% chance of a random quiz function being called
#           Check if there are enough cards in the deck to play again
#               If there are only 40% of the deck remaining
#                     Call generate deck function for a new deck
#                     Reset card count
#                     Print a statement informing the user the deck is being reshuffled
#               Else
#                     Ask the user if they would like to continue to play
#                     If the user wants to stop
#                          Set game in progress to false
#                     If the user wants to continue
#                          If a new player is joining
#                               Reshuffle deck
#                               Reset card count
#                     If the user simply wants to play again with the current players
#                          Reset the dealer's hand
#                          Reset all player’s hands
#      Print statement thanking the user for playing
# print("Thank you for playing blackjack simulation.")
