'''
Poker Game Winner Hand

Designed and Implemented by Göktuğ İnal.

Universitat Politecnica de Valencia
22.07.2021
GI
'''

import random
import time

def chooseTheBestHand(handOne, handTwo):
    '''
        It's called each time to compare fiveCards(table) and twoCards(hand) with ranking value(0...8) and card pairs in case of draw.
    '''

    if (handOne[5] != handTwo[5]):    # check 5th slot of array in order to determine ranking of the hand
        if ((handOne[5] > handTwo[5]) == True):
            return True # handOne is better
        else:
            return False
    if (handOne[5] == 4 or handOne[5] == 8): # if hand is Straight or Straight Flush
        if (handOne[2] != handTwo[2]):
            if ((handOne[2] > handTwo[2]) == True):
                return True
            else:
                return False
        else:
            return None
    if (handOne[5]==0 or handOne[5]==5): # Flush or High Card so, should check all cards to determine the best hand
        for i in range(5):
            if (handOne[4 - i] != handTwo[4 - i]): 
                if ((handOne[4 - i] > handTwo[4 - i]) == True):
                    return True
                else:
                    return False
        return None # draw or chop - In the poker world, to chop something means to split it among two or more players

    for j in range(6,10):   # One pair, Two Pair, Three of a kind, Four of a Kind and Full House control loop. Big card number wins
        if (handOne[j] != handTwo[j]):
            if ((handOne[j] > handTwo[j]) == True): 
                return True
            else:
                return False
        # Control point just in case that never provides handOne[j] != handTwo[j] condition above
        if (len(handOne) == j+1):
            return None # draw or chop - In the poker world, to chop something means to split it among two or more players

def cardCombination(sevenC, sevenFS): 
    '''
        seven cards and seven french suits combiantions to calculate the best hand for each player.
    '''

    bestHand = None
    for i in range(7):
        for j in range(i+1, 7):
            pack = []
            for next in range(7):
                if (next != i and next != j): 
                    pack.extend([sevenC[next], sevenFS[next]])
            sortedCards = sorted([pack[0],pack[2],pack[4],pack[6],pack[8]]) # sort 2,3,4.. Q(<),K(=),A(>) in order to rank
            fSuits = [pack[1],pack[3],pack[5],pack[7],pack[9]] # clubs (♣), diamonds (♦), hearts (♥), and spades (♠)
            hotHand = rankStud(sortedCards, fSuits) # rank the hand by sending five cards as a parameter
            if ((bestHand is None) or chooseTheBestHand(hotHand, bestHand)): 
                bestHand = hotHand
    return bestHand

