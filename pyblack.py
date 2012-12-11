# -*- coding: utf-8 -*-

from random import shuffle


class Card:
    '''
    This simple class manages single card objects.
    It has not any methods.
    '''
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

 
class Hand:
    '''
    This class manages hands that are lists of card object.
    It has some methods.
    '''
    
    def __init__(self):
        self.cards = [] #The hand is empty
        
    def __str__(self):
        suits = ['Picche', 'Cuori', 'Quadri', 'Fiori']
        ranks = ['Asso', 'Due', 'Tre', 'Quattro', 'Cinque',
                 'Sei', 'Sette', 'Otto', 'Nove', 'Dieci',
                 'Jack', 'Regina', 'Re']
        s = ''
        for card in self.cards:
            s += (' ' + ranks[card.rank - 1] + ' di '
                 + suits[card.suit - 1] + '\n')
        return s
    
    def IsAce(self):
        '''Check if is there at least one ace in the hand'''
        
        for card in self.cards:
            if card.rank == 1:
                return True
        else:
            return False
        
    def Add(self, card):
        '''Add a card at the END of the hand'''

        self.cards.append(card)

    def Reset(self):
        '''The hand return to be empty'''
        
        self.cards = []
            
    def Remove(self):
        '''Remove the FIRST card in the hand'''

        if self.cards == []: #If the hand is empty
            return False
        else:
            return self.cards.pop(0)
        
    def Value(self, ace):
        '''Return the value of the deck according to the ace'''
        
        self.value = 0 #The value of the hand is zero at beginning
        for card in self.cards: #For every card in the hand
            if card.rank > 10: #If it is a figure...
                self.value += 10 #...is value is 10
            elif card.rank == 1: #If it is an ace...
                if ace: #...according to the parameter...
                    self.value += 1 #...his value is 1...
                else:
                    self.value += 11 #...or 11
            else:
                self.value += card.rank #Else his value is the mark
        return self.value


class Deck(Hand):
    '''
    This class is inherited from Hand class.
    It manages decks that are like hands.
    It has only a method more.
    '''
    
    def __init__(self):
        self.cards = []
        for mark in range(1, 14): #for every marks
            for suit in range(1, 5): #for every suits
                self.Add(Card(mark, suit)) #Add a card to the deck
                
    def Shuffle(self, times):
        '''Shuffle the deck though it is empty'''
        
        for i in range(times):
            shuffle(self.cards)
        
        
class Player:
    '''
    This simple class manages player objects.
    It allow to have some simple thing with them,
    like bet or win money.
    '''
    
    def __init__(self, money):
        self.money = money
        self.hand = Hand() #Every player has a hand
        
    def Bet(self, bet):
        '''Return true if you can bet'''
        
        if bet > self.money: #If your money is not enough...
            return False #...you can't bet
        else:
            self.bet = bet
            return True
    
    def Win(self):
        '''Win your bet'''
        
        self.money += self.bet * 1.5
    
    def Lose(self):
        '''Lose your bet'''
        
        self.money -= self.bet
        
    def Take(self, deck, ncards):
        '''Add n cards to the hand taking them form the deck'''
        for i in range(ncards):
            self.hand.Add(deck.Remove())


class Dealer(Player):
    '''
    This class manages the dealer
    '''

    def __init__(self):
        self.hand = Hand() #Also the dealer has a hand
            
    def Play(self, deck):
        '''The dealer plays according to his rule'''
        
        while self.hand.Value(True) < 17:
            self.Take(deck, 1)
 
 
class View:
    '''
    This class manages the interface from
    the player to the game and vice versa
    '''

    def __init__(self, deck, player, dealer):
        self.deck = deck
        self.player = player
        self.dealer = dealer

    def AskBet(self):
        '''Return how much the player wants to bet'''
        
        bet = input('Quanto vuoi scommettere? ')
        while bet > self.player.money:
            print('Non hai abbastanza denaro!')
            bet = input('Quanto vuoi scommettere? ')
        return bet
        
    def DealerHand(self):
        
        '''Print the dealer's hand'''
        print('La mano del banco vale ' + 
              str(self.dealer.hand.Value(True)))
        print(self.dealer.hand)
        
    def PlayerHand(self):
        '''Print the player's hand'''
        
        if (self.player.hand.IsAce() and 
            self.player.hand.Value(False) <= 21):
            print('La tua mano vale ' + 
                  str(self.player.hand.Value(True)) + ' o '
                  + str(self.player.hand.Value(False)))
        else:
            print('La tua mano vale ' + 
                  str(self.player.hand.Value(True)))
        print(self.player.hand)

    def AskHitStand(self):
        '''Return true if the player wants hit'''
       
        while True:
            hitstand = raw_input('Vuoi chiedere Carta o ' + 
                                 'Stare("c" o "s")? ')
            if hitstand == 'c' or hitstand == 's':
                break
        if hitstand == 'c':
            return True
        else:
            return False
        
    def PlayerMoney(self):
        '''Print how much money you have'''
        
        print('Hai ' + str(self.player.money) + '$')
        
    def Win(self, string):
        '''Print your bet and your new money'''
        
        print(string)
        print('Hai vinto ' + str(self.player.bet * 1.5) +
              '$, quindi ora hai ' + str(self.player.money) + '$')
        
    def Lose(self, string):
        '''Print your bet and your new money'''
        
        print(string)
        print('Hai perso ' + str(self.player.bet) +
              '$, quindi ora hai ' + str(self.player.money) + '$')
        
    def PlayAgain(self):
        ''' '''
        
        while True:
            playagain = raw_input('Vuoi giocare ancora("s" o "n")? ')
            if playagain == 's' or playagain == 'n':
                break
        return playagain
 
    def Credits(self):
        '''Thank the player'''
        
        print('Grazie per aver giocato')
        print('Se hai riscontrato bug scrivi ' + 
              'pure ad andreaciceri96@gmail.com')
 
 
