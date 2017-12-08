import random
import copy
import numpy


class Card(object):
    """Defines a card object for the two-handed hearts game"""

    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
              "jack": 11, "queen": 12, "king": 13, "ace": 14, }
    suits = ["spades", "hearts", "diamonds", "clubs"]
    value_items = list(dict.keys(values))

    def __init__(self, value="", suit=""):

        if value not in self.values and value != "":
            print("Not a valid value.")
        if suit not in self.suits and suit != "":
            print("Not a valid suit.")
        else:
            if value == "":
                self.value = random.choice(self.value_items)
            if suit == "":
                self.suit = random.choice(self.suits)

            else:
                self.value = value
                self.suit = suit

    def __repr__(self):
        """Defines the representation of a card"""
        return "%s of %s" % (self.value, self.suit)

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def random_card(self):
        """Replaces the card object with a random card"""
        rand_value = random.randint(0, len(self.values) - 1)
        rand_suit = random.randint(0, len(self.suits) - 1)

        self.value = self.value_items[rand_value]
        self.suit = self.suits[rand_suit]

    def card_sort(self, sort_card):
        """Determines the higher of two cards for sorting purposes"""
        if self.suit == sort_card.suit:
            if self.values[self.value] < sort_card.values[sort_card.value]:
                return True
            else:
                return False
        else:
            if list.index(self.suits, self.suit) < list.index(sort_card.suits, sort_card.suit):
                return True
            else:
                return False

    def hearts_compare(self, compare_card):
        """Compares two cards for determining the winning card in a trick"""
        if self.suit == compare_card.suit:
            if self.values[self.value] > compare_card.values[compare_card.value]:
                return True
            else:
                return False
        else:
            return False

    def cards_below(self):
        """Returns all cards in a suit ranked below the card"""
        cards_to_return = []

        for keys in self.value_items:
            cards_to_return.append(Card(keys, self.suit))
        cards_to_remove = []

        for cards in cards_to_return:
            if cards.hearts_compare(self):
                cards_to_remove.append(cards)
        cards_to_return = [i for i in cards_to_return if i not in cards_to_remove]
        cards_to_return.remove(self)
        return cards_to_return

    def cards_above(self):
        """Returns all cards in a suit ranked above the card"""
        cards_to_return = []

        for keys in self.value_items:
            cards_to_return.append(Card(keys, self.suit))
        cards_to_remove = []

        for cards in cards_to_return:
            if not cards.hearts_compare(self):
                cards_to_remove.append(cards)
        cards_to_return = [i for i in cards_to_return if i not in cards_to_remove]
        return cards_to_return

class Deck(Card):
    """Defines a deck object for the two-handed hearts game"""

    def __init__(self):
        """Defines a deck as a list of card objects and defines an order and contents of a deck"""
        card_list = []
        suit_index = 0
        for suit in self.suits:
            value_index = 0
            for value in self.value_items:
                card_list.append(Card(value, suit))
                value_index += 1
            suit_index += 1

        self.contents = card_list
        self.order = card_list

    def __repr__(self):
        """Defines a string representation of a deck"""
        deck_string = [str(card) for card in self.order]

        return "\n".join(deck_string)

    def __eq__(self, other):
        """Defines equality amongst decks"""
        return self.contents == other.contents and self.order == other.order

    def shuffle(self):
        """Randomly shuffles the order of a deck"""
        new_deck = []
        for i in range(len(self.order)):
            card_choice = random.choice(self.order)
            self.order.remove(card_choice)
            new_deck.append(card_choice)

        self.order = new_deck

    def sort_deck(self):
        """Robust sorting for a deck of arbitrary size"""
        full_deck = Deck()
        sort_values = []
        new_order = []
        for i in range(len(self.order)):
            order_card = self.order[i]

            sort_value = list.index(full_deck.contents, order_card)
            sort_values.append(sort_value)
        sort_values.sort()

        for value_indexes in sort_values:
            new_order.append(full_deck.contents[value_indexes])
        self.order = new_order

    def arrange_contents(self):
        """Keeps contents in order while maintaining order"""
        full_deck = Deck()
        sort_values = []
        new_order = []
        for i in range(len(self.order)):
            order_card = self.order[i]

            sort_value = list.index(full_deck.contents, order_card)
            sort_values.append(sort_value)
        sort_values.sort()

        for value_indexes in sort_values:
            new_order.append(full_deck.contents[value_indexes])
        self.contents = new_order


class Hand(Deck):
    """Defines a hand for the two-handed hearts game"""

    def __init__(self, deck, size=13):
        """Initiates a hand of default size 13 by removing cards from the deck"""

        self.order = deck.order[0:size]
        self.contents = deck.order[0:size]
        self.arrange_contents()

        deck.order = deck.order[size:]
        deck.contents = deck.order
        deck.arrange_contents()

    def __repr__(self):
        """Defines a representation of a hand"""
        hand_string = [str(card) for card in self.contents]

        return "\n".join(hand_string)

    def add_card(self, card):
        """Adds a card to the hand"""
        self.order.append(card)
        self.contents.append(card)
        self.arrange_contents()

    def remove_card(self, card):
        """Removes a card from the hand"""
        self.order.remove(card)
        self.contents.remove(card)

    def has_suit(self, suit):
        """Indicates whether the player has a suit"""
        for cards in self.contents:
            if suit == cards.suit:
                return True
        return False

    def select_suit(self, suit):
        """Selects all cards of a particular suit"""
        selected_cards = []
        for cards in self.contents:
            if suit == cards.suit:
                selected_cards.append(cards)
        return selected_cards

    def select_anti_suit(self, suit):
        """Selects all cards not in a particular suit"""
        selected_cards = []
        for cards in self.contents:
            if suit != cards.suit:
                selected_cards.append(cards)
        return selected_cards

    def select_no_points(self):
        """Select all cards in the hand that aren't worth any points"""
        selected_cards = []
        queen_of_spades = Card("queen", "spades")
        for cards in self.contents:
            if cards.suit != "hearts" and cards != queen_of_spades:
                selected_cards.append(cards)
        return selected_cards

    def one_suit(self):
        """Determines if a hand is composed of a single suit"""
        first_suit = self.order[0].suit
        for cards in self.order[1:]:
            if cards.suit != first_suit:
                return False
        return True

    def legal_moves(self, trick, trick_num, hearts_broken):
        """Determines a set of legal cards to play given a trick and a trick number"""
        legal_cards = []
        if trick_num == 0:
            if trick == []:
                if Card("2", "clubs") in self.contents:
                    legal_cards.append(Card("2", "clubs"))
            else:
                if self.has_suit("clubs"):
                    legal_cards.extend(self.select_suit("clubs"))
                else:
                    legal_cards.extend(self.select_no_points())
                    if legal_cards == []:
                        legal_cards = self.contents
        else:
            if trick == []:
                if not hearts_broken:
                    legal_cards.extend(self.select_anti_suit("hearts"))
                    if legal_cards == []:
                        legal_cards = self.contents
                else:
                    legal_cards = self.contents
            else:
                trick_suit = trick[0].suit
                if self.has_suit(trick_suit):
                    legal_cards.extend(self.select_suit(trick_suit))
                else:
                    legal_cards = self.contents

        return legal_cards

class Player(object):
    """Defines a player in a hearts game. Random Performance: Approaches 78 ppg with a variance approaching 26 ppg.
    """

    ai_options = ["human", "random", "program"]

    def __init__(self, name, hand, ai):
        """Initiates a player with a hand and an AI"""
        self.name = name
        self.hand = hand
        self.won_cards = []
        self.score = 0
        self.trials = 0
        self.knowledge = {"held by any": [], "held by left": [], "held by across": [], "held by right": [],
                          "held by left or across": [], "held by left or right": [], "held by across or right": [],
                          "left no spades": False, "across no spades": False, "right no spades": False,
                          "left no hearts": False, "across no hearts": False, "right no hearts": False,
                          "left no diamonds": False, "across no diamonds": False, "right no diamonds": False,
                          "left no clubs": False, "across no clubs": False, "right no clubs": False, "only points": ""}

        # {"my score": 0, "left score": 0, "across score": 0, "right score": 0,
        #               "pass direction": "", "passed by me": [], "passed to me": [], "played by all": [],
        #               "played by left": [], "played by across": [], "played by right": [],
        #               "left has queen": False, "across has queen": False, "right has queen": False,
        #               "no spades": False, "left no spades": False, "across no spades": False,
        #               "right no spades": False,
        #               "no hearts": False, "left no hearts": False, "across no hearts": False,
        #               "right no hearts": False,
        #               "no diamonds": False, "left no diamonds": False, "across no diamonds": False,
        #               "right no diamonds": False,
        #               "no clubs": False, "left no clubs": False, "across no clubs": False,
        #               "right no clubs": False,
        #               "all points": False, "left all points": False, "across all points": False,
        #               "right all points": False,
        #               "took queen": False, "left took queen": False, "across took queen": False,
        #               "right took queen": False,
        #               "my points": 0, "left points": 0, "across points": 0,
        #               "right points": 0,
        #               "spades count": 0, "hearts count": 0, "diamonds count": 0, "clubs count": 0,
        #               "spades below": 0, "spades above": 0, "hearts below": 0, "hearts above": 0,
        #               "diamonds below": 0, "diamonds above": 0, "clubs below": 0, "clubs above": 0,
        #               "points remaining": 26, "winning": 0, "left winning": 0, "across winning": 0,
        #               "right winning": 0}

        if ai in self.ai_options:
            self.ai = ai
        else:
            print("Not a valid input")

    def __repr__(self):
        """Defines a representation of a player"""
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.hand == other.hand and self.won_cards == other.won_cards and \
               self.score == other.score and self.knowledge == other.knowledge and self.ai == other.ai and \
               self.trials == other.trials

    def choose_pass(self):
        """Picks three cards to pass"""
        hand = self.hand
        pass_list = []
        if self.ai == "random":
            for i in range(3):
                card_choice = random.choice(hand.order)
                hand.remove_card(card_choice)
                pass_list.append(card_choice)
            self.hand = hand
            return pass_list
        elif self.ai == "program":
            pass
        elif self.ai == "human":
            print(hand)
            print(self.name)
            for i in range(3):
                choice_str = str(input("Choose a card from your hand to pass: "))
                card_value = ""
                card_suit = ""
                for value in hand.value_items:
                    if value in choice_str:
                        card_value = value
                for suit in hand.suits:
                    if suit in choice_str:
                        card_suit = suit
                if card_value == "" or card_suit == "":
                    print("Not a valid input - try again")
                    return self.choose_pass()

                card_choice = Card(card_value, card_suit)
                pass_list.append(card_choice)
            for choices in pass_list:
                hand.remove_card(choices)
            self.hand = hand
            return pass_list

    def choose_play(self, hround):
        """Picks a card to play"""
        trick = hround.trick
        trick_num = hround.trick_num
        hearts_broken = hround.hearts_broken

        if self.ai == "random":
            card_choice = random.choice(self.hand.legal_moves(trick, trick_num, hearts_broken))
            return card_choice
        elif self.ai == "program":
            pass
        elif self.ai == "human":
            card_value = ""
            card_suit = ""
            while card_value == "" or card_suit == "":
                print(self.hand)
                print(self.name)
                choice_str = str(input("Choose a card from your hand to play: "))
                card_value = ""
                card_suit = ""
                for value in self.hand.value_items:
                    if value in choice_str:
                        card_value = value
                for suit in self.hand.suits:
                    if suit in choice_str:
                        card_suit = suit
                if card_value == "" or card_suit == "":
                    print("Not a valid input - try again")

            card_choice = Card(card_value, card_suit)
            return card_choice

    def play_card(self, card):
        """Compels a player to play a particular card"""
        if card in self.hand.contents:
            self.hand.remove_card(card)
            return card
        else:
            print("Card is not in hand")

    def has_suit(self, suit):
        """Indicates whether the player has a suit"""
        for cards in self.hand.order:
            if suit == cards.suit:
                return True
        return False

    def count_suit(self, suit):
        """Counts the number of cards of a suit in a players hand"""
        count = 0
        for cards in self.hand.order:
            if suit == cards.suit:
                count += 1
        return count

    def has_start(self, start_card=Card("2", "clubs")):
        """Indicates with the player has the starting card"""
        for cards in self.hand.order:
            if cards.suit == start_card.suit and cards.value == start_card.value:
                return True
        return False