def rankStud(card, suit):
    '''
        Ranking -worst to best

        High Hand - 0
        One Pair - 1
        Two Pair - 2 
        Three of a Kind - 3
        Straight - 4
        Flush - 5
        Full House - 6
        Four of a Kind - 7
        Straight Flush - 8    

        Card Array = [Sorted cards, ranking value(0...8), card pairs check in case of draw]
    '''
    if (suit.count(suit[0])==len(suit)):  # Check Straight Flush by controlling suits whether they are all same or not
        if ((card[0]==card[1]-1==card[2]-2==card[3]-3) and (card[4]-1==card[3] or card[4]-12==card[0])): # Ace check!
            card.append(8) # Straight Flush
        else:
            card.append(5) # Flush
    elif ((card[0] == card[1]-1 == card[2]-2 == card[3]-3) and (card[4]-1 == card[3] or card[4]-12 == card[0])): 
        card.append(4) # Straight
    elif (card[1]==card[2]==card[3] and (card[0]==card[1] or card[3]==card[4])):    # Four of a kind
        if (card[0]==card[1]):
            card.extend([7, card[3], card[4]])
        else:   # card[3]==card[4]
            card.extend([7, card[4], card[0]]) 
    elif (card[0]==card[1]==card[2] and card[3]==card[4]):  # Full House 
        card.extend([6, card[2], card[4]]) 
    elif (card[0] == card[1] and card[2] == card[3] == card[4]):
        card.extend([6, card[4], card[1]]) 
    elif (card[0]==card[1]==card[2]): 
        card.extend([3, card[2], card[4], card[3]]) # Three of a kind - [3, (one of pairs, and thre rest two cards)]
    elif (card[1]==card[2]==card[3]): 
        card.extend([3, card[3], card[4], card[0]]) 
    elif (card[2]==card[3]==card[4]): 
        card.extend([3, card[4], card[1], card[0]]) 
    elif ((card[0]==card[1] and (card[2]==card[3] or card[3]==card[4])) or (card[1]==card[2] and card[3]==card[4])):  # Two Pair - [2, (one of 1st pair, one of 2nd pair, and irrelevent card)]    
        if (card[0]==card[1] and card[2]==card[3]): 
            card.extend([2, card[3], card[1], card[4]])
        else: 
            if (card[0]==card[1] and card[3]==card[4]):
                card.extend([2, card[4], card[1], card[2]])
            else:   # card[1]==card[2] and card[3]==card[4]
                card.extend([2,card[4],card[1],card[0]])
    elif (card[0]==card[1] or card[1]==card[2]):  # One Pair - [1, (one of pairs, and the other three cards)]
        if (card[0]==card[1]):
            card.extend([1, card[1], card[4], card[3], card[2]])
        else:   # card[1]==card[2]
            card.extend([1, card[2], card[4], card[3], card[0]])
    elif (card[2]==card[3] or card[3]==card[4]):
        if (card[2]==card[3]):
            card.extend([1, card[3], card[4], card[1], card[0]])
        else:   # card[3]==card[4]
            card.extend([1, card[4], card[2], card[1], card[0]])
 
    # If array size(card) is less than 5, then the hand's rank is High Card which is 0. Thus, 0 is added to end of the array.  
    # Otherwise, just return the card.

    if (len(card) > 5):
        return card
    else:
        return card + [0]

def bestHandAmongPlayers(bunch):
    '''
        Return the index of winner hand; bunch is an array which holds players.
    '''

    whoIsTheBest = 0
    bouquet = []
    for flag in range(1, len(bunch)):
        whoWins = chooseTheBestHand(bunch[flag], bunch[whoIsTheBest]) # Player2 x Player1
        if (whoWins is None): 
            bouquet.append(flag)
        if (whoWins == True):
            bouquet = []
            whoIsTheBest = flag

    return (whoIsTheBest, bouquet)

def whichIsTheWinnerHand(fiveC, twoC, onTable):
    '''
        Convert T, J, Q, K and A to ASCII in order to be able to compare and sort. 
        
        N    ASCII    N      ASCII    N      ASCII
        2     50      7       55      <       60
        3     51      8       56      =       61
        4     52      9       57      >       62
        5     53      :       58
        6     54      ;       59
    '''

    cards = onTable.replace("T", ":").replace("J", ";").replace("Q", "<").replace("K", "=").replace("A", ">")
    deckOfCards = (",".join(str(ord(i)) for i in cards)).split(',')
    letter = []
    for j in deckOfCards:
        letter.append(int(j))

    combFiveStud = []
    sizeCards = len(onTable)

    # For example; 5s9hAhKc3s, cards on the table.. 10 characters, that is why I make loop start at 10(onset) till end of the cards.

    onset = 10
    while sizeCards > onset:
        combFiveStud.append(cardCombination([letter[0], letter[2], letter[4], letter[6], letter[8], letter[onset+1], letter[onset+3]], [letter[1], letter[3], letter[5], letter[7], letter[9], letter[onset+2], letter[onset+4]]))
        onset = onset + 5  # also count blank (4+1) - For example; 5s9hAhKc3s 3s9c 8s7s - letter[15+1] -> 8 so on...

    print('\n%s players are on the table right now!\n' % len(combFiveStud))

    print("Who is gonna win?? Coming soon... :)")
    time.sleep(3.5)
    input("\nPress enter to see lucky one!\n")

    result = bestHandAmongPlayers(combFiveStud) # Each players have their own best hand and let's see who is the winner

    printWinner(result[0], result[1], combFiveStud, fiveC ,twoC)    # result[0]: index of winner, result[1]: index of players who have drawn