class Game:
    '''
    This class manages the rules of the game
    '''
    
    def __init__(self):
        self.deck = Deck() #Create the deck
        self.deck.Shuffle(10) #Shuffle the deck 10 times
        self.player = Player(100) #The player has 100$
        self.dealer = Dealer()
        self.view = View(self.deck, self.player, self.dealer)
        
    def Play(self):
        self.view.PlayerMoney()
        
        stillplay = True

        while stillplay: #For every game
            bet = self.view.AskBet()
            self.player.Bet(bet) #The player bets
            self.player.hand.Reset() #The player's hand is empty
            self.dealer.hand.Reset() #the dealer's hand is empty
            self.player.Take(self.deck, 2) #The player takes 2 cards
            self.dealer.Take(self.deck, 1) #The dealer takes 1 cards
            
            self.view.DealerHand() #Print the dealer's hand
            
            stillhit = True
            
            while stillhit: #Until the player hits
                self.view.PlayerHand() #Print the player's hand
                hit = self.view.AskHitStand() #Hit or stand?
                
                
                if hit:
                    self.player.Take(self.deck, 1)
                    
                    if self.player.hand.Value(True) == 21 or \
                        self.player.hand.Value(False) == 21:
                         #If the value's hand is 21(both ace's value)
                         
                        self.view.PlayerHand() #Print the player's hand
                        self.player.Win()
                        self.view.Win('Hai fatto Blakjack')
                        
                        stillhit = False
                    
                    elif self.player.hand.Value(True) > 21 and \
                        self.player.hand.Value(False) > 21:
                        #If the value's hand busts(both ace's value)
                        
                        self.view.PlayerHand() #Print the player's hand
                        self.player.Lose()
                        self.view.Lose('Hai sballato')
                        
                        stillhit = False
                    
                else:
                    self.dealer.Play(self.deck)
                    #According to the dealer's rule
                    
                    self.view.DealerHand()
                    
                    if self.dealer.hand.Value(True) == 21:
                        #If the value of dealer's hand is 21
                        
                        self.player.Lose()
                        self.view.Lose('Il banco ha fatto Blakjack')
                    
                    elif self.dealer.hand.Value(True) > 21:
                        #If the value of dealer's hand is more than 21

                        self.player.Win()
                        self.view.Win('Il banco ha sballato')
                        
                    elif self.dealer.hand.Value(True) > \
                        self.player.hand.Value(True) and \
                        self.dealer.hand.Value(True) > \
                        self.player.hand.Value(False):
                        #If the value of dealer's hand is more
                        #than the value of player's hand
                        
                        self.player.Lose()
                        self.view.Lose('Il banco ha fatto più di te')
                        
                    elif self.dealer.hand.Value(True) == \
                        self.player.hand.Value(True) and \
                        self.dealer.hand.Value(True) == \
                        self.player.hand.Value(False):
                        #If the value of dealer's hand and
                        #the value of player's hand are equal
                        
                        self.player.Lose()
                        self.view.Lose('Il banco ha fatto' +
                                       'esattamente come te')
                        
                    elif self.dealer.hand.Value(True) < \
                        self.player.hand.Value(True) or \
                        self.dealer.hand.Value(True) < \
                        self.player.hand.Value(False):
                        #If the value of dealer's hand is less
                        #than the value of player's hand
                        
                        self.player.Win()
                        self.view.Win('Il banco ha fatto meno di te')

                    stillhit = False
            
            playagain = self.view.PlayAgain()
            
            if playagain == 'n': #If the player don't want play again
                self.view.Credits()
                stillplay = False



if __name__ == "__main__":  
    game = Game()
    game.Play()
