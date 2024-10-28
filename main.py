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
#      Initialize a deck as a set
#      For loop from 1 to K
#           Add 1 number for every suit into the deck

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

def play(hand, deck, counter, split = False):
    originalHand = hand[:]
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
    

    while True:
        if len(hand) == 2 and hand[0] == hand[1] and split == False:
            playerAction = input("Would you like to hit(H), stand(S), or split(SP)?\n")
        else:
            playerAction = input("Would you like to hit(H) or stand(S)?\n")
        
        if playerAction in ["H", "S"]:
            break
        if playerAction == "SP" and split == False:
            break
        else:
            print("Invalid Action.")
    
    match playerAction:
        case "H":
            newCard = deck.pop()
            counter += countCards([newCard])
            print(newCard)
            hand += convertHand([newCard])
            return play(hand, deck, counter)
        case "S":
            print(sum(hand))
            return [sum(hand)]
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
            
          
# Main Program()

#      Set player count = 0
#      Set game in progress = false
#      Set card count = 0
def main():
    playerCount = 0
    gameInProgress = False
    cardCount = 0
    deck = set()

    #      Print a message to greet the user
    #      Print rules and restraints of the blackjack program
    print("Welcome to this simulated blackjack where you can practice card counting")
    print("Due to constraints, players cannot double down and can only split a maximum of once per hand!")
    print("There can also only be a maximum of 3 players at the table.")
    #      User Input of player count
    while True:
        try:
            playerCount = int(input("Please enter the amount of players at the table: "))
        except ValueError:
            # playerCount = int(input("Please a valid number."))
            print("Please a valid number.")
        else:
            break

    if playerCount == 0:
        print("I cannot start a game of blackjack without any players.")
    #      User Input of confirmation to start the game (sets game in progress to true)
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
    #      Generate deck
    deck = generateDeck()
    #      Loop while the game in progress is true
    while gameInProgress:
        #           Set dealer hand to two popped values from the deck
        dealerHand = [deck.pop(), deck.pop()]
        cardCount += countCards(dealerHand[0])
        print(f"Dealer's hand: {dealerHand[0]}, _")
        playerHands = {}
        for i in range(playerCount):
            initialHand = [deck.pop(), deck.pop()]
            cardCount += countCards(initialHand)
            print(f"Player {i+1}'s hand: \n", initialHand)
            finalScores = play(initialHand, deck, cardCount)
            playerHands[f"Player {i+1}"] = finalScores
        # summary
        print("  _________________________")
        print("||Summary:")
        print(f"||Dealer's hand: [{dealerHand[0]}, _]")
        for player in playerHands:
            print(f"||{player}: {playerHands[player]}")
        print("||")
        print("||")
        print("||")
        print("||_________________________")
        # Dealer plays
        # which players win?
        # Check deck to see if there are enough cards
        while True:
            cont = input(print("Continue playing? (Y/N)"))
            if cont == "Y":
                break
            elif cont == "N":
                break
            else:
                print("Please enter either Y or N.")
        print(playerHands)
        gameInProgress = False

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
print("Thank you for playing blackjack simulation.")