def initRandomDistribution():
    '''
        The order of the cards, from highest to lowest, is: deuce, three, four, five, six, seven, eight, nine, ten (T), jack (j), queen (Q), king (K) and ace (A).
        Today's 52-card deck preserves the four original French suits of centuries ago: clubs (♣), diamonds (♦), hearts (♥), and spades (♠).
    '''
    
    orderofCards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"] # 13
    frenchSuits = ["c", "d", "h", "s"] # 4

    # Random distribution of five cards to the table.

    def randomFiveCards(hand):
        randomCards = orderofCards[random.randrange(0, 13)] + frenchSuits[random.randrange(0, 4)]
        # Check if already in hand
        while randomCards in hand:
            randomCards = orderofCards[random.randrange(0, 13)] + frenchSuits[random.randrange(0, 4)]
        return randomCards
    
    # Random distribution of two cards to the player's hand.
    
    def randomTwoCards(hand):
        return randomFiveCards(hand) + randomFiveCards(hand)

    randomHand = ''
    for i in range(5): 
        randomHand = randomHand + randomFiveCards(randomHand) # five random cards on the table.
    table = randomHand
    numPlayers = random.randrange(2, 9) # determine number of players randomly (2-9).

    # Two cards randomly chosen as the number of players.

    twoCards = []

    for j in range(numPlayers):
        randomHand = randomHand + " "
        fresh = randomTwoCards(randomHand)
        randomHand = randomHand + fresh 
        twoCards.append(fresh)

    return (table, twoCards, randomHand)

def printWinner(winner, bouquet, combFiveStud, fiveC ,twoC):
    '''
        Print Winner Hand.
    '''

    handRankingCategories = ["a high card", "one pair", "two pair", "three of a kind", "a straight", "flush", "full house", "four of a kind", "a straight flush"]
    ranks = ["highCard", "1-pair", "2-pair", "3ofaKind", "straight", "flush", "fullHouse", "4ofaKind", "straightflush"]
   
    if len(bouquet) > 0:    # check if they have drawn
        bNo = [b+1 for b in bouquet]
        print("*********************************************")
        print("Ups! No winner. These players have drawn: " + str(winner+1) + ", " + ", ".join(str(x) for x in bNo) + " with " + handRankingCategories[combFiveStud[winner][5]])
        print("*********************************************\n")
    else: 
        print("*********************************************")
        print('Player %s wins the round with ' % str(winner+1) + handRankingCategories[combFiveStud[winner][5]])
        print("*********************************************\n")

    for i in range(len(combFiveStud)):  # loop for every player
        val = combFiveStud[i]
        for j in range(len(val)): 
            if (j != 5):    # first 5 value - turn back to real value from ASCII
                val[j] -= 48 
            else:
                val[j] += 41   # 41 is just random value, then values are converted to string which shows card ranking
                
        newVal =[val[k] for k in range(6)]
        print(" Player " + str(i+1) + ": " + twoC[i] + " | " + " cards on the table: " + fiveC[0] + fiveC[1] + fiveC[2] + fiveC[3] + fiveC[4] + fiveC[5] + fiveC[6] + fiveC[7] + fiveC[8] + \
        " ---> best hand combination: " + " ".join(str(x) for x in newVal).replace("41",ranks[0]).replace("42",ranks[1]).replace("43",ranks[2]).replace("44",ranks[3]).replace("45",ranks[4])\
        .replace("46",ranks[5]).replace("47",ranks[6]).replace("48",ranks[7]).replace("49",ranks[8]).replace("10","T").replace("11","J").replace("12","Q").replace("13","K").replace("14","A"))

def main(rnd):
    '''
        Main Function - The program starts right here. 
        Calling the required function(initRandomDistribution()) for card distribution.
    '''

    fiveCards, twoCards, allCardsOnTheTable = initRandomDistribution()  # distribute cards randomly 
        
    print("\n")
    print("Poker Game - Round %s\n" % rnd)
    print("Hand(table - players): " + allCardsOnTheTable)
    print("-------------------------------------------------------------------")
    whichIsTheWinnerHand(fiveCards, twoCards, allCardsOnTheTable)

# To launch the game
round = 0
print("\nWelcome to the poker game!")
while(True):
    key = input("\nPress 'Enter' to continue poker game or press any other key and then 'Enter' to exit...")

    if(key == ""):
        round = round + 1
        main(round) # let's play
    else:
        print("\nEnd of the poker game\n")
        break