class HeartsRound(object):
    """Plays a round of hearts"""

    pass_options = ["left", "right", "across", "none"]

    standard_deck = Deck()

    def __init__(self, player1, player2, player3, player4, pass_dir):
        """Initiates a games of hearts with 4 players"""
        new_deck = Deck()
        new_deck.shuffle()
        player1.hand = Hand(new_deck)
        player2.hand = Hand(new_deck)
        player3.hand = Hand(new_deck)
        player4.hand = Hand(new_deck)
        player1.won_cards = []
        player2.won_cards = []
        player3.won_cards = []
        player4.won_cards = []

        self.players = [player1, player2, player3, player4]
        for player in self.players:
            for card in self.standard_deck.contents:
                if card not in player.hand.contents:
                    list.append(player.knowledge["held by any"], card)
            if player.hand.one_suit():
                single_suit = player.hand.contents[0].suit
                if pass_dir == "none":
                    player.knowledge["left no " + single_suit] = True
                    player.knowledge["across no " + single_suit] = True
                    player.knowledge["right no " + single_suit] = True
                elif pass_dir == "left":
                    player.knowledge["across no " + single_suit] = True
                    player.knowledge["right no " + single_suit] = True
                elif pass_dir == "across":
                    player.knowledge["left no " + single_suit] = True
                    player.knowledge["right no " + single_suit] = True
                else:
                    player.knowledge["left no " + single_suit] = True
                    player.knowledge["across no " + single_suit] = True

        self.played_players = {player1.name: [], player2.name: [], player3.name: [], player4.name: []}
        self.played_all = []
        self.passed_players = {player1.name: [], player2.name: [], player3.name: [], player4.name: []}
        self.passed = False
        self.started = False
        self.complete = False
        self.has_lead = player1
        self.trick = []
        self.trick_suit = ""
        self.trick_num = 0
        self.hearts_broken = False
        self.round_score = {player1.name: 0, player2.name: 0, player3.name: 0, player4.name: 0}
        if pass_dir in self.pass_options:
            self.pass_dir = pass_dir
        else:
            print("Invalid pass direction")

    def __eq__(self, other):
        """Defines equality amongst rounds"""
        return self.players == other.players and self.played_players == other.played_players and self.played_all == other.played_all and \
            self.passed_players == other.passed_players and self.passed == other.passed and self.started == \
            other.started and self.complete == other.complete and self.has_lead == other.has_lead and self.trick == \
            other.trick and self.trick_suit == other.trick_suit and self.trick_num == other.trick_num and \
            self.hearts_broken == other.hearts_broken and self.round_score == other.round_score and self.pass_dir == \
            other.pass_dir

    def player_rotation(self):
        """Determines the player rotation given the player with the lead"""
        lead_position = self.players.index(self.has_lead)
        if lead_position == 0:
            return self.players[1:]
        if lead_position == 1:
            return [self.players[2], self.players[3], self.players[0]]
        if lead_position == 2:
            return [self.players[3], self.players[0], self.players[1]]
        if lead_position == 3:
            return self.players[:3]

    def player_order(self, player):
        """Gives the clockwise order for the other players in the game given a particular order"""
        lead_position = self.players.index(player)
        if lead_position == 0:
            return self.players[1:]
        if lead_position == 1:
            return [self.players[2], self.players[3], self.players[0]]
        if lead_position == 2:
            return [self.players[3], self.players[0], self.players[1]]
        if lead_position == 3:
            return self.players[:3]

    def equivalent_moves(self, player):
        """Determines if all of a players legal moves are equivalent"""
        legal_moves = player.hand.legal_moves(self.trick, self.trick_num, self.hearts_broken)
        card_suit = legal_moves[0].suit
        for cards in legal_moves[1:]:
            if cards.suit != card_suit:
                return False
        low_card = legal_moves[0]
        for cards in legal_moves[1:]:
            if low_card.hearts_compare(cards):
                low_card = cards
        high_card = legal_moves[0]
        for cards in legal_moves[1:]:
            if not high_card.hearts_compare(cards):
                high_card = cards
        higher_cards = low_card.cards_above()
        lower_cards = high_card.cards_below()
        inbetween_cards = [i for i in lower_cards if i in higher_cards]

        for cards in inbetween_cards:
            if cards not in self.played_all and cards not in player.hand.contents or cards in self.trick:
                return False
        return True

    def points_remain(self):
        """Determines if points remain in the round"""
        points_cards = [Card("2", "hearts"), Card("3", "hearts"), Card("4", "hearts"), Card("5", "hearts"),
                        Card("6", "hearts"), Card("7", "hearts"), Card("8", "hearts"), Card("9", "hearts"),
                        Card("10", "hearts"), Card("jack", "hearts"), Card("queen", "hearts"), Card("king", "hearts"),
                        Card("ace", "hearts"), Card("queen", "spades")]

        for cards in points_cards:
            if cards not in self.played_all or cards in self.trick:
                return True
        return False

    def cant_effect_outcome(self, player):
        """Determines if any of the cards in the players hand can win a trick and if any of them contain points"""
        player_hand = player.hand.contents
        points_cards = [Card("2", "hearts"), Card("3", "hearts"), Card("4", "hearts"), Card("5", "hearts"),
                        Card("6", "hearts"), Card("7", "hearts"), Card("8", "hearts"), Card("9", "hearts"),
                        Card("10", "hearts"), Card("jack", "hearts"), Card("queen", "hearts"), Card("king", "hearts"),
                        Card("ace", "hearts"), Card("queen", "spades")]

        for cards in player_hand:
            if cards in points_cards:
                return False
            lower_cards = cards.cards_below()
            for card in lower_cards:
                if card not in self.played_all and card not in player.hand.contents or card in self.trick:
                    return False
        return True

    def start_passing(self):
        """Starts a passing before a round of hearts"""
        if self.passed is False and self.trick_num == 0 and self.pass_dir != "none":
            passes = {}
            for player in self.players:
                passes[player.name] = player.choose_pass()

            if self.pass_dir == "left":
                for i, player in enumerate(self.players):
                    pass_to_player = self.players[(i + 1) % 4]
                    list.extend(player.knowledge["held by left"], passes[player.name])
                    for cards in passes[player.name]:
                        pass_to_player.hand.add_card(cards)
                        list.remove(pass_to_player.knowledge["held by any"], cards)
                    if pass_to_player.ai == "human":
                        print(pass_to_player.name, "has been passed:\n", passes[player.name])

            if self.pass_dir == "right":
                for i, player in enumerate(self.players):
                    pass_to_player = self.players[(i - 1) % 4]
                    list.extend(player.knowledge["held by right"], passes[player.name])
                    for cards in passes[player.name]:
                        pass_to_player.hand.add_card(cards)
                        list.remove(pass_to_player.knowledge["held by any"], cards)
                    if pass_to_player.ai == "human":
                        print(pass_to_player.name, "has been passed:\n", passes[player.name])

            if self.pass_dir == "across":
                for i, player in enumerate(self.players):
                    pass_to_player = self.players[(i + 2) % 4]
                    list.extend(player.knowledge["held by across"], passes[player.name])
                    for cards in passes[player.name]:
                        pass_to_player.hand.add_card(cards)
                        list.remove(pass_to_player.knowledge["held by any"], cards)
                    if pass_to_player.ai == "human":
                        print(pass_to_player.name, "has been passed:\n", passes[player.name])

            self.passed_players = passes
            self.passed = True

        else:
            if self.pass_dir == "none":
                self.passed = True
            else:
                print("Players already passed")

    def start_passing_np(self):
        """Starts a passing before a round of hearts with no printing"""
        if self.passed is False and self.trick_num == 0 and self.pass_dir != "none":
            passes = {}
            for player in self.players:
                passes[player.name] = player.choose_pass()

            if self.pass_dir == "left":
                for i, player in enumerate(self.players):
                    pass_to_player = self.players[(i + 1) % 4]
                    list.extend(player.knowledge["held by left"], passes[player.name])
                    for cards in passes[player.name]:
                        pass_to_player.hand.add_card(cards)
                        list.remove(pass_to_player.knowledge["held by any"], cards)

            if self.pass_dir == "right":
                for i, player in enumerate(self.players):
                    pass_to_player = self.players[(i - 1) % 4]
                    list.extend(player.knowledge["held by right"], passes[player.name])
                    for cards in passes[player.name]:
                        pass_to_player.hand.add_card(cards)
                        list.remove(pass_to_player.knowledge["held by any"], cards)

            if self.pass_dir == "across":
                for i, player in enumerate(self.players):
                    pass_to_player = self.players[(i + 2) % 4]
                    list.extend(player.knowledge["held by across"], passes[player.name])
                    for cards in passes[player.name]:
                        pass_to_player.hand.add_card(cards)
                        list.remove(pass_to_player.knowledge["held by any"], cards)

            self.passed_players = passes
            self.passed = True

        else:
            if self.pass_dir == "none":
                self.passed = True

    def play_trick(self):
        """Initiates the next trick of the round"""
        if self.passed is False:
            print("Please pass first")
            return
        if self.trick_num >= 13:
            print("Round over!")
            return

        elif self.trick_num == 0 and self.trick == []:
            self.started = True
            for player in self.players:
                if player.hand.one_suit():
                    single_suit = player.hand.contents[0].suit
                    player.knowledge["left no " + single_suit] = True
                    player.knowledge["across no " + single_suit] = True
                    player.knowledge["right no " + single_suit] = True
                if player.has_start() is True:
                    self.has_lead = player
            self.trick.append(self.has_lead.play_card(Card("2", "clubs")))
            self.trick_suit = "clubs"
            self.played_all.append(Card("2", "clubs"))
            self.played_players[self.has_lead.name].append(Card("2", "clubs"))
            print(self.has_lead.name, "played:", Card("2", "clubs"))
            for player in self.player_rotation():
                if self.trick[0] in player.knowledge["held by any"]:
                    list.remove(player.knowledge["held by any"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left"]:
                    list.remove(player.knowledge["held by left"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by across"]:
                    list.remove(player.knowledge["held by across"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by right"]:
                    list.remove(player.knowledge["held by right"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left or across"]:
                    list.remove(player.knowledge["held by left or across"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left or right"]:
                    list.remove(player.knowledge["held by left or right"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by across or right"]:
                    list.remove(player.knowledge["held by across or right"], self.trick[0])

                card_to_play = player.choose_play(self)
                while card_to_play.suit != self.trick_suit and player.has_suit(self.trick_suit):
                    print("Invalid play: you must follow suit - try again")
                    card_to_play = player.choose_play(self)

                while card_to_play.suit == "hearts" or card_to_play == Card("queen", "spades"):
                    print("Invalid play: no points on the first trick - try again")
                    card_to_play = player.choose_play(self)
                    if not player.has_suit("diamonds") and not player.has_suit("clubs") \
                            and not player.has_suit("spades") or not player.has_suit("diamonds") \
                            and not player.has_suit("clubs") and player.count_suit("hearts") == 12 \
                            and player.has_start("queen", "spades"):
                        break

                notify_players = self.player_order(player)

                for p in notify_players:
                    if card_to_play in p.knowledge["held by any"]:
                        list.remove(p.knowledge["held by any"], card_to_play)
                    elif card_to_play in p.knowledge["held by left"]:
                        list.remove(p.knowledge["held by left"], card_to_play)
                    elif card_to_play in p.knowledge["held by across"]:
                        list.remove(p.knowledge["held by across"], card_to_play)
                    elif card_to_play in p.knowledge["held by right"]:
                        list.remove(p.knowledge["held by right"], card_to_play)
                    elif card_to_play in p.knowledge["held by left or across"]:
                        list.remove(p.knowledge["held by left or across"], card_to_play)
                    elif card_to_play in p.knowledge["held by left or right"]:
                        list.remove(p.knowledge["held by left or right"], card_to_play)
                    elif card_to_play in p.knowledge["held by across or right"]:
                        list.remove(p.knowledge["held by across or right"], card_to_play)

                if card_to_play.suit != self.trick_suit:
                    if card_to_play == Card("queen", "spades"):
                        notify_players[0].knowledge["only points"] = 2
                        notify_players[1].knowledge["only points"] = 1
                        notify_players[2].knowledge["only points"] = 0

                        if not notify_players[0].knowledge["right no " + self.trick_suit]:
                            notify_players[0].knowledge["right no " + self.trick_suit] = True
                            notify_players[0].knowledge["right no spades"] = True
                            notify_players[0].knowledge["right no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by any"] = [i for i in
                                                                          notify_players[0].knowledge["held by any"] if
                                                                          i not in cards_to_remove]
                            notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by left or right"] = \
                                [i for i in notify_players[0].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by across or right"] = \
                                [i for i in notify_players[0].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                            if notify_players[0].has_suit("hearts"):
                                notify_players[0].knowledge["held by right"].extend(
                                    notify_players[0].knowledge["held by any"])
                                notify_players[0].knowledge["held by any"] = []

                        if not notify_players[1].knowledge["across no " + self.trick_suit]:
                            notify_players[1].knowledge["across no " + self.trick_suit] = True
                            notify_players[1].knowledge["across no spades"] = True
                            notify_players[1].knowledge["across no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by any"] = \
                                [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by left or across"] = \
                                [i for i in notify_players[1].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by across or right"] = \
                                [i for i in notify_players[1].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                            if notify_players[1].has_suit("hearts"):
                                notify_players[1].knowledge["held by across"].extend(
                                    notify_players[1].knowledge["held by any"])
                                notify_players[1].knowledge["held by any"] = []
                        if not notify_players[2].knowledge["left no " + self.trick_suit]:
                            notify_players[2].knowledge["left no " + self.trick_suit] = True
                            notify_players[2].knowledge["left no spades"] = True
                            notify_players[2].knowledge["left no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by any"] = \
                                [i for i in notify_players[2].knowledge["held by any"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or across"] = \
                                [i for i in notify_players[2].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or right"] = \
                                [i for i in notify_players[2].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                            if notify_players[2].has_suit("hearts"):
                                notify_players[2].knowledge["held by left"].extend(
                                    notify_players[2].knowledge["held by any"])
                                notify_players[2].knowledge["held by any"] = []

                    elif card_to_play.suit == "hearts":
                        notify_players[0].knowledge["only points"] = 2
                        notify_players[1].knowledge["only points"] = 1
                        notify_players[2].knowledge["only points"] = 0
                        if not notify_players[0].knowledge["right no " + self.trick_suit]:
                            notify_players[0].knowledge["right no " + self.trick_suit] = True
                            notify_players[0].knowledge["right no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by any"] = [i for i in
                                                                          notify_players[0].knowledge["held by any"] if
                                                                          i not in cards_to_remove]
                            notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by left or right"] = \
                                [i for i in notify_players[0].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by across or right"] = \
                                [i for i in notify_players[0].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                            if Card("queen", "spades") in notify_players[0].hand or notify_players[0].has_suit("hearts"):
                                notify_players[0].knowledge["held by right"].extend(notify_players[0].knowledge["held by any"])
                                notify_players[0].knowledge["held by any"] = []

                        if not notify_players[1].knowledge["across no " + self.trick_suit]:
                            notify_players[1].knowledge["across no " + self.trick_suit] = True
                            notify_players[1].knowledge["across no spades"] = True
                            notify_players[1].knowledge["across no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by any"] = \
                                [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by left or across"] = \
                                [i for i in notify_players[1].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by across or right"] = \
                                [i for i in notify_players[1].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                            if Card("queen", "spades") in notify_players[1].hand or notify_players[1].has_suit("hearts"):
                                notify_players[1].knowledge["held by across"].extend(notify_players[1].knowledge["held by any"])
                                notify_players[1].knowledge["held by any"] = []
                        if not notify_players[2].knowledge["left no " + self.trick_suit]:
                            notify_players[2].knowledge["left no " + self.trick_suit] = True
                            notify_players[2].knowledge["left no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by any"] = \
                                [i for i in notify_players[2].knowledge["held by any"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or across"] = \
                                [i for i in notify_players[2].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or right"] = \
                                [i for i in notify_players[2].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                            if Card("queen", "spades") in notify_players[2].hand or notify_players[2].has_suit("hearts"):
                                notify_players[2].knowledge["held by left"].extend(notify_players[2].knowledge["held by any"])
                                notify_players[2].knowledge["held by any"] = []
                    else:
                        if not notify_players[0].knowledge["right no " + self.trick_suit]:
                            notify_players[0].knowledge["right no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by any"] = [i for i in
                                                                          notify_players[0].knowledge["held by any"] if
                                                                          i not in cards_to_remove]
                            notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by left or right"] = \
                                [i for i in notify_players[0].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by across or right"] = \
                                [i for i in notify_players[0].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                        if not notify_players[1].knowledge["across no " + self.trick_suit]:
                            notify_players[1].knowledge["across no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by any"] = \
                                [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by left or across"] = \
                                [i for i in notify_players[1].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by across or right"] = \
                                [i for i in notify_players[1].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                        if not notify_players[2].knowledge["left no " + self.trick_suit]:
                            notify_players[2].knowledge["left no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by any"] = \
                                [i for i in notify_players[2].knowledge["held by any"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or across"] = \
                                [i for i in notify_players[2].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or right"] = \
                                [i for i in notify_players[2].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by right"].extend(cards_to_remove)

                self.trick.append(card_to_play)
                player.hand.remove_card(card_to_play)
                self.played_all.append(card_to_play)
                self.played_players[player.name].append(card_to_play)
                print(player.name, "played:", card_to_play)
            print(self.trick)

        elif self.trick_num == 0:
            trick_progress = len(self.trick) - 1
            rotation = self.player_rotation()
            last_card = self.trick[trick_progress]
            if trick_progress == 0:
                last_player = self.has_lead
            else:
                last_player = rotation[trick_progress - 1]

            notify_players = self.player_order(last_player)

            for p in notify_players:
                if last_card in p.knowledge["held by any"]:
                    list.remove(p.knowledge["held by any"], last_card)
                elif last_card in p.knowledge["held by left"]:
                    list.remove(p.knowledge["held by left"], last_card)
                elif last_card in p.knowledge["held by across"]:
                    list.remove(p.knowledge["held by across"], last_card)
                elif last_card in p.knowledge["held by right"]:
                    list.remove(p.knowledge["held by right"], last_card)
                elif last_card in p.knowledge["held by left or across"]:
                    list.remove(p.knowledge["held by left or across"], last_card)
                elif last_card in p.knowledge["held by left or right"]:
                    list.remove(p.knowledge["held by left or right"], last_card)
                elif last_card in p.knowledge["held by across or right"]:
                    list.remove(p.knowledge["held by across or right"], last_card)

            if last_card.suit != self.trick_suit:
                if last_card == Card("queen", "spades"):
                    notify_players[0].knowledge["only points"] = 2
                    notify_players[1].knowledge["only points"] = 1
                    notify_players[2].knowledge["only points"] = 0

                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        notify_players[0].knowledge["right no spades"] = True
                        notify_players[0].knowledge["right no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                        if notify_players[0].has_suit("hearts"):
                            notify_players[0].knowledge["held by right"].extend(
                                notify_players[0].knowledge["held by any"])
                            notify_players[0].knowledge["held by any"] = []

                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        notify_players[1].knowledge["across no spades"] = True
                        notify_players[1].knowledge["across no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                        if notify_players[1].has_suit("hearts"):
                            notify_players[1].knowledge["held by across"].extend(
                                notify_players[1].knowledge["held by any"])
                            notify_players[1].knowledge["held by any"] = []
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        notify_players[2].knowledge["left no spades"] = True
                        notify_players[2].knowledge["left no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                        if notify_players[2].has_suit("hearts"):
                            notify_players[2].knowledge["held by left"].extend(
                                notify_players[2].knowledge["held by any"])
                            notify_players[2].knowledge["held by any"] = []

                elif last_card.suit == "hearts":
                    notify_players[0].knowledge["only points"] = 2
                    notify_players[1].knowledge["only points"] = 1
                    notify_players[2].knowledge["only points"] = 0
                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        notify_players[0].knowledge["right no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                        if Card("queen", "spades") in notify_players[0].hand or notify_players[0].has_suit("hearts"):
                            notify_players[0].knowledge["held by right"].extend(
                                notify_players[0].knowledge["held by any"])
                            notify_players[0].knowledge["held by any"] = []

                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        notify_players[1].knowledge["across no spades"] = True
                        notify_players[1].knowledge["across no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                        if Card("queen", "spades") in notify_players[1].hand or notify_players[1].has_suit("hearts"):
                            notify_players[1].knowledge["held by across"].extend(
                                notify_players[1].knowledge["held by any"])
                            notify_players[1].knowledge["held by any"] = []
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        notify_players[2].knowledge["left no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                        if Card("queen", "spades") in notify_players[2].hand or notify_players[2].has_suit("hearts"):
                            notify_players[2].knowledge["held by left"].extend(
                                notify_players[2].knowledge["held by any"])
                            notify_players[2].knowledge["held by any"] = []
                else:
                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)

            if trick_progress < 3:
                for player in rotation[trick_progress:]:
                    if self.trick[0] in player.knowledge["held by any"]:
                        list.remove(player.knowledge["held by any"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left"]:
                        list.remove(player.knowledge["held by left"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by across"]:
                        list.remove(player.knowledge["held by across"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by right"]:
                        list.remove(player.knowledge["held by right"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left or across"]:
                        list.remove(player.knowledge["held by left or across"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left or right"]:
                        list.remove(player.knowledge["held by left or right"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by across or right"]:
                        list.remove(player.knowledge["held by across or right"], self.trick[0])

                    card_to_play = player.choose_play(self)
                    while card_to_play.suit != self.trick_suit and player.has_suit(self.trick_suit):
                        print("Invalid play: you must follow suit - try again")
                        card_to_play = player.choose_play(self)

                    while card_to_play.suit == "hearts" or card_to_play == Card("queen", "spades"):
                        print("Invalid play: no points on the first trick - try again")
                        card_to_play = player.choose_play(self)
                        if not player.has_suit("diamonds") and not player.has_suit("clubs") \
                                and not player.has_suit("spades") or not player.has_suit("diamonds") \
                                and not player.has_suit("clubs") and player.count_suit("hearts") == 12 \
                                and player.has_start("queen", "spades"):
                            break

                    notify_players = self.player_order(player)

                    for p in notify_players:
                        if card_to_play in p.knowledge["held by any"]:
                            list.remove(p.knowledge["held by any"], card_to_play)
                        elif card_to_play in p.knowledge["held by left"]:
                            list.remove(p.knowledge["held by left"], card_to_play)
                        elif card_to_play in p.knowledge["held by across"]:
                            list.remove(p.knowledge["held by across"], card_to_play)
                        elif card_to_play in p.knowledge["held by right"]:
                            list.remove(p.knowledge["held by right"], card_to_play)
                        elif card_to_play in p.knowledge["held by left or across"]:
                            list.remove(p.knowledge["held by left or across"], card_to_play)
                        elif card_to_play in p.knowledge["held by left or right"]:
                            list.remove(p.knowledge["held by left or right"], card_to_play)
                        elif card_to_play in p.knowledge["held by across or right"]:
                            list.remove(p.knowledge["held by across or right"], card_to_play)

                    if card_to_play.suit != self.trick_suit:
                        if card_to_play == Card("queen", "spades"):
                            notify_players[0].knowledge["only points"] = 2
                            notify_players[1].knowledge["only points"] = 1
                            notify_players[2].knowledge["only points"] = 0

                            if not notify_players[0].knowledge["right no " + self.trick_suit]:
                                notify_players[0].knowledge["right no " + self.trick_suit] = True
                                notify_players[0].knowledge["right no spades"] = True
                                notify_players[0].knowledge["right no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by any"] = [i for i in
                                                                              notify_players[0].knowledge["held by any"] if
                                                                              i not in cards_to_remove]
                                notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by left or right"] = \
                                    [i for i in notify_players[0].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by across or right"] = \
                                    [i for i in notify_players[0].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                                if notify_players[0].has_suit("hearts"):
                                    notify_players[0].knowledge["held by right"].extend(
                                        notify_players[0].knowledge["held by any"])
                                    notify_players[0].knowledge["held by any"] = []

                            if not notify_players[1].knowledge["across no " + self.trick_suit]:
                                notify_players[1].knowledge["across no " + self.trick_suit] = True
                                notify_players[1].knowledge["across no spades"] = True
                                notify_players[1].knowledge["across no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by any"] = \
                                    [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by left or across"] = \
                                    [i for i in notify_players[1].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by across or right"] = \
                                    [i for i in notify_players[1].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                                if notify_players[1].has_suit("hearts"):
                                    notify_players[1].knowledge["held by across"].extend(
                                        notify_players[1].knowledge["held by any"])
                                    notify_players[1].knowledge["held by any"] = []
                            if not notify_players[2].knowledge["left no " + self.trick_suit]:
                                notify_players[2].knowledge["left no " + self.trick_suit] = True
                                notify_players[2].knowledge["left no spades"] = True
                                notify_players[2].knowledge["left no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by any"] = \
                                    [i for i in notify_players[2].knowledge["held by any"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or across"] = \
                                    [i for i in notify_players[2].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or right"] = \
                                    [i for i in notify_players[2].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                                if notify_players[2].has_suit("hearts"):
                                    notify_players[2].knowledge["held by left"].extend(
                                        notify_players[2].knowledge["held by any"])
                                    notify_players[2].knowledge["held by any"] = []

                        elif card_to_play.suit == "hearts":
                            notify_players[0].knowledge["only points"] = 2
                            notify_players[1].knowledge["only points"] = 1
                            notify_players[2].knowledge["only points"] = 0
                            if not notify_players[0].knowledge["right no " + self.trick_suit]:
                                notify_players[0].knowledge["right no " + self.trick_suit] = True
                                notify_players[0].knowledge["right no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by any"] = [i for i in
                                                                              notify_players[0].knowledge["held by any"] if
                                                                              i not in cards_to_remove]
                                notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by left or right"] = \
                                    [i for i in notify_players[0].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by across or right"] = \
                                    [i for i in notify_players[0].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                                if Card("queen", "spades") in notify_players[0].hand or notify_players[0].has_suit("hearts"):
                                    notify_players[0].knowledge["held by right"].extend(notify_players[0].knowledge["held by any"])
                                    notify_players[0].knowledge["held by any"] = []

                            if not notify_players[1].knowledge["across no " + self.trick_suit]:
                                notify_players[1].knowledge["across no " + self.trick_suit] = True
                                notify_players[1].knowledge["across no spades"] = True
                                notify_players[1].knowledge["across no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by any"] = \
                                    [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by left or across"] = \
                                    [i for i in notify_players[1].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by across or right"] = \
                                    [i for i in notify_players[1].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                                if Card("queen", "spades") in notify_players[1].hand or notify_players[1].has_suit("hearts"):
                                    notify_players[1].knowledge["held by across"].extend(notify_players[1].knowledge["held by any"])
                                    notify_players[1].knowledge["held by any"] = []
                            if not notify_players[2].knowledge["left no " + self.trick_suit]:
                                notify_players[2].knowledge["left no " + self.trick_suit] = True
                                notify_players[2].knowledge["left no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by any"] = \
                                    [i for i in notify_players[2].knowledge["held by any"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or across"] = \
                                    [i for i in notify_players[2].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or right"] = \
                                    [i for i in notify_players[2].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                                if Card("queen", "spades") in notify_players[2].hand or notify_players[2].has_suit("hearts"):
                                    notify_players[2].knowledge["held by left"].extend(notify_players[2].knowledge["held by any"])
                                    notify_players[2].knowledge["held by any"] = []
                        else:
                            if not notify_players[0].knowledge["right no " + self.trick_suit]:
                                notify_players[0].knowledge["right no " + self.trick_suit] = True
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by any"] = [i for i in
                                                                              notify_players[0].knowledge["held by any"] if
                                                                              i not in cards_to_remove]
                                notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by left or right"] = \
                                    [i for i in notify_players[0].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by across or right"] = \
                                    [i for i in notify_players[0].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                            if not notify_players[1].knowledge["across no " + self.trick_suit]:
                                notify_players[1].knowledge["across no " + self.trick_suit] = True
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by any"] = \
                                    [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by left or across"] = \
                                    [i for i in notify_players[1].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by across or right"] = \
                                    [i for i in notify_players[1].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                            if not notify_players[2].knowledge["left no " + self.trick_suit]:
                                notify_players[2].knowledge["left no " + self.trick_suit] = True
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by any"] = \
                                    [i for i in notify_players[2].knowledge["held by any"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or across"] = \
                                    [i for i in notify_players[2].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or right"] = \
                                    [i for i in notify_players[2].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by right"].extend(cards_to_remove)

                    self.trick.append(card_to_play)
                    player.hand.remove_card(card_to_play)
                    self.played_all.append(card_to_play)
                    self.played_players[player.name].append(card_to_play)
                    print(player.name, "played:", card_to_play)
            print(self.trick)

        elif self.trick_num < 13 and self.trick == []:
            self.trick_suit = ""
            lead_card = self.has_lead.choose_play(self)
            while not self.hearts_broken and lead_card.suit == "hearts":
                print("Invalid play: hearts have not been broken - try again")
                lead_card = self.has_lead.choose_play(self)
                if not self.has_lead.has_suit("spades") and not self.has_lead.has_suit("diamonds") \
                        and not self.has_lead.has_suit("clubs"):
                    o_players = self.player_rotation()

                    o_players[0].knowledge["right no spades"] = True
                    o_players[0].knowledge["right no diamonds"] = True
                    o_players[0].knowledge["right no clubs"] = True
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by any"] = [i for i in
                                                             o_players[0].knowledge["held by any"] if
                                                             i not in cards_to_remove]
                    o_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by left or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by left or right"] = \
                        [i for i in o_players[0].knowledge["held by left or right"]
                         if i not in cards_to_remove]
                    o_players[0].knowledge["held by left"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by across or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by across or right"] = \
                        [i for i in o_players[0].knowledge["held by across or right"]
                         if i not in cards_to_remove]
                    o_players[0].knowledge["held by across"].extend(cards_to_remove)

                    o_players[1].knowledge["across no clubs"] = True
                    o_players[1].knowledge["across no spades"] = True
                    o_players[1].knowledge["across no diamonds"] = True
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by any"] = \
                        [i for i in o_players[1].knowledge["held by any"] if i not in cards_to_remove]
                    o_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by left or across"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by left or across"] = \
                        [i for i in o_players[1].knowledge["held by left or across"]
                         if i not in cards_to_remove]
                    o_players[1].knowledge["held by left"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by across or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by across or right"] = \
                        [i for i in o_players[1].knowledge["held by across or right"]
                         if i not in cards_to_remove]
                    o_players[1].knowledge["held by right"].extend(cards_to_remove)

                    o_players[2].knowledge["left no spades"] = True
                    o_players[2].knowledge["left no diamonds"] = True
                    o_players[2].knowledge["left no clubs"] = True
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by any"] = \
                        [i for i in o_players[2].knowledge["held by any"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by left or across"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by left or across"] = \
                        [i for i in o_players[2].knowledge["held by left or across"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by across"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by left or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by left or right"] = \
                        [i for i in o_players[2].knowledge["held by left or right"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by right"].extend(cards_to_remove)
                    break
            if (lead_card.suit == "hearts" or lead_card == Card("queen", "spades")) and self.has_lead.knowledge["only points"] != "":
                players_without_points = self.player_rotation()
                players_without_points.remove(players_without_points[self.has_lead.knowledge["only points"]])
                if players_without_points[0].knowledge["only points"] == 0:
                    players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge[
                        "held by any"]
                if players_without_points[0].knowledge["only points"] == 1:
                    players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge[
                        "held by any"]
                if players_without_points[0].knowledge["only points"] == 2:
                    players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge[
                        "held by any"]
                players_without_points[0].knowledge["held by any"] = []

                if players_without_points[1].knowledge["only points"] == 0:
                    players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge[
                        "held by any"]
                if players_without_points[1].knowledge["only points"] == 1:
                    players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge[
                        "held by any"]
                if players_without_points[1].knowledge["only points"] == 2:
                    players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge[
                        "held by any"]
                players_without_points[1].knowledge["held by any"] = []

            self.played_all.append(lead_card)
            self.has_lead.hand.remove_card(lead_card)

            notify_players = self.player_rotation()
            self.played_players[self.has_lead.name].append(lead_card)
            self.trick_suit = lead_card.suit
            self.trick.append(lead_card)
            print(self.has_lead.name, "played:", lead_card)
            for player in self.player_rotation():
                if self.trick[0] in player.knowledge["held by any"]:
                    list.remove(player.knowledge["held by any"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left"]:
                    list.remove(player.knowledge["held by left"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by across"]:
                    list.remove(player.knowledge["held by across"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by right"]:
                    list.remove(player.knowledge["held by right"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left or across"]:
                    list.remove(player.knowledge["held by left or across"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left or right"]:
                    list.remove(player.knowledge["held by left or right"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by across or right"]:
                    list.remove(player.knowledge["held by across or right"], self.trick[0])

                card_to_play = player.choose_play(self)
                while card_to_play.suit != self.trick_suit and player.has_suit(self.trick_suit):
                    print("Invalid play: you must follow suit - try again")
                    card_to_play = player.choose_play(self)

                notify_players = self.player_order(player)

                for p in notify_players:
                    if card_to_play in p.knowledge["held by any"]:
                        list.remove(p.knowledge["held by any"], card_to_play)
                    elif card_to_play in p.knowledge["held by left"]:
                        list.remove(p.knowledge["held by left"], card_to_play)
                    elif card_to_play in p.knowledge["held by across"]:
                        list.remove(p.knowledge["held by across"], card_to_play)
                    elif card_to_play in p.knowledge["held by right"]:
                        list.remove(p.knowledge["held by right"], card_to_play)
                    elif card_to_play in p.knowledge["held by left or across"]:
                        list.remove(p.knowledge["held by left or across"], card_to_play)
                    elif card_to_play in p.knowledge["held by left or right"]:
                        list.remove(p.knowledge["held by left or right"], card_to_play)
                    elif card_to_play in p.knowledge["held by across or right"]:
                        list.remove(p.knowledge["held by across or right"], card_to_play)

                if (card_to_play.suit == "hearts" or card_to_play == Card("queen", "spades")) and player.knowledge["only points"] != "":
                    players_without_points = notify_players
                    players_without_points.remove(players_without_points[player.knowledge["only points"]])
                    if players_without_points[0].knowledge["only points"] == 0:
                        players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge["held by any"]
                    if players_without_points[0].knowledge["only points"] == 1:
                        players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge["held by any"]
                    if players_without_points[0].knowledge["only points"] == 2:
                        players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge["held by any"]
                    players_without_points[0].knowledge["held by any"] = []

                    if players_without_points[1].knowledge["only points"] == 0:
                        players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge["held by any"]
                    if players_without_points[1].knowledge["only points"] == 1:
                        players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge["held by any"]
                    if players_without_points[1].knowledge["only points"] == 2:
                        players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge["held by any"]
                    players_without_points[1].knowledge["held by any"] = []

                if card_to_play.suit != self.trick_suit:
                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)

                self.trick.append(card_to_play)
                player.hand.remove_card(card_to_play)
                self.played_all.append(card_to_play)
                self.played_players[player.name].append(card_to_play)
                print(player.name, "played:", card_to_play)
            print(self.trick)

        elif self.trick_num < 13:
            trick_progress = len(self.trick) - 1
            rotation = self.player_rotation()
            last_card = self.trick[trick_progress]
            if trick_progress == 0:
                last_player = self.has_lead
            else:
                last_player = rotation[trick_progress - 1]

            notify_players = self.player_order(last_player)

            for p in notify_players:
                if last_card in p.knowledge["held by any"]:
                    list.remove(p.knowledge["held by any"], last_card)
                elif last_card in p.knowledge["held by left"]:
                    list.remove(p.knowledge["held by left"], last_card)
                elif last_card in p.knowledge["held by across"]:
                    list.remove(p.knowledge["held by across"], last_card)
                elif last_card in p.knowledge["held by right"]:
                    list.remove(p.knowledge["held by right"], last_card)
                elif last_card in p.knowledge["held by left or across"]:
                    list.remove(p.knowledge["held by left or across"], last_card)
                elif last_card in p.knowledge["held by left or right"]:
                    list.remove(p.knowledge["held by left or right"], last_card)
                elif last_card in p.knowledge["held by across or right"]:
                    list.remove(p.knowledge["held by across or right"], last_card)

            if trick_progress == 0:
                self.trick_suit = last_card.suit
                if not self.hearts_broken and last_card.suit == "hearts" and not self.has_lead.has_suit("spades") and \
                        not self.has_lead.has_suit("diamonds") and not self.has_lead.has_suit("clubs"):
                    o_players = self.player_rotation()

                    o_players[0].knowledge["right no spades"] = True
                    o_players[0].knowledge["right no diamonds"] = True
                    o_players[0].knowledge["right no clubs"] = True
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by any"] = [i for i in
                                                             o_players[0].knowledge["held by any"] if
                                                             i not in cards_to_remove]
                    o_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by left or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by left or right"] = \
                        [i for i in o_players[0].knowledge["held by left or right"]
                         if i not in cards_to_remove]
                    o_players[0].knowledge["held by left"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by across or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by across or right"] = \
                        [i for i in o_players[0].knowledge["held by across or right"]
                         if i not in cards_to_remove]
                    o_players[0].knowledge["held by across"].extend(cards_to_remove)

                    o_players[1].knowledge["across no clubs"] = True
                    o_players[1].knowledge["across no spades"] = True
                    o_players[1].knowledge["across no diamonds"] = True
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by any"] = \
                        [i for i in o_players[1].knowledge["held by any"] if i not in cards_to_remove]
                    o_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by left or across"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by left or across"] = \
                        [i for i in o_players[1].knowledge["held by left or across"]
                         if i not in cards_to_remove]
                    o_players[1].knowledge["held by left"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by across or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by across or right"] = \
                        [i for i in o_players[1].knowledge["held by across or right"]
                         if i not in cards_to_remove]
                    o_players[1].knowledge["held by right"].extend(cards_to_remove)

                    o_players[2].knowledge["left no spades"] = True
                    o_players[2].knowledge["left no diamonds"] = True
                    o_players[2].knowledge["left no clubs"] = True
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by any"] = \
                        [i for i in o_players[2].knowledge["held by any"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by left or across"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by left or across"] = \
                        [i for i in o_players[2].knowledge["held by left or across"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by across"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by left or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by left or right"] = \
                        [i for i in o_players[2].knowledge["held by left or right"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by right"].extend(cards_to_remove)
                if (last_card.suit == "hearts" or last_card == Card("queen", "spades")) and self.has_lead.knowledge["only points"] != "":
                    players_without_points = self.player_rotation()
                    players_without_points.remove(players_without_points[self.has_lead.knowledge["only points"]])
                    if players_without_points[0].knowledge["only points"] == 0:
                        players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge[
                            "held by any"]
                    if players_without_points[0].knowledge["only points"] == 1:
                        players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge[
                            "held by any"]
                    if players_without_points[0].knowledge["only points"] == 2:
                        players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge[
                            "held by any"]
                    players_without_points[0].knowledge["held by any"] = []

                    if players_without_points[1].knowledge["only points"] == 0:
                        players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge[
                            "held by any"]
                    if players_without_points[1].knowledge["only points"] == 1:
                        players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge[
                            "held by any"]
                    if players_without_points[1].knowledge["only points"] == 2:
                        players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge[
                            "held by any"]
                    players_without_points[1].knowledge["held by any"] = []

                if len(last_player.hand.contents) == len(notify_players[0].knowledge["held by right"]):
                    notify_players[0].knowledge["held by left"].extend(
                        notify_players[0].knowledge["held by left or right"])
                    notify_players[0].knowledge["held by left or right"] = []
                    notify_players[0].knowledge["held by across"].extend(
                        notify_players[0].knowledge["held by across or right"])
                    notify_players[0].knowledge["held by across or right"] = []
                    notify_players[0].knowledge["held by left or across"].extend(
                        notify_players[0].knowledge["held by any"])
                    notify_players[0].knowledge["held by any"] = []
                if len(last_player.hand.contents) == len(notify_players[1].knowledge["held by across"]):
                    notify_players[1].knowledge["held by left"].extend(
                        notify_players[1].knowledge["held by left or across"])
                    notify_players[1].knowledge["held by left or across"] = []
                    notify_players[1].knowledge["held by right"].extend(
                        notify_players[1].knowledge["held by across or right"])
                    notify_players[1].knowledge["held by across or right"] = []
                    notify_players[1].knowledge["held by left or right"].extend(
                        notify_players[1].knowledge["held by any"])
                    notify_players[1].knowledge["held by any"] = []
                if len(last_player.hand.contents) == len(notify_players[2].knowledge["held by left"]):
                    notify_players[2].knowledge["held by across"].extend(
                        notify_players[2].knowledge["held by left or across"])
                    notify_players[2].knowledge["held by left or across"] = []
                    notify_players[2].knowledge["held by right"].extend(
                        notify_players[2].knowledge["held by left or right"])
                    notify_players[2].knowledge["held by left or right"] = []
                    notify_players[2].knowledge["held by across or right"].extend(
                        notify_players[2].knowledge["held by any"])
                    notify_players[2].knowledge["held by any"] = []

                print(self.has_lead.name, "played:", last_card)
            else:
                if (last_card.suit == "hearts" or last_card == Card("queen", "spades")) and last_player.knowledge[
                        "only points"] != "":
                    players_without_points = notify_players
                    players_without_points.remove(players_without_points[last_player.knowledge["only points"]])
                    if players_without_points[0].knowledge["only points"] == 0:
                        players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge[
                            "held by any"]
                    if players_without_points[0].knowledge["only points"] == 1:
                        players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge[
                            "held by any"]
                    if players_without_points[0].knowledge["only points"] == 2:
                        players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge[
                            "held by any"]
                    players_without_points[0].knowledge["held by any"] = []

                    if players_without_points[1].knowledge["only points"] == 0:
                        players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge[
                            "held by any"]
                    if players_without_points[1].knowledge["only points"] == 1:
                        players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge[
                            "held by any"]
                    if players_without_points[1].knowledge["only points"] == 2:
                        players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge[
                            "held by any"]
                    players_without_points[1].knowledge["held by any"] = []

                if last_card.suit != self.trick_suit:
                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                print(last_player, "played:", last_card)
            if trick_progress < 3:
                for player in rotation[trick_progress:]:
                    if self.trick[0] in player.knowledge["held by any"]:
                        list.remove(player.knowledge["held by any"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left"]:
                        list.remove(player.knowledge["held by left"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by across"]:
                        list.remove(player.knowledge["held by across"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by right"]:
                        list.remove(player.knowledge["held by right"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left or across"]:
                        list.remove(player.knowledge["held by left or across"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left or right"]:
                        list.remove(player.knowledge["held by left or right"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by across or right"]:
                        list.remove(player.knowledge["held by across or right"], self.trick[0])

                    card_to_play = player.choose_play(self)
                    while card_to_play.suit != self.trick_suit and player.has_suit(self.trick_suit):
                        print("Invalid play: you must follow suit - try again")
                        card_to_play = player.choose_play(self)

                    notify_players = self.player_order(player)

                    for p in notify_players:
                        if card_to_play in p.knowledge["held by any"]:
                            list.remove(p.knowledge["held by any"], card_to_play)
                        elif card_to_play in p.knowledge["held by left"]:
                            list.remove(p.knowledge["held by left"], card_to_play)
                        elif card_to_play in p.knowledge["held by across"]:
                            list.remove(p.knowledge["held by across"], card_to_play)
                        elif card_to_play in p.knowledge["held by right"]:
                            list.remove(p.knowledge["held by right"], card_to_play)
                        elif card_to_play in p.knowledge["held by left or across"]:
                            list.remove(p.knowledge["held by left or across"], card_to_play)
                        elif card_to_play in p.knowledge["held by left or right"]:
                            list.remove(p.knowledge["held by left or right"], card_to_play)
                        elif card_to_play in p.knowledge["held by across or right"]:
                            list.remove(p.knowledge["held by across or right"], card_to_play)

                    if (card_to_play.suit == "hearts" or card_to_play == Card("queen", "spades")) and player.knowledge["only points"] != "":
                        players_without_points = notify_players
                        players_without_points.remove(players_without_points[player.knowledge["only points"]])
                        if players_without_points[0].knowledge["only points"] == 0:
                            players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge["held by any"]
                        if players_without_points[0].knowledge["only points"] == 1:
                            players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge["held by any"]
                        if players_without_points[0].knowledge["only points"] == 2:
                            players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge["held by any"]
                        players_without_points[0].knowledge["held by any"] = []

                        if players_without_points[1].knowledge["only points"] == 0:
                            players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge["held by any"]
                        if players_without_points[1].knowledge["only points"] == 1:
                            players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge["held by any"]
                        if players_without_points[1].knowledge["only points"] == 2:
                            players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge["held by any"]
                        players_without_points[1].knowledge["held by any"] = []

                    if card_to_play.suit != self.trick_suit:
                        if not notify_players[0].knowledge["right no " + self.trick_suit]:
                            notify_players[0].knowledge["right no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by any"] = [i for i in
                                                                          notify_players[0].knowledge["held by any"] if
                                                                          i not in cards_to_remove]
                            notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by left or right"] = \
                                [i for i in notify_players[0].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by across or right"] = \
                                [i for i in notify_players[0].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                        if not notify_players[1].knowledge["across no " + self.trick_suit]:
                            notify_players[1].knowledge["across no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by any"] = \
                                [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by left or across"] = \
                                [i for i in notify_players[1].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by across or right"] = \
                                [i for i in notify_players[1].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                        if not notify_players[2].knowledge["left no " + self.trick_suit]:
                            notify_players[2].knowledge["left no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by any"] = \
                                [i for i in notify_players[2].knowledge["held by any"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or across"] = \
                                [i for i in notify_players[2].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or right"] = \
                                [i for i in notify_players[2].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by right"].extend(cards_to_remove)

                    self.trick.append(card_to_play)
                    player.hand.remove_card(card_to_play)
                    self.played_all.append(card_to_play)
                    self.played_players[player.name].append(card_to_play)
                    print(player.name, "played:", card_to_play)
            print(self.trick)

        high_card = self.trick[0]
        for card in self.trick:
            if card.hearts_compare(high_card):
                high_card = card
            if card.suit == "hearts" and not self.hearts_broken:
                self.hearts_broken = True
        high_card_index = self.trick.index(high_card)
        if high_card_index == 0:
            self.has_lead.won_cards.extend(self.trick)
        if high_card_index > 0:
            other_players = self.player_rotation()
            self.has_lead = other_players[high_card_index - 1]
            self.has_lead.won_cards.extend(self.trick)
        self.trick_num += 1
        if self.trick_num == 13:
            self.complete = True
        self.trick = []
        self.trick_suit = ""
        print(self.has_lead.name, "has won trick", self.trick_num, "with the", high_card)

    def play_trick_np(self):
        """Plays trick with no printing"""
        if self.passed is False:
            return
        if self.trick_num >= 13:
            return

        elif self.trick_num == 0 and self.trick == []:
            self.started = True
            for player in self.players:
                if player.hand.one_suit():
                    single_suit = player.hand.contents[0].suit
                    player.knowledge["left no " + single_suit] = True
                    player.knowledge["across no " + single_suit] = True
                    player.knowledge["right no " + single_suit] = True
                if player.has_start() is True:
                    self.has_lead = player
            self.trick.append(self.has_lead.play_card(Card("2", "clubs")))
            self.trick_suit = "clubs"
            self.played_all.append(Card("2", "clubs"))
            self.played_players[self.has_lead.name].append(Card("2", "clubs"))
            for player in self.player_rotation():
                if self.trick[0] in player.knowledge["held by any"]:
                    list.remove(player.knowledge["held by any"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left"]:
                    list.remove(player.knowledge["held by left"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by across"]:
                    list.remove(player.knowledge["held by across"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by right"]:
                    list.remove(player.knowledge["held by right"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left or across"]:
                    list.remove(player.knowledge["held by left or across"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left or right"]:
                    list.remove(player.knowledge["held by left or right"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by across or right"]:
                    list.remove(player.knowledge["held by across or right"], self.trick[0])

                card_to_play = player.choose_play(self)
                while card_to_play.suit != self.trick_suit and player.has_suit(self.trick_suit):
                    card_to_play = player.choose_play(self)

                while card_to_play.suit == "hearts" or card_to_play == Card("queen", "spades"):
                    card_to_play = player.choose_play(self)
                    if not player.has_suit("diamonds") and not player.has_suit("clubs") \
                            and not player.has_suit("spades") or not player.has_suit("diamonds") \
                            and not player.has_suit("clubs") and player.count_suit("hearts") == 12 \
                            and player.has_start("queen", "spades"):
                        break

                notify_players = self.player_order(player)

                for p in notify_players:
                    if card_to_play in p.knowledge["held by any"]:
                        list.remove(p.knowledge["held by any"], card_to_play)
                    elif card_to_play in p.knowledge["held by left"]:
                        list.remove(p.knowledge["held by left"], card_to_play)
                    elif card_to_play in p.knowledge["held by across"]:
                        list.remove(p.knowledge["held by across"], card_to_play)
                    elif card_to_play in p.knowledge["held by right"]:
                        list.remove(p.knowledge["held by right"], card_to_play)
                    elif card_to_play in p.knowledge["held by left or across"]:
                        list.remove(p.knowledge["held by left or across"], card_to_play)
                    elif card_to_play in p.knowledge["held by left or right"]:
                        list.remove(p.knowledge["held by left or right"], card_to_play)
                    elif card_to_play in p.knowledge["held by across or right"]:
                        list.remove(p.knowledge["held by across or right"], card_to_play)

                if card_to_play.suit != self.trick_suit:
                    if card_to_play == Card("queen", "spades"):
                        notify_players[0].knowledge["only points"] = 2
                        notify_players[1].knowledge["only points"] = 1
                        notify_players[2].knowledge["only points"] = 0

                        if not notify_players[0].knowledge["right no " + self.trick_suit]:
                            notify_players[0].knowledge["right no " + self.trick_suit] = True
                            notify_players[0].knowledge["right no spades"] = True
                            notify_players[0].knowledge["right no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by any"] = [i for i in
                                                                          notify_players[0].knowledge["held by any"] if
                                                                          i not in cards_to_remove]
                            notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by left or right"] = \
                                [i for i in notify_players[0].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by across or right"] = \
                                [i for i in notify_players[0].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                            if notify_players[0].has_suit("hearts"):
                                notify_players[0].knowledge["held by right"].extend(
                                    notify_players[0].knowledge["held by any"])
                                notify_players[0].knowledge["held by any"] = []

                        if not notify_players[1].knowledge["across no " + self.trick_suit]:
                            notify_players[1].knowledge["across no " + self.trick_suit] = True
                            notify_players[1].knowledge["across no spades"] = True
                            notify_players[1].knowledge["across no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by any"] = \
                                [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by left or across"] = \
                                [i for i in notify_players[1].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by across or right"] = \
                                [i for i in notify_players[1].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                            if notify_players[1].has_suit("hearts"):
                                notify_players[1].knowledge["held by across"].extend(
                                    notify_players[1].knowledge["held by any"])
                                notify_players[1].knowledge["held by any"] = []
                        if not notify_players[2].knowledge["left no " + self.trick_suit]:
                            notify_players[2].knowledge["left no " + self.trick_suit] = True
                            notify_players[2].knowledge["left no spades"] = True
                            notify_players[2].knowledge["left no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by any"] = \
                                [i for i in notify_players[2].knowledge["held by any"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or across"] = \
                                [i for i in notify_players[2].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or right"] = \
                                [i for i in notify_players[2].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                            if notify_players[2].has_suit("hearts"):
                                notify_players[2].knowledge["held by left"].extend(
                                    notify_players[2].knowledge["held by any"])
                                notify_players[2].knowledge["held by any"] = []

                    elif card_to_play.suit == "hearts":
                        notify_players[0].knowledge["only points"] = 2
                        notify_players[1].knowledge["only points"] = 1
                        notify_players[2].knowledge["only points"] = 0
                        if not notify_players[0].knowledge["right no " + self.trick_suit]:
                            notify_players[0].knowledge["right no " + self.trick_suit] = True
                            notify_players[0].knowledge["right no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by any"] = [i for i in
                                                                          notify_players[0].knowledge["held by any"] if
                                                                          i not in cards_to_remove]
                            notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by left or right"] = \
                                [i for i in notify_players[0].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by across or right"] = \
                                [i for i in notify_players[0].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                            if Card("queen", "spades") in notify_players[0].hand or notify_players[0].has_suit("hearts"):
                                notify_players[0].knowledge["held by right"].extend(notify_players[0].knowledge["held by any"])
                                notify_players[0].knowledge["held by any"] = []

                        if not notify_players[1].knowledge["across no " + self.trick_suit]:
                            notify_players[1].knowledge["across no " + self.trick_suit] = True
                            notify_players[1].knowledge["across no spades"] = True
                            notify_players[1].knowledge["across no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by any"] = \
                                [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by left or across"] = \
                                [i for i in notify_players[1].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by across or right"] = \
                                [i for i in notify_players[1].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                            if Card("queen", "spades") in notify_players[1].hand or notify_players[1].has_suit("hearts"):
                                notify_players[1].knowledge["held by across"].extend(notify_players[1].knowledge["held by any"])
                                notify_players[1].knowledge["held by any"] = []
                        if not notify_players[2].knowledge["left no " + self.trick_suit]:
                            notify_players[2].knowledge["left no " + self.trick_suit] = True
                            notify_players[2].knowledge["left no diamonds"] = True
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by any"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by any"] = \
                                [i for i in notify_players[2].knowledge["held by any"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or across"] = \
                                [i for i in notify_players[2].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                        or cards.suit == "diamonds":
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or right"] = \
                                [i for i in notify_players[2].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                            if Card("queen", "spades") in notify_players[2].hand or notify_players[2].has_suit("hearts"):
                                notify_players[2].knowledge["held by left"].extend(notify_players[2].knowledge["held by any"])
                                notify_players[2].knowledge["held by any"] = []
                    else:
                        if not notify_players[0].knowledge["right no " + self.trick_suit]:
                            notify_players[0].knowledge["right no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by any"] = [i for i in
                                                                          notify_players[0].knowledge["held by any"] if
                                                                          i not in cards_to_remove]
                            notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by left or right"] = \
                                [i for i in notify_players[0].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by across or right"] = \
                                [i for i in notify_players[0].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                        if not notify_players[1].knowledge["across no " + self.trick_suit]:
                            notify_players[1].knowledge["across no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by any"] = \
                                [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by left or across"] = \
                                [i for i in notify_players[1].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by across or right"] = \
                                [i for i in notify_players[1].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                        if not notify_players[2].knowledge["left no " + self.trick_suit]:
                            notify_players[2].knowledge["left no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by any"] = \
                                [i for i in notify_players[2].knowledge["held by any"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or across"] = \
                                [i for i in notify_players[2].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or right"] = \
                                [i for i in notify_players[2].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by right"].extend(cards_to_remove)

                self.trick.append(card_to_play)
                player.hand.remove_card(card_to_play)
                self.played_all.append(card_to_play)
                self.played_players[player.name].append(card_to_play)

        elif self.trick_num == 0:
            trick_progress = len(self.trick) - 1
            rotation = self.player_rotation()
            last_card = self.trick[trick_progress]
            if trick_progress == 0:
                last_player = self.has_lead
            else:
                last_player = rotation[trick_progress - 1]

            notify_players = self.player_order(last_player)

            for p in notify_players:
                if last_card in p.knowledge["held by any"]:
                    list.remove(p.knowledge["held by any"], last_card)
                elif last_card in p.knowledge["held by left"]:
                    list.remove(p.knowledge["held by left"], last_card)
                elif last_card in p.knowledge["held by across"]:
                    list.remove(p.knowledge["held by across"], last_card)
                elif last_card in p.knowledge["held by right"]:
                    list.remove(p.knowledge["held by right"], last_card)
                elif last_card in p.knowledge["held by left or across"]:
                    list.remove(p.knowledge["held by left or across"], last_card)
                elif last_card in p.knowledge["held by left or right"]:
                    list.remove(p.knowledge["held by left or right"], last_card)
                elif last_card in p.knowledge["held by across or right"]:
                    list.remove(p.knowledge["held by across or right"], last_card)

            if last_card.suit != self.trick_suit:
                if last_card == Card("queen", "spades"):
                    notify_players[0].knowledge["only points"] = 2
                    notify_players[1].knowledge["only points"] = 1
                    notify_players[2].knowledge["only points"] = 0

                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        notify_players[0].knowledge["right no spades"] = True
                        notify_players[0].knowledge["right no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                        if notify_players[0].has_suit("hearts"):
                            notify_players[0].knowledge["held by right"].extend(
                                notify_players[0].knowledge["held by any"])
                            notify_players[0].knowledge["held by any"] = []

                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        notify_players[1].knowledge["across no spades"] = True
                        notify_players[1].knowledge["across no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                        if notify_players[1].has_suit("hearts"):
                            notify_players[1].knowledge["held by across"].extend(
                                notify_players[1].knowledge["held by any"])
                            notify_players[1].knowledge["held by any"] = []
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        notify_players[2].knowledge["left no spades"] = True
                        notify_players[2].knowledge["left no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                        if notify_players[2].has_suit("hearts"):
                            notify_players[2].knowledge["held by left"].extend(
                                notify_players[2].knowledge["held by any"])
                            notify_players[2].knowledge["held by any"] = []

                elif last_card.suit == "hearts":
                    notify_players[0].knowledge["only points"] = 2
                    notify_players[1].knowledge["only points"] = 1
                    notify_players[2].knowledge["only points"] = 0
                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        notify_players[0].knowledge["right no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                        if Card("queen", "spades") in notify_players[0].hand or notify_players[0].has_suit("hearts"):
                            notify_players[0].knowledge["held by right"].extend(
                                notify_players[0].knowledge["held by any"])
                            notify_players[0].knowledge["held by any"] = []

                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        notify_players[1].knowledge["across no spades"] = True
                        notify_players[1].knowledge["across no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                        if Card("queen", "spades") in notify_players[1].hand or notify_players[1].has_suit("hearts"):
                            notify_players[1].knowledge["held by across"].extend(
                                notify_players[1].knowledge["held by any"])
                            notify_players[1].knowledge["held by any"] = []
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        notify_players[2].knowledge["left no diamonds"] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                    or cards.suit == "diamonds":
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                        if Card("queen", "spades") in notify_players[2].hand or notify_players[2].has_suit("hearts"):
                            notify_players[2].knowledge["held by left"].extend(
                                notify_players[2].knowledge["held by any"])
                            notify_players[2].knowledge["held by any"] = []
                else:
                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)

            if trick_progress < 3:
                for player in rotation[trick_progress:]:
                    if self.trick[0] in player.knowledge["held by any"]:
                        list.remove(player.knowledge["held by any"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left"]:
                        list.remove(player.knowledge["held by left"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by across"]:
                        list.remove(player.knowledge["held by across"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by right"]:
                        list.remove(player.knowledge["held by right"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left or across"]:
                        list.remove(player.knowledge["held by left or across"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left or right"]:
                        list.remove(player.knowledge["held by left or right"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by across or right"]:
                        list.remove(player.knowledge["held by across or right"], self.trick[0])

                    card_to_play = player.choose_play(self)
                    while card_to_play.suit != self.trick_suit and player.has_suit(self.trick_suit):
                        card_to_play = player.choose_play(self)

                    while card_to_play.suit == "hearts" or card_to_play == Card("queen", "spades"):
                        card_to_play = player.choose_play(self)
                        if not player.has_suit("diamonds") and not player.has_suit("clubs") \
                                and not player.has_suit("spades") or not player.has_suit("diamonds") \
                                and not player.has_suit("clubs") and player.count_suit("hearts") == 12 \
                                and player.has_start("queen", "spades"):
                            break

                    notify_players = self.player_order(player)

                    for p in notify_players:
                        if card_to_play in p.knowledge["held by any"]:
                            list.remove(p.knowledge["held by any"], card_to_play)
                        elif card_to_play in p.knowledge["held by left"]:
                            list.remove(p.knowledge["held by left"], card_to_play)
                        elif card_to_play in p.knowledge["held by across"]:
                            list.remove(p.knowledge["held by across"], card_to_play)
                        elif card_to_play in p.knowledge["held by right"]:
                            list.remove(p.knowledge["held by right"], card_to_play)
                        elif card_to_play in p.knowledge["held by left or across"]:
                            list.remove(p.knowledge["held by left or across"], card_to_play)
                        elif card_to_play in p.knowledge["held by left or right"]:
                            list.remove(p.knowledge["held by left or right"], card_to_play)
                        elif card_to_play in p.knowledge["held by across or right"]:
                            list.remove(p.knowledge["held by across or right"], card_to_play)

                    if card_to_play.suit != self.trick_suit:
                        if card_to_play == Card("queen", "spades"):
                            notify_players[0].knowledge["only points"] = 2
                            notify_players[1].knowledge["only points"] = 1
                            notify_players[2].knowledge["only points"] = 0

                            if not notify_players[0].knowledge["right no " + self.trick_suit]:
                                notify_players[0].knowledge["right no " + self.trick_suit] = True
                                notify_players[0].knowledge["right no spades"] = True
                                notify_players[0].knowledge["right no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by any"] = [i for i in
                                                                              notify_players[0].knowledge["held by any"] if
                                                                              i not in cards_to_remove]
                                notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by left or right"] = \
                                    [i for i in notify_players[0].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by across or right"] = \
                                    [i for i in notify_players[0].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                                if notify_players[0].has_suit("hearts"):
                                    notify_players[0].knowledge["held by right"].extend(
                                        notify_players[0].knowledge["held by any"])
                                    notify_players[0].knowledge["held by any"] = []

                            if not notify_players[1].knowledge["across no " + self.trick_suit]:
                                notify_players[1].knowledge["across no " + self.trick_suit] = True
                                notify_players[1].knowledge["across no spades"] = True
                                notify_players[1].knowledge["across no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by any"] = \
                                    [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by left or across"] = \
                                    [i for i in notify_players[1].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by across or right"] = \
                                    [i for i in notify_players[1].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                                if notify_players[1].has_suit("hearts"):
                                    notify_players[1].knowledge["held by across"].extend(
                                        notify_players[1].knowledge["held by any"])
                                    notify_players[1].knowledge["held by any"] = []
                            if not notify_players[2].knowledge["left no " + self.trick_suit]:
                                notify_players[2].knowledge["left no " + self.trick_suit] = True
                                notify_players[2].knowledge["left no spades"] = True
                                notify_players[2].knowledge["left no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by any"] = \
                                    [i for i in notify_players[2].knowledge["held by any"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or across"] = \
                                    [i for i in notify_players[2].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or right"] = \
                                    [i for i in notify_players[2].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                                if notify_players[2].has_suit("hearts"):
                                    notify_players[2].knowledge["held by left"].extend(
                                        notify_players[2].knowledge["held by any"])
                                    notify_players[2].knowledge["held by any"] = []

                        elif card_to_play.suit == "hearts":
                            notify_players[0].knowledge["only points"] = 2
                            notify_players[1].knowledge["only points"] = 1
                            notify_players[2].knowledge["only points"] = 0
                            if not notify_players[0].knowledge["right no " + self.trick_suit]:
                                notify_players[0].knowledge["right no " + self.trick_suit] = True
                                notify_players[0].knowledge["right no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by any"] = [i for i in
                                                                              notify_players[0].knowledge["held by any"] if
                                                                              i not in cards_to_remove]
                                notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by left or right"] = \
                                    [i for i in notify_players[0].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by across or right"] = \
                                    [i for i in notify_players[0].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                                if Card("queen", "spades") in notify_players[0].hand or notify_players[0].has_suit("hearts"):
                                    notify_players[0].knowledge["held by right"].extend(notify_players[0].knowledge["held by any"])
                                    notify_players[0].knowledge["held by any"] = []

                            if not notify_players[1].knowledge["across no " + self.trick_suit]:
                                notify_players[1].knowledge["across no " + self.trick_suit] = True
                                notify_players[1].knowledge["across no spades"] = True
                                notify_players[1].knowledge["across no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by any"] = \
                                    [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by left or across"] = \
                                    [i for i in notify_players[1].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by across or right"] = \
                                    [i for i in notify_players[1].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                                if Card("queen", "spades") in notify_players[1].hand or notify_players[1].has_suit("hearts"):
                                    notify_players[1].knowledge["held by across"].extend(notify_players[1].knowledge["held by any"])
                                    notify_players[1].knowledge["held by any"] = []
                            if not notify_players[2].knowledge["left no " + self.trick_suit]:
                                notify_players[2].knowledge["left no " + self.trick_suit] = True
                                notify_players[2].knowledge["left no diamonds"] = True
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by any"] = \
                                    [i for i in notify_players[2].knowledge["held by any"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or across"] = \
                                    [i for i in notify_players[2].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit or cards.suit == "spades" and cards.value != "queen" \
                                            or cards.suit == "diamonds":
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or right"] = \
                                    [i for i in notify_players[2].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by right"].extend(cards_to_remove)
                                if Card("queen", "spades") in notify_players[2].hand or notify_players[2].has_suit("hearts"):
                                    notify_players[2].knowledge["held by left"].extend(notify_players[2].knowledge["held by any"])
                                    notify_players[2].knowledge["held by any"] = []
                        else:
                            if not notify_players[0].knowledge["right no " + self.trick_suit]:
                                notify_players[0].knowledge["right no " + self.trick_suit] = True
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by any"] = [i for i in
                                                                              notify_players[0].knowledge["held by any"] if
                                                                              i not in cards_to_remove]
                                notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by left or right"] = \
                                    [i for i in notify_players[0].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[0].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[0].knowledge["held by across or right"] = \
                                    [i for i in notify_players[0].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                            if not notify_players[1].knowledge["across no " + self.trick_suit]:
                                notify_players[1].knowledge["across no " + self.trick_suit] = True
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by any"] = \
                                    [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by left or across"] = \
                                    [i for i in notify_players[1].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[1].knowledge["held by across or right"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[1].knowledge["held by across or right"] = \
                                    [i for i in notify_players[1].knowledge["held by across or right"]
                                     if i not in cards_to_remove]
                                notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                            if not notify_players[2].knowledge["left no " + self.trick_suit]:
                                notify_players[2].knowledge["left no " + self.trick_suit] = True
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by any"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by any"] = \
                                    [i for i in notify_players[2].knowledge["held by any"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or across"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or across"] = \
                                    [i for i in notify_players[2].knowledge["held by left or across"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                                cards_to_remove = []
                                for cards in notify_players[2].knowledge["held by left or right"]:
                                    if cards.suit == self.trick_suit:
                                        cards_to_remove.append(cards)
                                notify_players[2].knowledge["held by left or right"] = \
                                    [i for i in notify_players[2].knowledge["held by left or right"]
                                     if i not in cards_to_remove]
                                notify_players[2].knowledge["held by right"].extend(cards_to_remove)

                    self.trick.append(card_to_play)
                    player.hand.remove_card(card_to_play)
                    self.played_all.append(card_to_play)
                    self.played_players[player.name].append(card_to_play)

        elif self.trick_num < 13 and self.trick == []:
            self.trick_suit = ""
            lead_card = self.has_lead.choose_play(self)
            while not self.hearts_broken and lead_card.suit == "hearts":
                lead_card = self.has_lead.choose_play(self)
                if not self.has_lead.has_suit("spades") and not self.has_lead.has_suit("diamonds") \
                        and not self.has_lead.has_suit("clubs"):
                    o_players = self.player_rotation()

                    o_players[0].knowledge["right no spades"] = True
                    o_players[0].knowledge["right no diamonds"] = True
                    o_players[0].knowledge["right no clubs"] = True
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by any"] = [i for i in
                                                             o_players[0].knowledge["held by any"] if
                                                             i not in cards_to_remove]
                    o_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by left or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by left or right"] = \
                        [i for i in o_players[0].knowledge["held by left or right"]
                         if i not in cards_to_remove]
                    o_players[0].knowledge["held by left"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by across or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by across or right"] = \
                        [i for i in o_players[0].knowledge["held by across or right"]
                         if i not in cards_to_remove]
                    o_players[0].knowledge["held by across"].extend(cards_to_remove)

                    o_players[1].knowledge["across no clubs"] = True
                    o_players[1].knowledge["across no spades"] = True
                    o_players[1].knowledge["across no diamonds"] = True
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by any"] = \
                        [i for i in o_players[1].knowledge["held by any"] if i not in cards_to_remove]
                    o_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by left or across"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by left or across"] = \
                        [i for i in o_players[1].knowledge["held by left or across"]
                         if i not in cards_to_remove]
                    o_players[1].knowledge["held by left"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by across or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by across or right"] = \
                        [i for i in o_players[1].knowledge["held by across or right"]
                         if i not in cards_to_remove]
                    o_players[1].knowledge["held by right"].extend(cards_to_remove)

                    o_players[2].knowledge["left no spades"] = True
                    o_players[2].knowledge["left no diamonds"] = True
                    o_players[2].knowledge["left no clubs"] = True
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by any"] = \
                        [i for i in o_players[2].knowledge["held by any"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by left or across"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by left or across"] = \
                        [i for i in o_players[2].knowledge["held by left or across"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by across"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by left or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by left or right"] = \
                        [i for i in o_players[2].knowledge["held by left or right"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by right"].extend(cards_to_remove)
                    break
            if (lead_card.suit == "hearts" or lead_card == Card("queen", "spades")) and self.has_lead.knowledge["only points"] != "":
                players_without_points = self.player_rotation()
                players_without_points.remove(players_without_points[self.has_lead.knowledge["only points"]])
                if players_without_points[0].knowledge["only points"] == 0:
                    players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge[
                        "held by any"]
                if players_without_points[0].knowledge["only points"] == 1:
                    players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge[
                        "held by any"]
                if players_without_points[0].knowledge["only points"] == 2:
                    players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge[
                        "held by any"]
                players_without_points[0].knowledge["held by any"] = []

                if players_without_points[1].knowledge["only points"] == 0:
                    players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge[
                        "held by any"]
                if players_without_points[1].knowledge["only points"] == 1:
                    players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge[
                        "held by any"]
                if players_without_points[1].knowledge["only points"] == 2:
                    players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge[
                        "held by any"]
                players_without_points[1].knowledge["held by any"] = []

            self.played_all.append(lead_card)
            self.has_lead.hand.remove_card(lead_card)
            self.played_players[self.has_lead.name].append(lead_card)
            self.trick_suit = lead_card.suit
            self.trick.append(lead_card)
            for player in self.player_rotation():
                if self.trick[0] in player.knowledge["held by any"]:
                    list.remove(player.knowledge["held by any"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left"]:
                    list.remove(player.knowledge["held by left"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by across"]:
                    list.remove(player.knowledge["held by across"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by right"]:
                    list.remove(player.knowledge["held by right"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left or across"]:
                    list.remove(player.knowledge["held by left or across"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by left or right"]:
                    list.remove(player.knowledge["held by left or right"], self.trick[0])
                elif self.trick[0] in player.knowledge["held by across or right"]:
                    list.remove(player.knowledge["held by across or right"], self.trick[0])

                card_to_play = player.choose_play(self)
                while card_to_play.suit != self.trick_suit and player.has_suit(self.trick_suit):
                    card_to_play = player.choose_play(self)

                notify_players = self.player_order(player)

                for p in notify_players:
                    if card_to_play in p.knowledge["held by any"]:
                        list.remove(p.knowledge["held by any"], card_to_play)
                    elif card_to_play in p.knowledge["held by left"]:
                        list.remove(p.knowledge["held by left"], card_to_play)
                    elif card_to_play in p.knowledge["held by across"]:
                        list.remove(p.knowledge["held by across"], card_to_play)
                    elif card_to_play in p.knowledge["held by right"]:
                        list.remove(p.knowledge["held by right"], card_to_play)
                    elif card_to_play in p.knowledge["held by left or across"]:
                        list.remove(p.knowledge["held by left or across"], card_to_play)
                    elif card_to_play in p.knowledge["held by left or right"]:
                        list.remove(p.knowledge["held by left or right"], card_to_play)
                    elif card_to_play in p.knowledge["held by across or right"]:
                        list.remove(p.knowledge["held by across or right"], card_to_play)

                if (card_to_play.suit == "hearts" or card_to_play == Card("queen", "spades")) and player.knowledge["only points"] != "":
                    players_without_points = notify_players
                    players_without_points.remove(players_without_points[player.knowledge["only points"]])
                    if players_without_points[0].knowledge["only points"] == 0:
                        players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge["held by any"]
                    if players_without_points[0].knowledge["only points"] == 1:
                        players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge["held by any"]
                    if players_without_points[0].knowledge["only points"] == 2:
                        players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge["held by any"]
                    players_without_points[0].knowledge["held by any"] = []

                    if players_without_points[1].knowledge["only points"] == 0:
                        players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge["held by any"]
                    if players_without_points[1].knowledge["only points"] == 1:
                        players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge["held by any"]
                    if players_without_points[1].knowledge["only points"] == 2:
                        players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge["held by any"]
                    players_without_points[1].knowledge["held by any"] = []

                if card_to_play.suit != self.trick_suit:
                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)

                self.trick.append(card_to_play)
                player.hand.remove_card(card_to_play)
                self.played_all.append(card_to_play)
                self.played_players[player.name].append(card_to_play)

        elif self.trick_num < 13:
            trick_progress = len(self.trick) - 1
            rotation = self.player_rotation()
            last_card = self.trick[trick_progress]
            if trick_progress == 0:
                last_player = self.has_lead
            else:
                last_player = rotation[trick_progress - 1]

            notify_players = self.player_order(last_player)

            for p in notify_players:
                if last_card in p.knowledge["held by any"]:
                    list.remove(p.knowledge["held by any"], last_card)
                elif last_card in p.knowledge["held by left"]:
                    list.remove(p.knowledge["held by left"], last_card)
                elif last_card in p.knowledge["held by across"]:
                    list.remove(p.knowledge["held by across"], last_card)
                elif last_card in p.knowledge["held by right"]:
                    list.remove(p.knowledge["held by right"], last_card)
                elif last_card in p.knowledge["held by left or across"]:
                    list.remove(p.knowledge["held by left or across"], last_card)
                elif last_card in p.knowledge["held by left or right"]:
                    list.remove(p.knowledge["held by left or right"], last_card)
                elif last_card in p.knowledge["held by across or right"]:
                    list.remove(p.knowledge["held by across or right"], last_card)

            if trick_progress == 0:
                self.trick_suit = last_card.suit
                if not self.hearts_broken and last_card.suit == "hearts" and not self.has_lead.has_suit("spades") and \
                        not self.has_lead.has_suit("diamonds") and not self.has_lead.has_suit("clubs"):
                    o_players = self.player_rotation()

                    o_players[0].knowledge["right no spades"] = True
                    o_players[0].knowledge["right no diamonds"] = True
                    o_players[0].knowledge["right no clubs"] = True
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by any"] = [i for i in
                                                             o_players[0].knowledge["held by any"] if
                                                             i not in cards_to_remove]
                    o_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by left or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by left or right"] = \
                        [i for i in o_players[0].knowledge["held by left or right"]
                         if i not in cards_to_remove]
                    o_players[0].knowledge["held by left"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[0].knowledge["held by across or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[0].knowledge["held by across or right"] = \
                        [i for i in o_players[0].knowledge["held by across or right"]
                         if i not in cards_to_remove]
                    o_players[0].knowledge["held by across"].extend(cards_to_remove)

                    o_players[1].knowledge["across no clubs"] = True
                    o_players[1].knowledge["across no spades"] = True
                    o_players[1].knowledge["across no diamonds"] = True
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by any"] = \
                        [i for i in o_players[1].knowledge["held by any"] if i not in cards_to_remove]
                    o_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by left or across"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by left or across"] = \
                        [i for i in o_players[1].knowledge["held by left or across"]
                         if i not in cards_to_remove]
                    o_players[1].knowledge["held by left"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[1].knowledge["held by across or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[1].knowledge["held by across or right"] = \
                        [i for i in o_players[1].knowledge["held by across or right"]
                         if i not in cards_to_remove]
                    o_players[1].knowledge["held by right"].extend(cards_to_remove)

                    o_players[2].knowledge["left no spades"] = True
                    o_players[2].knowledge["left no diamonds"] = True
                    o_players[2].knowledge["left no clubs"] = True
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by any"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by any"] = \
                        [i for i in o_players[2].knowledge["held by any"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by left or across"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by left or across"] = \
                        [i for i in o_players[2].knowledge["held by left or across"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by across"].extend(cards_to_remove)
                    cards_to_remove = []
                    for cards in o_players[2].knowledge["held by left or right"]:
                        if cards.suit != "hearts":
                            cards_to_remove.append(cards)
                    o_players[2].knowledge["held by left or right"] = \
                        [i for i in o_players[2].knowledge["held by left or right"]
                         if i not in cards_to_remove]
                    o_players[2].knowledge["held by right"].extend(cards_to_remove)
                if (last_card.suit == "hearts" or last_card == Card("queen", "spades")) and self.has_lead.knowledge["only points"] != "":
                    players_without_points = self.player_rotation()
                    players_without_points.remove(players_without_points[self.has_lead.knowledge["only points"]])
                    if players_without_points[0].knowledge["only points"] == 0:
                        players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge[
                            "held by any"]
                    if players_without_points[0].knowledge["only points"] == 1:
                        players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge[
                            "held by any"]
                    if players_without_points[0].knowledge["only points"] == 2:
                        players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge[
                            "held by any"]
                    players_without_points[0].knowledge["held by any"] = []

                    if players_without_points[1].knowledge["only points"] == 0:
                        players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge[
                            "held by any"]
                    if players_without_points[1].knowledge["only points"] == 1:
                        players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge[
                            "held by any"]
                    if players_without_points[1].knowledge["only points"] == 2:
                        players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge[
                            "held by any"]
                    players_without_points[1].knowledge["held by any"] = []

            else:
                if (last_card.suit == "hearts" or last_card == Card("queen", "spades")) and last_player.knowledge[
                        "only points"] != "":
                    players_without_points = notify_players
                    players_without_points.remove(players_without_points[last_player.knowledge["only points"]])
                    if players_without_points[0].knowledge["only points"] == 0:
                        players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge[
                            "held by any"]
                    if players_without_points[0].knowledge["only points"] == 1:
                        players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge[
                            "held by any"]
                    if players_without_points[0].knowledge["only points"] == 2:
                        players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge[
                            "held by any"]
                    players_without_points[0].knowledge["held by any"] = []

                    if players_without_points[1].knowledge["only points"] == 0:
                        players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge[
                            "held by any"]
                    if players_without_points[1].knowledge["only points"] == 1:
                        players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge[
                            "held by any"]
                    if players_without_points[1].knowledge["only points"] == 2:
                        players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge[
                            "held by any"]
                    players_without_points[1].knowledge["held by any"] = []

                if last_card.suit != self.trick_suit:
                    if not notify_players[0].knowledge["right no " + self.trick_suit]:
                        notify_players[0].knowledge["right no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by any"] = [i for i in
                                                                      notify_players[0].knowledge["held by any"] if
                                                                      i not in cards_to_remove]
                        notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by left or right"] = \
                            [i for i in notify_players[0].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[0].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[0].knowledge["held by across or right"] = \
                            [i for i in notify_players[0].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                    if not notify_players[1].knowledge["across no " + self.trick_suit]:
                        notify_players[1].knowledge["across no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by any"] = \
                            [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by left or across"] = \
                            [i for i in notify_players[1].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[1].knowledge["held by across or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[1].knowledge["held by across or right"] = \
                            [i for i in notify_players[1].knowledge["held by across or right"]
                             if i not in cards_to_remove]
                        notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                    if not notify_players[2].knowledge["left no " + self.trick_suit]:
                        notify_players[2].knowledge["left no " + self.trick_suit] = True
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by any"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by any"] = \
                            [i for i in notify_players[2].knowledge["held by any"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or across"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or across"] = \
                            [i for i in notify_players[2].knowledge["held by left or across"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                        cards_to_remove = []
                        for cards in notify_players[2].knowledge["held by left or right"]:
                            if cards.suit == self.trick_suit:
                                cards_to_remove.append(cards)
                        notify_players[2].knowledge["held by left or right"] = \
                            [i for i in notify_players[2].knowledge["held by left or right"]
                             if i not in cards_to_remove]
                        notify_players[2].knowledge["held by right"].extend(cards_to_remove)
            if trick_progress < 3:
                for player in rotation[trick_progress:]:
                    if self.trick[0] in player.knowledge["held by any"]:
                        list.remove(player.knowledge["held by any"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left"]:
                        list.remove(player.knowledge["held by left"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by across"]:
                        list.remove(player.knowledge["held by across"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by right"]:
                        list.remove(player.knowledge["held by right"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left or across"]:
                        list.remove(player.knowledge["held by left or across"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by left or right"]:
                        list.remove(player.knowledge["held by left or right"], self.trick[0])
                    elif self.trick[0] in player.knowledge["held by across or right"]:
                        list.remove(player.knowledge["held by across or right"], self.trick[0])

                    card_to_play = player.choose_play(self)
                    while card_to_play.suit != self.trick_suit and player.has_suit(self.trick_suit):
                        card_to_play = player.choose_play(self)

                    notify_players = self.player_order(player)

                    for p in notify_players:
                        if card_to_play in p.knowledge["held by any"]:
                            list.remove(p.knowledge["held by any"], card_to_play)
                        elif card_to_play in p.knowledge["held by left"]:
                            list.remove(p.knowledge["held by left"], card_to_play)
                        elif card_to_play in p.knowledge["held by across"]:
                            list.remove(p.knowledge["held by across"], card_to_play)
                        elif card_to_play in p.knowledge["held by right"]:
                            list.remove(p.knowledge["held by right"], card_to_play)
                        elif card_to_play in p.knowledge["held by left or across"]:
                            list.remove(p.knowledge["held by left or across"], card_to_play)
                        elif card_to_play in p.knowledge["held by left or right"]:
                            list.remove(p.knowledge["held by left or right"], card_to_play)
                        elif card_to_play in p.knowledge["held by across or right"]:
                            list.remove(p.knowledge["held by across or right"], card_to_play)

                    if (card_to_play.suit == "hearts" or card_to_play == Card("queen", "spades")) and player.knowledge["only points"] != "":
                        players_without_points = notify_players
                        players_without_points.remove(players_without_points[player.knowledge["only points"]])
                        if players_without_points[0].knowledge["only points"] == 0:
                            players_without_points[0].knowledge["held by left"] = players_without_points[0].knowledge["held by any"]
                        if players_without_points[0].knowledge["only points"] == 1:
                            players_without_points[0].knowledge["held by across"] = players_without_points[0].knowledge["held by any"]
                        if players_without_points[0].knowledge["only points"] == 2:
                            players_without_points[0].knowledge["held by right"] = players_without_points[0].knowledge["held by any"]
                        players_without_points[0].knowledge["held by any"] = []

                        if players_without_points[1].knowledge["only points"] == 0:
                            players_without_points[1].knowledge["held by left"] = players_without_points[1].knowledge["held by any"]
                        if players_without_points[1].knowledge["only points"] == 1:
                            players_without_points[1].knowledge["held by across"] = players_without_points[1].knowledge["held by any"]
                        if players_without_points[1].knowledge["only points"] == 2:
                            players_without_points[1].knowledge["held by right"] = players_without_points[1].knowledge["held by any"]
                        players_without_points[1].knowledge["held by any"] = []

                    if card_to_play.suit != self.trick_suit:
                        if not notify_players[0].knowledge["right no " + self.trick_suit]:
                            notify_players[0].knowledge["right no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by any"] = [i for i in
                                                                          notify_players[0].knowledge["held by any"] if
                                                                          i not in cards_to_remove]
                            notify_players[0].knowledge["held by left or across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by left or right"] = \
                                [i for i in notify_players[0].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[0].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[0].knowledge["held by across or right"] = \
                                [i for i in notify_players[0].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[0].knowledge["held by across"].extend(cards_to_remove)
                        if not notify_players[1].knowledge["across no " + self.trick_suit]:
                            notify_players[1].knowledge["across no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by any"] = \
                                [i for i in notify_players[1].knowledge["held by any"] if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by left or across"] = \
                                [i for i in notify_players[1].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by left"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[1].knowledge["held by across or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[1].knowledge["held by across or right"] = \
                                [i for i in notify_players[1].knowledge["held by across or right"]
                                 if i not in cards_to_remove]
                            notify_players[1].knowledge["held by right"].extend(cards_to_remove)
                        if not notify_players[2].knowledge["left no " + self.trick_suit]:
                            notify_players[2].knowledge["left no " + self.trick_suit] = True
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by any"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by any"] = \
                                [i for i in notify_players[2].knowledge["held by any"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across or right"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or across"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or across"] = \
                                [i for i in notify_players[2].knowledge["held by left or across"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by across"].extend(cards_to_remove)
                            cards_to_remove = []
                            for cards in notify_players[2].knowledge["held by left or right"]:
                                if cards.suit == self.trick_suit:
                                    cards_to_remove.append(cards)
                            notify_players[2].knowledge["held by left or right"] = \
                                [i for i in notify_players[2].knowledge["held by left or right"]
                                 if i not in cards_to_remove]
                            notify_players[2].knowledge["held by right"].extend(cards_to_remove)

                    self.trick.append(card_to_play)
                    player.hand.remove_card(card_to_play)
                    self.played_all.append(card_to_play)
                    self.played_players[player.name].append(card_to_play)

        high_card = self.trick[0]
        for card in self.trick:
            if card.hearts_compare(high_card):
                high_card = card
            if card.suit == "hearts" and not self.hearts_broken:
                self.hearts_broken = True
        high_card_index = self.trick.index(high_card)
        if high_card_index == 0:
            self.has_lead.won_cards.extend(self.trick)
        if high_card_index > 0:
            other_players = self.player_rotation()
            self.has_lead = other_players[high_card_index - 1]
            self.has_lead.won_cards.extend(self.trick)
        self.trick_num += 1
        if self.trick_num == 13:
            self.complete = True
        self.trick = []
        self.trick_suit = ""

    def score_round(self):
        """Scores a completed round of hearts"""
        if self.trick_num == 13:
            for player in self.players:
                round_score = 0
                for card in player.won_cards:
                    if card.suit == "hearts":
                        player.score += 1
                        round_score += 1
                    if card.suit == "spades" and card.value == "queen":
                        player.score += 13
                        round_score += 13
                if round_score == 26:
                    player.score += -26
                    round_score += -26
                    self.has_lead = player
                    other_players = self.player_rotation()
                    for p in other_players:
                        p.score += 26
                        self.round_score[p.name] += 26
                self.round_score[player.name] += round_score
            print(self.round_score)
        else:
            print("Round is not complete")

    def score_round_np(self):
        """Scores a completed round of hearts with no printing"""
        if self.trick_num == 13:
            for player in self.players:
                round_score = 0
                for card in player.won_cards:
                    if card.suit == "hearts":
                        player.score += 1
                        round_score += 1
                    if card.suit == "spades" and card.value == "queen":
                        player.score += 13
                        round_score += 13
                if round_score == 26:
                    player.score += -26
                    round_score += -26
                    self.has_lead = player
                    other_players = self.player_rotation()
                    for p in other_players:
                        p.score += 26
                        self.round_score[p.name] += 26
                self.round_score[player.name] += round_score

    def play_round(self):
        """Plays a round of hearts"""
        if not self.passed and not self.started:
            self.start_passing()
            for trick in range(13):
                self.play_trick()
            self.score_round()
        elif self.trick_num < 13:
            for trick in range(13 - self.trick_num):
                self.play_trick()
            self.score_round()
        else:
            self.score_round()

    def play_round_np(self):
        """Plays a round of hearts with no printing"""
        if not self.passed and not self.started:
            self.start_passing_np()
            for trick in range(13):
                self.play_trick_np()
            self.score_round_np()
        else:
            for trick in range(13 - self.trick_num):
                self.play_trick()
            self.score_round()


class Hearts(HeartsRound):
    """Plays a full hearts game"""

    def __init__(self, player1, player2, player3, player4):
        """Initiates a game of hearts"""

        self.players = [player1, player2, player3, player4]
        for player in self.players:
            player.score = 0
            player.knowledge = {}

        self.game_score = {player1.name: 0, player2.name: 0, player3.name: 0, player4.name: 0}
        self.round_num = 0
        self.score_limit = 100
        self.started = False
        self.complete = False
        self.victor = ""
        self.leader = ""
        self.queens = {player1.name: 0, player2.name: 0, player3.name: 0, player4.name: 0}
        self.moonshots = {player1.name: 0, player2.name: 0, player3.name: 0, player4.name: 0}
        self.hpr = {player1.name: 0, player2.name: 0, player3.name: 0, player4.name: 0}
        self.qpr = {player1.name: 0, player2.name: 0, player3.name: 0, player4.name: 0}
        self.mpr = {player1.name: 0, player2.name: 0, player3.name: 0, player4.name: 0}
        self.ppr = {player1.name: 0, player2.name: 0, player3.name: 0, player4.name: 0}

    def single_round(self):
        """Plays a single round of a hearts game"""
        if not self.started:
            self.started = True
        if max(self.game_score.values()) < self.score_limit:
            current_round = HeartsRound(self.players[0], self.players[1], self.players[2], self.players[3],
                                        self.pass_options[self.round_num % 4])
            current_round.play_round()
            for player in self.players:
                self.game_score[player.name] = player.score

            for player in self.players:
                if player.name == min(self.game_score.keys(), key=(lambda key: self.game_score[key])):
                    self.leader = player.name
                if sum(current_round.round_score.values()) == 78 and current_round.round_score[player.name] == 0:
                    self.moonshots[player.name] += 1
                for card in player.won_cards:
                    if card == Card("queen", "spades") and sum(current_round.round_score.values()) == 26 \
                            and current_round.round_score[player.name] != 0:
                        self.queens[player.name] += 1
                self.hpr[player.name] = (player.score - 13 * self.queens[player.name]) / (self.round_num + 1)
                self.qpr[player.name] = self.queens[player.name] / (self.round_num + 1)
                self.mpr[player.name] = self.moonshots[player.name] / (self.round_num + 1)
                self.ppr[player.name] = player.score / (self.round_num + 1)

            self.round_num += 1
            print("Game score at round", self.round_num, ":", "\n", self.game_score)
            if max(self.game_score.values()) >= self.score_limit:
                self.complete = True
                self.victor = min(self.game_score.keys(), key=(lambda key: self.game_score[key]))
                print("Game is complete,", self.victor, "is the winner")

                print("Queens taken: \n", self.queens)
                print("Successful moonshots: \n", self.moonshots)
                print("Hearts received per round: \n", self.hpr)
                print("Queens taken per round: \n", self.qpr)
                print("Moonshots per round: \n", self.mpr)
                print("Points taken per round: \n", self.ppr)

        else:
            return

    def play_hearts(self):
        """Plays a game of hearts"""
        while max(self.game_score.values()) < self.score_limit:
            self.single_round()


class AIplayer(Player):
    """Defines an AI player for a game of hearts"""

    standard_deck = Deck()

    def __init__(self, name, hand, trials):
        """Initiates a player with a hand and an AI"""
        self.name = name
        self.hand = hand
        self.won_cards = []
        self.score = 0
        self.knowledge = {"held by any": [], "held by left": [], "held by across": [], "held by right": [],
                          "held by left or across": [], "held by left or right": [], "held by across or right": [],
                          "left no spades": False, "across no spades": False, "right no spades": False,
                          "left no hearts": False, "across no hearts": False, "right no hearts": False,
                          "left no diamonds": False, "across no diamonds": False, "right no diamonds": False,
                          "left no clubs": False, "across no clubs": False, "right no clubs": False, "only points": ""}

        self.ai = "program"
        self.trials = trials

    def __repr__(self):
        """Defines a representation of a player"""
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.hand == other.hand and self.won_cards == other.won_cards and \
               self.score == other.score and self.knowledge == other.knowledge and self.trials == other.trials and \
               self.ai == other.ai

    def choose_pass(self):
        """Picks three cards to pass"""
        hand = self.hand
        pass_list = []
        if self.ai == "random" or self.ai == "program":
            for i in range(3):
                card_choice = random.choice(hand.order)
                hand.remove_card(card_choice)
                pass_list.append(card_choice)
            self.hand = hand
            return pass_list
        elif self.ai == "program":
            pass
        elif self.ai == "human":
            print(hand)
            print(self.name)
            for i in range(3):
                choice_str = str(input("Choose a card from your hand to pass: "))
                card_value = ""
                card_suit = ""
                for value in hand.value_items:
                    if value in choice_str:
                        card_value = value
                for suit in hand.suits:
                    if suit in choice_str:
                        card_suit = suit
                if card_value == "" or card_suit == "":
                    print("Not a valid input - try again")
                    return self.choose_pass()

                card_choice = Card(card_value, card_suit)
                pass_list.append(card_choice)
            for choices in pass_list:
                hand.remove_card(choices)
            self.hand = hand
            return pass_list

    def play_card(self, card):
        """Compels a player to play a particular card"""
        if card in self.hand.contents:
            self.hand.remove_card(card)
            return card
        else:
            print("Card is not in hand")

    def has_suit(self, suit):
        """Indicates whether the player has a suit"""
        for cards in self.hand.order:
            if suit == cards.suit:
                return True
        return False

    def count_suit(self, suit):
        """Counts the number of cards of a suit in a players hand"""
        count = 0
        for cards in self.hand.order:
            if suit == cards.suit:
                count += 1
        return count

    def has_start(self, start_card=Card("2", "clubs")):
        """Indicates with the player has the starting card"""
        for cards in self.hand.order:
            if cards.suit == start_card.suit and cards.value == start_card.value:
                return True
        return False

    def choose_play(self, hround):
        """Picks a card to play using a monte carlo simulation"""

        trick = copy.deepcopy(hround.trick)
        trick_num = copy.deepcopy(hround.trick_num)
        hearts_broken = copy.deepcopy(hround.hearts_broken)
        play_options = self.hand.legal_moves(trick, trick_num, hearts_broken)

        virtual_round = copy.deepcopy(hround)

        if len(play_options) == 1 or virtual_round.equivalent_moves(self) or not virtual_round.points_remain or \
                virtual_round.cant_effect_outcome(self):
            return random.choice(play_options)

        ai_index = virtual_round.players.index(self)
        lead_position = virtual_round.players.index(virtual_round.has_lead)
        virtual_players = ["", "", "", ""]

        ai_player = AIplayer(virtual_round.players[ai_index].name,
                             virtual_round.players[ai_index].hand, self.trials)
        ai_player.won_cards = virtual_round.players[ai_index].won_cards[:]
        ai_player.score = virtual_round.players[ai_index].score
        ai_player.knowledge = virtual_round.players[ai_index].knowledge

        left_player = Player(virtual_round.players[(ai_index + 1) % 4].name,
                               virtual_round.players[(ai_index + 1) % 4].hand, "random")
        left_player.won_cards = virtual_round.players[(ai_index + 1) % 4].won_cards[:]
        left_player.score = virtual_round.players[(ai_index + 1) % 4].score
        left_player.knowledge = virtual_round.players[(ai_index + 1) % 4].knowledge

        across_player = Player(virtual_round.players[(ai_index + 2) % 4].name,
                                 virtual_round.players[(ai_index + 2) % 4].hand, "random")
        across_player.won_cards = virtual_round.players[(ai_index + 2) % 4].won_cards[:]
        across_player.score = virtual_round.players[(ai_index + 2) % 4].score
        across_player.knowledge = virtual_round.players[(ai_index + 2) % 4].knowledge

        right_player = Player(virtual_round.players[(ai_index + 3) % 4].name,
                                virtual_round.players[(ai_index + 3) % 4].hand, "random")
        right_player.won_cards = virtual_round.players[(ai_index + 3) % 4].won_cards[:]
        right_player.score = virtual_round.players[(ai_index + 3) % 4].score
        right_player.knowledge = virtual_round.players[(ai_index + 3) % 4].knowledge

        print(ai_player.name, "knowledge:", ai_player.knowledge)
        held_by_any = ai_player.knowledge["held by any"][:]
        held_by_left_or_across = ai_player.knowledge["held by left or across"][:]
        held_by_left_or_right = ai_player.knowledge["held by left or right"][:]
        held_by_across_or_right = ai_player.knowledge["held by across or right"][:]
        left_potential_cards = held_by_any[:]
        left_potential_cards.extend(held_by_left_or_across)
        left_potential_cards.extend(held_by_left_or_right)
        left_hand_size = len(left_player.hand.contents)
        across_hand_size = len(across_player.hand.contents)
        right_hand_size = len(right_player.hand.contents)
        left_to_pick = left_hand_size - len(ai_player.knowledge["held by left"])
        across_to_pick = across_hand_size - len(ai_player.knowledge["held by across"])
        right_to_pick = right_hand_size - len(ai_player.knowledge["held by right"])

        new_left_hand = ai_player.knowledge["held by left"][:]
        new_across_hand = ai_player.knowledge["held by across"][:]
        new_right_hand = ai_player.knowledge["held by right"][:]
        print(len(held_by_any))
        print(len(held_by_across_or_right))
        print(across_to_pick)
        print(len(held_by_left_or_across))
        print(right_to_pick)
        print(len(held_by_left_or_right))
        for x in range(left_to_pick):
            if len(held_by_any) + len(held_by_across_or_right) > across_to_pick - len(held_by_left_or_across) and \
                    len(held_by_any) + len(held_by_across_or_right) > right_to_pick - len(held_by_left_or_right):
                chosen_card = random.choice(left_potential_cards)
                new_left_hand.append(chosen_card)
                left_potential_cards.remove(chosen_card)
                if chosen_card in held_by_any:
                    held_by_any.remove(chosen_card)
                if chosen_card in held_by_left_or_across:
                    held_by_left_or_across.remove(chosen_card)
                if chosen_card in held_by_left_or_right:
                    held_by_left_or_right.remove(chosen_card)
            elif len(held_by_any) + len(held_by_across_or_right) <= across_to_pick - len(held_by_left_or_across):
                chosen_card = random.choice(held_by_left_or_right)
                new_left_hand.append(chosen_card)
                held_by_left_or_right.remove(chosen_card)
            elif len(held_by_any) + len(held_by_across_or_right) <= right_to_pick - len(held_by_left_or_right):
                chosen_card = random.choice(held_by_left_or_across)
                new_left_hand.append(chosen_card)
                left_potential_cards.remove(chosen_card)
                held_by_left_or_across.remove(chosen_card)

        left_player.hand.contents = new_left_hand[:]
        left_player.hand.order = new_left_hand[:]
        left_player.hand.arrange_contents()

        new_across_hand.extend(held_by_left_or_across)
        across_to_pick = across_to_pick - len(held_by_left_or_across)
        across_potential_cards = held_by_any[:]
        across_potential_cards.extend(held_by_across_or_right)
        if across_potential_cards != []:
            for x in range(across_to_pick):
                chosen_card = random.choice(across_potential_cards)
                new_across_hand.append(chosen_card)
                across_potential_cards.remove(chosen_card)
                if chosen_card in held_by_any:
                    held_by_any.remove(chosen_card)
                if chosen_card in held_by_across_or_right:
                    held_by_across_or_right.remove(chosen_card)

        across_player.hand.contents = new_across_hand[:]
        across_player.hand.order = new_across_hand[:]
        across_player.hand.arrange_contents()

        new_right_hand.extend(held_by_any)
        new_right_hand.extend(held_by_across_or_right)
        new_right_hand.extend(held_by_left_or_right)

        right_player.hand.contents = new_right_hand[:]
        right_player.hand.order = new_right_hand[:]
        right_player.hand.arrange_contents()




        # new_left_hand = ai_player.knowledge["held by left"][:]
        # # print("lpc:", left_potential_cards)
        # # print("left hand:", new_left_hand)
        # # if len(held_by_any) + len(held_by_across_or_right) + len(ai_player.knowledge["held by across"]) + \
        # #         len(held_by_left_or_across) <= len(across_player.hand.contents) and \
        # #         len(held_by_any) + len(held_by_left_or_right) + len(ai_player.knowledge["held by right"]) + \
        # #         len(held_by_across_or_right) <= len(right_player.hand.contents):
        # #     left_potential_cards = []
        # #
        # # elif len(held_by_any) + len(held_by_across_or_right) + len(ai_player.knowledge["held by across"]) + \
        # #         len(held_by_left_or_across) <= len(across_player.hand.contents):
        # #     left_potential_cards = held_by_left_or_right
        # #     print("blah1")
        # #
        # # elif len(held_by_any) + len(held_by_left_or_right) + len(held_by_across_or_right) + \
        # #         len(ai_player.knowledge["held by right"]) <= len(right_player.hand.contents):
        # #     print("blah2")
        # #     left_potential_cards = held_by_left_or_across
        #
        # left_hand_size = len(left_player.hand.contents) - len(new_left_hand)
        # if left_potential_cards != []:
        #     for x in range(left_hand_size):
        #         chosen_card = random.choice(left_potential_cards)
        #         new_left_hand.append(chosen_card)
        #         left_potential_cards.remove(chosen_card)
        #         if chosen_card in held_by_any:
        #             held_by_any.remove(chosen_card)
        #         if chosen_card in held_by_left_or_across:
        #             held_by_left_or_across.remove(chosen_card)
        #         if chosen_card in held_by_left_or_right:
        #             held_by_left_or_right.remove(chosen_card)
        # # left_player.hand.contents = new_left_hand[:]
        # # left_player.hand.order = new_left_hand[:]
        # # left_player.hand.arrange_contents()
        # # new_across_hand = ai_player.knowledge["held by across"][:]
        # # new_across_hand.extend(held_by_left_or_across)
        # # across_potential_cards = held_by_any[:]
        # # across_potential_cards.extend(held_by_across_or_right)
        # #
        # # if len(held_by_any) + len(held_by_across_or_right) + len(held_by_left_or_right) + \
        # #         len(ai_player.knowledge["held by right"]) <= len(right_player.hand.contents):
        # #     across_potential_cards = held_by_left_or_across
        # #     print("blah3")
        #
        #
        #
        # across_hand_size = len(across_player.hand.contents) - len(new_across_hand)
        #
        # # print("apc:", across_potential_cards)
        # # print("across hand:", new_across_hand)
        # if across_potential_cards != []:
        #     for x in range(across_hand_size):
        #         chosen_card = random.choice(across_potential_cards)
        #         new_across_hand.append(chosen_card)
        #         across_potential_cards.remove(chosen_card)
        #         if chosen_card in held_by_any:
        #             held_by_any.remove(chosen_card)
        #         if chosen_card in held_by_across_or_right:
        #             held_by_across_or_right.remove(chosen_card)
        #
        # # across_player.hand.contents = new_across_hand[:]
        # # across_player.hand.order = new_across_hand[:]
        # # across_player.hand.arrange_contents()
        # #
        # # new_right_hand = ai_player.knowledge["held by right"][:]
        # # new_right_hand.extend(held_by_any)
        # # new_right_hand.extend(held_by_across_or_right)
        # # new_right_hand.extend(held_by_left_or_right)
        # #
        # # right_player.hand.contents = new_right_hand[:]
        # # right_player.hand.order = new_right_hand[:]
        # # right_player.hand.arrange_contents()

        print(ai_player.name, len(ai_player.hand.contents), ai_player.hand.contents)
        print(left_player.name, len(left_player.hand.contents), left_player.hand.contents)
        print(across_player.name, len(across_player.hand.contents), across_player.hand.contents)
        print(right_player.name, len(right_player.hand.contents), right_player.hand.contents, "\n")

        all_cards = self.standard_deck.contents[:]

        all_cards = [i for i in all_cards if i not in virtual_round.played_all]

        left_player.knowledge["held by any"] = [i for i in all_cards if i not in left_player.hand.contents]
        left_player.knowledge["held by left or across"] = []
        left_player.knowledge["held by left or right"] = []
        left_player.knowledge["held by across or right"] = []
        left_player.knowledge["held by across"] = []
        left_player.knowledge["held by left"] = []
        left_player.knowledge["held by right"] = []

        if left_player.knowledge["left no spades"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or across"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or across"] = [i for i in
                                                               left_player.knowledge["held by left or across"]
                                                               if i not in cards_to_remove]
            left_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or right"] = [i for i in
                                                              left_player.knowledge["held by left or right"]
                                                              if i not in cards_to_remove]
            left_player.knowledge["held by right"].extend(cards_to_remove)

        if left_player.knowledge["left no hearts"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or across"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or across"] = [i for i in
                                                               left_player.knowledge["held by left or across"]
                                                               if i not in cards_to_remove]
            left_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or right"] = [i for i in
                                                              left_player.knowledge["held by left or right"]
                                                              if i not in cards_to_remove]
            left_player.knowledge["held by right"].extend(cards_to_remove)

        if left_player.knowledge["left no diamonds"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or across"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or across"] = [i for i in
                                                               left_player.knowledge["held by left or across"]
                                                               if i not in cards_to_remove]
            left_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or right"] = [i for i in
                                                              left_player.knowledge["held by left or right"]
                                                              if i not in cards_to_remove]
            left_player.knowledge["held by right"].extend(cards_to_remove)

        if left_player.knowledge["left no clubs"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or across"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or across"] = [i for i in
                                                               left_player.knowledge["held by left or across"]
                                                               if i not in cards_to_remove]
            left_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or right"] = [i for i in
                                                              left_player.knowledge["held by left or right"]
                                                              if i not in cards_to_remove]
            left_player.knowledge["held by right"].extend(cards_to_remove)

        if left_player.knowledge["across no spades"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or across"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or across"] = [i for i in
                                                               left_player.knowledge["held by left or across"]
                                                               if i not in cards_to_remove]
            left_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by across or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by across or right"] = [i for i in
                                                                left_player.knowledge["held by across or right"]
                                                                if i not in cards_to_remove]
            left_player.knowledge["held by right"].extend(cards_to_remove)

        if left_player.knowledge["across no hearts"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or across"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or across"] = [i for i in
                                                               left_player.knowledge["held by left or across"]
                                                               if i not in cards_to_remove]
            left_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by across or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by across or right"] = [i for i in
                                                                left_player.knowledge["held by across or right"]
                                                                if i not in cards_to_remove]
            left_player.knowledge["held by right"].extend(cards_to_remove)

        if left_player.knowledge["across no diamonds"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or across"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or across"] = [i for i in
                                                               left_player.knowledge["held by left or across"]
                                                               if i not in cards_to_remove]
            left_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by across or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by across or right"] = [i for i in
                                                                left_player.knowledge["held by across or right"]
                                                                if i not in cards_to_remove]
            left_player.knowledge["held by right"].extend(cards_to_remove)

        if left_player.knowledge["across no clubs"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or across"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or across"] = [i for i in
                                                               left_player.knowledge["held by left or across"]
                                                               if i not in cards_to_remove]
            left_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by across or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by across or right"] = [i for i in
                                                                left_player.knowledge["held by across or right"]
                                                                if i not in cards_to_remove]
            left_player.knowledge["held by right"].extend(cards_to_remove)

        if left_player.knowledge["right no spades"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or right"] = [i for i in
                                                              left_player.knowledge["held by left or right"]
                                                              if i not in cards_to_remove]
            left_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by across or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by across or right"] = [i for i in
                                                                left_player.knowledge["held by across or right"]
                                                                if i not in cards_to_remove]
            left_player.knowledge["held by across"].extend(cards_to_remove)

        if left_player.knowledge["right no hearts"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or right"] = [i for i in
                                                              left_player.knowledge["held by left or right"]
                                                              if i not in cards_to_remove]
            left_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by across or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by across or right"] = [i for i in
                                                                left_player.knowledge["held by across or right"]
                                                                if i not in cards_to_remove]
            left_player.knowledge["held by across"].extend(cards_to_remove)

        if left_player.knowledge["right no diamonds"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or right"] = [i for i in
                                                              left_player.knowledge["held by left or right"]
                                                              if i not in cards_to_remove]
            left_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by across or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by across or right"] = [i for i in
                                                                left_player.knowledge["held by across or right"]
                                                                if i not in cards_to_remove]
            left_player.knowledge["held by across"].extend(cards_to_remove)

        if left_player.knowledge["right no clubs"]:
            cards_to_remove = []
            for cards in left_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by any"] = [i for i in left_player.knowledge["held by any"] if i not in
                                                    cards_to_remove]
            left_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by left or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by left or right"] = [i for i in
                                                              left_player.knowledge["held by left or right"]
                                                              if i not in cards_to_remove]
            left_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in left_player.knowledge["held by across or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            left_player.knowledge["held by across or right"] = [i for i in
                                                                left_player.knowledge["held by across or right"]
                                                                if i not in cards_to_remove]
            left_player.knowledge["held by across"].extend(cards_to_remove)

        across_player.knowledge["held by any"] = [i for i in all_cards if i not in across_player.hand.contents]
        across_player.knowledge["held by left or across"] = []
        across_player.knowledge["held by left or right"] = []
        across_player.knowledge["held by across or right"] = []
        across_player.knowledge["held by left"] = []
        across_player.knowledge["held by right"] = []
        across_player.knowledge["held by across"] = []

        if across_player.knowledge["left no spades"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or across"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or across"] = [i for i in
                                                                 across_player.knowledge["held by left or across"]
                                                                 if i not in cards_to_remove]
            across_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or right"] = [i for i in
                                                                across_player.knowledge["held by left or right"]
                                                                if i not in cards_to_remove]
            across_player.knowledge["held by right"].extend(cards_to_remove)

        if across_player.knowledge["left no hearts"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not in
                                                      cards_to_remove]
            across_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or across"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or across"] = [i for i in
                                                                 across_player.knowledge["held by left or across"]
                                                                 if i not in cards_to_remove]
            across_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or right"] = [i for i in
                                                                across_player.knowledge["held by left or right"]
                                                                if i not in cards_to_remove]
            across_player.knowledge["held by right"].extend(cards_to_remove)

        if across_player.knowledge["left no diamonds"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or across"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or across"] = [i for i in
                                                                 across_player.knowledge["held by left or across"]
                                                                 if i not in cards_to_remove]
            across_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or right"] = [i for i in
                                                                across_player.knowledge["held by left or right"]
                                                                if i not in cards_to_remove]
            across_player.knowledge["held by right"].extend(cards_to_remove)

        if across_player.knowledge["left no clubs"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or across"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or across"] = [i for i in
                                                                 across_player.knowledge["held by left or across"]
                                                                 if i not in cards_to_remove]
            across_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or right"] = [i for i in
                                                                across_player.knowledge["held by left or right"]
                                                                if i not in cards_to_remove]
            across_player.knowledge["held by right"].extend(cards_to_remove)

        if across_player.knowledge["across no spades"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not in
                                                      cards_to_remove]
            across_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or across"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or across"] = [i for i in
                                                                 across_player.knowledge["held by left or across"]
                                                                 if i not in cards_to_remove]
            across_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by across or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by across or right"] = [i for i in
                                                                  across_player.knowledge["held by across or right"]
                                                                  if i not in cards_to_remove]
            across_player.knowledge["held by right"].extend(cards_to_remove)

        if across_player.knowledge["across no hearts"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or across"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or across"] = [i for i in
                                                                 across_player.knowledge["held by left or across"]
                                                                 if i not in cards_to_remove]
            across_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by across or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by across or right"] = [i for i in
                                                                  across_player.knowledge["held by across or right"]
                                                                  if i not in cards_to_remove]
            across_player.knowledge["held by right"].extend(cards_to_remove)

        if across_player.knowledge["across no diamonds"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or across"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or across"] = [i for i in
                                                                 across_player.knowledge["held by left or across"]
                                                                 if i not in cards_to_remove]
            across_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by across or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by across or right"] = [i for i in
                                                                  across_player.knowledge["held by across or right"]
                                                                  if i not in cards_to_remove]
            across_player.knowledge["held by right"].extend(cards_to_remove)

        if across_player.knowledge["across no clubs"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or across"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or across"] = [i for i in
                                                                 across_player.knowledge["held by left or across"]
                                                                 if i not in cards_to_remove]
            across_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by across or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by across or right"] = [i for i in
                                                                  across_player.knowledge["held by across or right"]
                                                                  if i not in cards_to_remove]
            across_player.knowledge["held by right"].extend(cards_to_remove)

        if across_player.knowledge["right no spades"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not in
                                                      cards_to_remove]
            across_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or right"] = [i for i in
                                                                across_player.knowledge["held by left or right"]
                                                                if i not in cards_to_remove]
            across_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by across or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by across or right"] = [i for i in
                                                                  across_player.knowledge["held by across or right"]
                                                                  if i not in cards_to_remove]
            across_player.knowledge["held by across"].extend(cards_to_remove)

        if across_player.knowledge["right no hearts"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or right"] = [i for i in
                                                                across_player.knowledge["held by left or right"]
                                                                if i not in cards_to_remove]
            across_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by across or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by across or right"] = [i for i in
                                                                  across_player.knowledge["held by across or right"]
                                                                  if i not in cards_to_remove]
            across_player.knowledge["held by across"].extend(cards_to_remove)

        if across_player.knowledge["right no diamonds"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or right"] = [i for i in
                                                                across_player.knowledge["held by left or right"]
                                                                if i not in cards_to_remove]
            across_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by across or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by across or right"] = [i for i in
                                                                  across_player.knowledge["held by across or right"]
                                                                  if i not in cards_to_remove]
            across_player.knowledge["held by across"].extend(cards_to_remove)

        if across_player.knowledge["right no clubs"]:
            cards_to_remove = []
            for cards in across_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by any"] = [i for i in across_player.knowledge["held by any"] if i not
                                                      in cards_to_remove]
            across_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by left or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by left or right"] = [i for i in
                                                                across_player.knowledge["held by left or right"]
                                                                if i not in cards_to_remove]
            across_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in across_player.knowledge["held by across or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            across_player.knowledge["held by across or right"] = [i for i in
                                                                  across_player.knowledge["held by across or right"]
                                                                  if i not in cards_to_remove]
            across_player.knowledge["held by across"].extend(cards_to_remove)

        right_player.knowledge["held by any"] = [i for i in all_cards if i not in right_player.hand.contents]
        right_player.knowledge["held by left or across"] = []
        right_player.knowledge["held by left or right"] = []
        right_player.knowledge["held by across or right"] = []
        right_player.knowledge["held by right"] = []
        right_player.knowledge["held by across"] = []
        right_player.knowledge["held by left"] = []

        if right_player.knowledge["left no spades"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or across"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or across"] = [i for i in
                                                                right_player.knowledge[
                                                                    "held by left or across"]
                                                                if i not in cards_to_remove]
            right_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or right"] = [i for i in
                                                               right_player.knowledge["held by left or right"]
                                                               if i not in cards_to_remove]
            right_player.knowledge["held by right"].extend(cards_to_remove)

        if right_player.knowledge["left no hearts"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if
                                                     i not in
                                                     cards_to_remove]
            right_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or across"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or across"] = [i for i in
                                                                right_player.knowledge[
                                                                    "held by left or across"]
                                                                if i not in cards_to_remove]
            right_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or right"] = [i for i in
                                                               right_player.knowledge["held by left or right"]
                                                               if i not in cards_to_remove]
            right_player.knowledge["held by right"].extend(cards_to_remove)

        if right_player.knowledge["left no diamonds"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or across"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or across"] = [i for i in
                                                                right_player.knowledge[
                                                                    "held by left or across"]
                                                                if i not in cards_to_remove]
            right_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or right"] = [i for i in
                                                               right_player.knowledge["held by left or right"]
                                                               if i not in cards_to_remove]
            right_player.knowledge["held by right"].extend(cards_to_remove)

        if right_player.knowledge["left no clubs"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by across or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or across"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or across"] = [i for i in
                                                                right_player.knowledge[
                                                                    "held by left or across"]
                                                                if i not in cards_to_remove]
            right_player.knowledge["held by across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or right"] = [i for i in
                                                               right_player.knowledge["held by left or right"]
                                                               if i not in cards_to_remove]
            right_player.knowledge["held by right"].extend(cards_to_remove)

        if right_player.knowledge["across no spades"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if
                                                     i not in
                                                     cards_to_remove]
            right_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or across"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or across"] = [i for i in
                                                                right_player.knowledge[
                                                                    "held by left or across"]
                                                                if i not in cards_to_remove]
            right_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by across or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by across or right"] = [i for i in
                                                                 right_player.knowledge[
                                                                     "held by across or right"]
                                                                 if i not in cards_to_remove]
            right_player.knowledge["held by right"].extend(cards_to_remove)

        if right_player.knowledge["across no hearts"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or across"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or across"] = [i for i in
                                                                right_player.knowledge[
                                                                    "held by left or across"]
                                                                if i not in cards_to_remove]
            right_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by across or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by across or right"] = [i for i in
                                                                 right_player.knowledge[
                                                                     "held by across or right"]
                                                                 if i not in cards_to_remove]
            right_player.knowledge["held by right"].extend(cards_to_remove)

        if right_player.knowledge["across no diamonds"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or across"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or across"] = [i for i in
                                                                right_player.knowledge[
                                                                    "held by left or across"]
                                                                if i not in cards_to_remove]
            right_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by across or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by across or right"] = [i for i in
                                                                 right_player.knowledge[
                                                                     "held by across or right"]
                                                                 if i not in cards_to_remove]
            right_player.knowledge["held by right"].extend(cards_to_remove)

        if right_player.knowledge["across no clubs"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by left or right"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or across"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or across"] = [i for i in
                                                                right_player.knowledge[
                                                                    "held by left or across"]
                                                                if i not in cards_to_remove]
            right_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by across or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by across or right"] = [i for i in
                                                                 right_player.knowledge[
                                                                     "held by across or right"]
                                                                 if i not in cards_to_remove]
            right_player.knowledge["held by right"].extend(cards_to_remove)

        if right_player.knowledge["right no spades"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if
                                                     i not in
                                                     cards_to_remove]
            right_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or right"] = [i for i in
                                                               right_player.knowledge["held by left or right"]
                                                               if i not in cards_to_remove]
            right_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by across or right"]:
                if cards.suit == "spades":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by across or right"] = [i for i in
                                                                 right_player.knowledge[
                                                                     "held by across or right"]
                                                                 if i not in cards_to_remove]
            right_player.knowledge["held by across"].extend(cards_to_remove)

        if right_player.knowledge["right no hearts"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or right"] = [i for i in
                                                               right_player.knowledge["held by left or right"]
                                                               if i not in cards_to_remove]
            right_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by across or right"]:
                if cards.suit == "hearts":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by across or right"] = [i for i in
                                                                 right_player.knowledge[
                                                                     "held by across or right"]
                                                                 if i not in cards_to_remove]
            right_player.knowledge["held by across"].extend(cards_to_remove)

        if right_player.knowledge["right no diamonds"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or right"] = [i for i in
                                                               right_player.knowledge["held by left or right"]
                                                               if i not in cards_to_remove]
            right_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by across or right"]:
                if cards.suit == "diamonds":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by across or right"] = [i for i in
                                                                 right_player.knowledge[
                                                                     "held by across or right"]
                                                                 if i not in cards_to_remove]
            right_player.knowledge["held by across"].extend(cards_to_remove)

        if right_player.knowledge["right no clubs"]:
            cards_to_remove = []
            for cards in right_player.knowledge["held by any"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by any"] = [i for i in right_player.knowledge["held by any"] if i not
                                                     in cards_to_remove]
            right_player.knowledge["held by left or across"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by left or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by left or right"] = [i for i in
                                                               right_player.knowledge["held by left or right"]
                                                               if i not in cards_to_remove]
            right_player.knowledge["held by left"].extend(cards_to_remove)
            cards_to_remove = []
            for cards in right_player.knowledge["held by across or right"]:
                if cards.suit == "clubs":
                    cards_to_remove.append(cards)
            right_player.knowledge["held by across or right"] = [i for i in
                                                                 right_player.knowledge[
                                                                     "held by across or right"]
                                                                 if i not in cards_to_remove]
            right_player.knowledge["held by across"].extend(cards_to_remove)

        print(ai_player.name, "knowledge:", ai_player.knowledge)
        print(left_player.name, "knowledge:", left_player.knowledge)
        print(across_player.name, "knowledge:", across_player.knowledge)
        print(right_player.name, "knowledge:", right_player.knowledge)

        virtual_players[ai_index] = ai_player
        virtual_players[(ai_index + 1) % 4] = left_player
        virtual_players[(ai_index + 2) % 4] = across_player
        virtual_players[(ai_index + 3) % 4] = right_player

        virtual_round.players = virtual_players

        virtual_round.has_lead = virtual_round.players[lead_position]

        virtual_round.played_players = {virtual_round.players[0].name:
                                            hround.played_players[hround.players[0].name],
                                        virtual_round.players[1].name:
                                            hround.played_players[hround.players[1].name],
                                        virtual_round.players[2].name:
                                            hround.played_players[hround.players[2].name],
                                        virtual_round.players[3].name:
                                            hround.played_players[hround.players[3].name]}
        virtual_round.passed_players = {virtual_round.players[0].name:
                                            hround.passed_players[hround.players[0].name],
                                        virtual_round.players[1].name:
                                            hround.passed_players[hround.players[1].name],
                                        virtual_round.players[2].name:
                                            hround.passed_players[hround.players[2].name],
                                        virtual_round.players[3].name:
                                            hround.passed_players[hround.players[3].name]}
        virtual_round.round_score = {virtual_round.players[0].name:
                                         hround.round_score[hround.players[0].name],
                                     virtual_round.players[1].name:
                                         hround.round_score[hround.players[1].name],
                                     virtual_round.players[2].name:
                                         hround.round_score[hround.players[2].name],
                                     virtual_round.players[3].name:
                                         hround.round_score[hround.players[3].name]}

        option_score = {}
        for opt in play_options:
            option_score[str(opt)] = 0
        for card in play_options:
            print(card)
            print(self.trials)
            for n in range(self.trials):

                virtual_round.trick.append(card)
                ai_player.hand.remove_card(card)
                virtual_round.played_all.append(card)
                virtual_round.played_players[ai_player.name].append(card)
                virtual_round.play_trick()
                virtual_round.play_round()

                print(virtual_round.players)
                print(ai_player)

                other_players = virtual_round.players[:]
                other_players.remove(virtual_round.players[ai_index])
                other_player_scores = [other_players[0].score, other_players[1].score, other_players[2].score]
                option_score[str(card)] += virtual_round.round_score[ai_player.name] - min(other_player_scores)

                virtual_round = copy.deepcopy(hround)

                lead_position = virtual_round.players.index(virtual_round.has_lead)
                virtual_players = ["", "", "", ""]

                ai_player = AIplayer(virtual_round.players[ai_index].name,
                                       virtual_round.players[ai_index].hand, self.trials)
                ai_player.won_cards = virtual_round.players[ai_index].won_cards[:]
                ai_player.score = virtual_round.players[ai_index].score
                ai_player.knowledge = virtual_round.players[ai_index].knowledge

                left_player = Player(virtual_round.players[(ai_index + 1) % 4].name,
                                       virtual_round.players[(ai_index + 1) % 4].hand, "random")
                left_player.won_cards = virtual_round.players[(ai_index + 1) % 4].won_cards[:]
                left_player.score = virtual_round.players[(ai_index + 1) % 4].score
                left_player.knowledge = virtual_round.players[(ai_index + 1) % 4].knowledge

                across_player = Player(virtual_round.players[(ai_index + 2) % 4].name,
                                         virtual_round.players[(ai_index + 2) % 4].hand, "random")
                across_player.won_cards = virtual_round.players[(ai_index + 2) % 4].won_cards[:]
                across_player.score = virtual_round.players[(ai_index + 2) % 4].score
                across_player.knowledge = virtual_round.players[(ai_index + 2) % 4].knowledge

                right_player = Player(virtual_round.players[(ai_index + 3) % 4].name,
                                        virtual_round.players[(ai_index + 3) % 4].hand, "random")
                right_player.won_cards = virtual_round.players[(ai_index + 3) % 4].won_cards[:]
                right_player.score = virtual_round.players[(ai_index + 3) % 4].score
                right_player.knowledge = virtual_round.players[(ai_index + 3) % 4].knowledge

        winning_play_string = min(option_score.keys(), key=(lambda key: option_score[key]))

        card_value = ""
        card_suit = ""
        for value in self.hand.value_items:
            if value in winning_play_string:
                card_value = value
        for suit in self.hand.suits:
            if suit in winning_play_string:
                card_suit = suit

        card_choice = Card(card_value, card_suit)

        return card_choice



Bob1 = AIplayer("Bob1", [], 1)
Bob2 = Player("Bob2", [], "random")
Bob3 = Player("Bob3", [], "random")
Bob4 = Player("Bob4", [], "random")

round1 = HeartsRound(Bob1, Bob2, Bob3, Bob4, "left")

round1.start_passing_np()

round1.play_trick()




#
# score_list1 = []
# score_list2 = []
# score_list3 = []
# score_list4 = []
#
# for i in range(1000):
#     Game1 = Hearts(Bob1, Bob2, Bob3, Bob4)
#
#     Game1.play_hearts()
#
#     score_list1.append(Game1.game_score["Bob1"])
#     score_list2.append(Game1.game_score["Bob2"])
#     score_list3.append(Game1.game_score["Bob3"])
#     score_list4.append(Game1.game_score["Bob4"])
#
# print(numpy.mean(score_list1))
# print(numpy.mean(score_list2))
# print(numpy.mean(score_list3))
# print(numpy.mean(score_list4))
#
# print(numpy.std(score_list1))
# print(numpy.std(score_list2))
# print(numpy.std(score_list3))
# print(numpy.std(score_list4))



# for round in range(13):
#     Round1.play_trick()
#     print(Round1.trick_num, "\n", Round1.played_players)
#     for play in Round1.players:
#         print("\n", play.won_cards)
#
# Round1.score_round()

#
# Round1.start_passing()



