import random
import copy

from slotmachine.config import *

from slotmachine.symbols import (
    string_compare,
    string_has,
    strset_compare,
    strset_has,
)

class SlotSimulator:

    def __init__(self):
        self.total_winnings = 0
        self.bonus_total = 0

        self.slots = [
            [],
            [],
            [],
            [],
            []
        ]

        self.rares = [f"R{x}" for x in range(RARENUM)]
        self.epics = [f"E{x}" for x in range(EPICNUM)]
        self.uniques = [f"U{x}" for x in range(UNIQUENUM)]
        self.legends = [f"L{x}" for x in range(LEGENDNUM)]
        self.mystics = [f"M{x}" for x in range(MYSTICNUM)]

        random.seed()
        
    def reelcheck(self, symbol, reel):
        connect = False
        for cursymbol in range(REELHEIGHT):
            if string_compare(symbol, self.slots[reel][cursymbol]):
                connect = True
        return connect

    def spreadcheck(self, reel, symbol):
        if string_has('S', self.slots[reel][symbol]):
                    if reel != 0:
                        self.spreadingwild(reel-1,symbol)
                    if reel != REELS-1:
                        self.spreadingwild(reel+1,symbol)
                    if symbol != 0:
                        self.spreadingwild(reel,symbol-1)
                    if symbol != REELHEIGHT-1:
                        self.spreadingwild(reel,symbol+1)

    def spreadingwild(self, reel, symbol):
        if not string_has('W',self.slots[reel][symbol]):
            if not string_has('S',self.slots[reel][symbol]):
                if not string_has('R',self.slots[reel][symbol]):
                    if not string_has('P', self.slots[reel][symbol]):
                        if not self.slots[reel][symbol].islower():
                            tempsymbol = list(copy.copy(self.slots[reel][symbol]))
                            tempsymbol[1] = 'S'
                            self.slots[reel][symbol] = str(f"{tempsymbol[0]}{tempsymbol[1]}")
                            self.spreadcheck(reel, symbol)

    def spin(self, bonus = False, amount = 0, tier = 0):
        if bonus and not STREAMLINE:
            print(f"BONUS SPIN! {amount} REMAINING")
        # Reset reels
        for reel in self.slots:
            reel.clear()
        
        # Populate reels
        for reel in self.slots:
            scatterhit = False
            for _ in range(REELHEIGHT):
                if scatterhit:
                    pull = random.randint(1, 95)
                else:
                    pull = random.randint(1, 100)
                chance = random.randint(1,10)
                if pull <= RARETHRES:
                    rare = copy.copy(random.choice(self.rares))
                    reel.append(rare)
                elif pull <= EPICTHRES:
                    epic = copy.copy(random.choice(self.epics))
                    if chance <= ARMRATE:
                        epic = str.lower(epic)
                    if bonus and tier > 13:
                        reel.append("EW")
                    else:
                        reel.append(epic)
                elif pull <= UNIQUETHRES:
                    unique = copy.copy(random.choice(self.uniques))
                    if chance <= ARMRATE:
                        unique = str.lower(unique)
                    if bonus and tier > 8:
                        reel.append("UW")
                    else:
                        reel.append(unique)
                
                elif pull <= LEGENDTHRES:
                    legend = copy.copy(random.choice(self.legends))
                    if chance <= ARMRATE:
                        legend = str.lower(legend)
                    if bonus and tier > 4:
                        reel.append("LW")
                    else:
                        reel.append(legend)
                elif pull <= MYSTICTHRES:
                    mystic = copy.copy(random.choice(self.mystics))
                    if chance <= ARMRATE:
                        mystic = str.lower(mystic)
                    if bonus and tier > 1:
                        reel.append("MW")
                    else:
                        reel.append(mystic)
                elif pull <= WILDTHRES:
                    if chance <= SPREADRATE:
                        reel.append("WS")
                    else:
                        reel.append("WW")
                        
                else:
                    reel.append("PP")
                    scatterhit = True
                    
    ##    if VERBOSE:
    ##        for reel in slots:
    ##            print(f"reel{reel}")

        #Spreading wild check

        spreadhappening = False
        spreadtick = 0
        
        for curreel in range(REELS):
            for cursymbol in range(REELHEIGHT):
                if string_compare(self.slots[curreel][cursymbol], "WS", True):
                    self.spreadcheck(curreel,cursymbol)
                    spreadhappening = True
                    if bonus:
                        spreadtick += 1
                        

        for curreel in range(REELS):
            for cursymbol in range(REELHEIGHT):
                if string_has('S', self.slots[curreel][cursymbol]) and not string_compare(self.slots[curreel][cursymbol], "WS", True):
                    tempsymbol = list(copy.copy(self.slots[curreel][cursymbol]))
                    tempsymbol[1] = 'W'
                    self.slots[curreel][cursymbol] = str(f"{tempsymbol[0]}{tempsymbol[1]}")
                   
        if VERBOSE:
            for reel in self.slots:
                print(f"reel{reel}")
            

        




            
        # Determine winning combinations and calculate payout
        round_winnings = 0
        freespins = 0

        #First, we read the first reel for the symbols we want connecting
        consecutive_symbols = set()
        minreel = 0
        #If you had no wilds you'd only check the first 3 reels, but since we have wilds, we could have wilds up to the 4th
        #reel, and then random symbols. These must be accounted for
        for curreel in range(REELS):
            cur_symbols = []
            wildextend = False
            #Hence, here
            if curreel == minreel:
                for cursymbol in range(REELHEIGHT):
                    symbol = self.slots[curreel][cursymbol]
                    if 'W' in symbol: #If there's a wild, it will allow all connections to the next reel, so add to the set.
                        if VERBOSE and not wildextend:
                            print("Wild extend!")
                        wildextend = True
                    consecutive_symbols.add(str.upper(symbol))

            #If it's reel 2 or 3, we then compare and modify the list we made to hold what we've found continuing,
            #then make the consecutive symbols hold the new current symbols
            if curreel == 1 or curreel == 2:
                for connecting in consecutive_symbols:
                    purewild = False
                    if 'W' in connecting:
                        purewild = True
                    if strset_compare(connecting, self.slots[curreel], purewild):
                        cur_symbols.append(str.upper(connecting))
                consecutive_symbols = set(cur_symbols)
            if VERBOSE:
                print(f"{consecutive_symbols}")
            if len(consecutive_symbols) == 0:
                break
            if wildextend: minreel += 1

        #Good debug to see what the computer sees
        if VERBOSE:
            print("winning symbols:" , ''.join(consecutive_symbols))

    ##Now we need to pay out.
    ##It is important that it was a set, and not a list, since with a list we can have multiple of the same symbol.
    ##Therefore, we want a highlander rule. Every unique symbol only needs evaluation once. It's also important
    ##to go by symbol like this, since multiple symbols can pay at different lines, in different way count. Even
    ##more so with wilds


        #Scatter check
        scattercount = 0
        for curreel in range(REELS):
            for cursymbol in range(REELHEIGHT):
                symbol = self.slots[curreel][cursymbol]
                if string_has('P', symbol):
                    scattercount += 1

        if scattercount > 2:
            if bonus:
                freespins += 3 + (2 * (scattercount - 3))
                if VERBOSE:
                    print("RETRIGGER!")
            else:
                freespins += 10 + (3 * (scattercount - 3))
                if VERBOSE:
                    print("BONUS TRIGGERED!")

        scatter = copy.copy(consecutive_symbols)
        for symbol in consecutive_symbols:
            if 'P' in symbol:
                scatter.remove(symbol)
        consecutive_symbols = scatter


        #Wild lines must be paid and cleared!
        wildpay = 0
        
        if strset_has('W', consecutive_symbols):
            symbol = 'W'
            paylength = 0
            payways = 1
            mult = 0
            connecting = True
            purewild = False
            while connecting:
                for curreel in range(REELS):
                    if strset_has(symbol, self.slots[curreel]) and connecting == True:
                        paylength += 1
                        for cursymbol in range(REELHEIGHT):
                            if string_has(symbol, self.slots[curreel][cursymbol]):
                                mult += 1
                        payways = payways * mult
                        mult = 0
                    else:
                        connecting = False
                    if curreel == REELS - 1:
                        connecting = False
            if paylength == 5:
                if VERBOSE:
                    print(f"ways: {payways}")
                    print(f"length: {paylength}")
                payout = PAYOUTS[symbol[0]][paylength - 3] * payways
                if not STREAMLINE:
                    print(symbol + f" has paid out ${payout:.2f}")
                round_winnings += payout
                wildpay += payways
        nonwildlines = copy.copy(consecutive_symbols)
        for symbol in consecutive_symbols:
            if 'W' in symbol:
                nonwildlines.remove(symbol)
        consecutive_symbols = nonwildlines
            
            
        for symbol in consecutive_symbols:
            paylength = 0 #How far did the connection go?
            payways = 1 #How many ways are there?
            mult = 0
            connecting = True
            #While statement to kill the loop. No need to check further if we stopped connecting
            while connecting:
                for curreel in range(REELS):
                    if strset_compare(symbol, self.slots[curreel]) and connecting == True:
                        paylength += 1
                        for cursymbol in range(REELHEIGHT):
                            if string_compare(symbol, self.slots[curreel][cursymbol]):
                                mult += 1
                        payways = payways * mult
                        mult = 0
                    else:
                        connecting = False
                    if curreel == REELS - 1: #Should failsafe and always close off if full connection
                        connecting = False
            if VERBOSE:
                print(f"ways: {payways - wildpay}")
                print(f"length: {paylength}")
            payout = PAYOUTS[str.upper(symbol[0])][paylength - 3] * (payways - wildpay)
            if not STREAMLINE:
                print(symbol + f" has paid out ${payout:.2f}")
            round_winnings += payout

        
        if bonus:
            if tier < 2 and tier + spreadtick >= 2:
                if not STREAMLINE: print("MILITARY ARE OVERRRUN!")
                freespins += 3
            if tier < 5 and tier + spreadtick >= 5:
                if not STREAMLINE: print("SURVIVORS ARE OVERRRUN!")
                freespins += 2
            if tier < 9 and tier + spreadtick >= 9:
                if not STREAMLINE: print("GUESTS ARE OVERRRUN!")
                freespins += 1
            if tier < 14 and tier + spreadtick >= 14:
                if not STREAMLINE: print("EVERTHING IS OVERRUN!!!!")
                freespins += 1
            tier += spreadtick

        if not bonus and freespins == 0:    
            if not STREAMLINE:
                print(f"Spin {run + 1}: Winnings: ${round_winnings:.2f}")
        elif freespins != 0:
            self.spin(True, freespins + amount, tier)
        else:
            self.bonus_total += round_winnings
            if amount > 0:
                self.spin(True, amount - 1, tier)
            else:
                if not STREAMLINE:
                    print(f"YOU HAVE WON ${self.bonus_total:.2f}!!!!!!!!!!!!!!")
                self.bonus_total = 0
        self.total_winnings += round_winnings
