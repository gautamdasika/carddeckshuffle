from flask import Flask, session, abort, request
import random
from math import floor
app = Flask(__name__)
app.secret_key = "super secret key"

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def show(self):
        if self.value == 1:
            val = "Ace"
        elif self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"
        else:
            val = self.value

        return "{} of {}".format(val, self.suit)

class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        return [card.show() for card in self.cards]


    # Generate 52 cards
    def build(self):
        self.cards = []
        for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in range(1, 14):
                self.cards.append(Card(suit, val))

    def serialize(self):
        return {
            'cards': [card.serialize() for card in self.cards]
        }


@app.route("/")
def hello():
    decks = ""
    if 'decks' in session:
        decks = str(list(session['decks'].keys()))
    return decks+"<br/><br/>Welcome to deck of cards. To create a deck, go to /createdeck. To pop, cut, shuffle or display a deck, go to /(task)?deck=(deck_name)."
@app.route("/createdeck")
def createDeck():
    deck = Deck()
    if 'deck_num' not in session:
        session['deck_num'] = 0

    if 'decks' not in session:
        session['decks'] = {}
    deck_name = "deck"+str(session['deck_num']+1)
    session['deck_num'] += 1
    session['decks'][deck_name] = {}
    session['decks'][deck_name]['current_deck'] = deck.show()
    session['decks'][deck_name]['dealt_cards']=[]
    return "'deck name' : {}, <br/><br/>'cards':{},<br/><br/> 'dealt cards': {}".format(deck_name, session['decks'][deck_name]['current_deck'],session['decks'][deck_name]['dealt_cards'])

@app.route("/shuffle")
def shuffle():
    deck_name = request.args.get('deck')
    decks = session['decks']
    cards = decks[deck_name]['current_deck']
    if cards is None:
        abort(404)
    for i in range(len(cards) - 1, 0, -1):
        randi = random.randint(0, i)
        if i == randi:
            continue
        cards[i], cards[randi] = cards[randi], cards[i]
    decks[deck_name]['current_deck'] = cards
    session.pop('decks')
    session['decks'] = decks
    return "'deck name' : {}, <br/><br/>'cards':{},<br/><br/> 'dealt cards': {}".format(deck_name, session['decks'][deck_name]['current_deck'],session['decks'][deck_name]['dealt_cards'])

@app.route("/pop")
def pop():
    deck_name = request.args.get('deck')
    if 'decks' not in session:
        abort(404)
    decks = session['decks']
    cards = decks[deck_name]['current_deck']
    dealt_cards = decks[deck_name]['dealt_cards']
    popped_card = cards.pop(0)
    decks[deck_name]['current_deck'] = cards
    dealt_cards.append(popped_card)
    decks[deck_name]['dealt_cards'] = dealt_cards
    session.pop('decks')
    session['decks'] = decks
    return "'deck name' : {}, <br/><br/>'cards':{},<br/><br/> 'dealt cards': {}".format(deck_name, session['decks'][deck_name]['current_deck'],session['decks'][deck_name]['dealt_cards'])

@app.route("/cut")
def cut():
    deck_name = request.args.get('deck')
    if 'decks' not in session:
        abort(404)
    decks = session['decks']
    cards = decks[deck_name]['current_deck']
    if len(cards) > 1:
        sep_pt = floor(len(cards)/2)
        cut_cards = cards[sep_pt:]
        cut_cards.extend(cards[0:sep_pt])
        decks[deck_name]['current_deck'] = cut_cards
        session.pop('decks')
        session['decks'] = decks
    return "'deck name' : {}, <br/><br/>'cards':{},<br/><br/> 'dealt cards': {}".format(deck_name, session['decks'][deck_name]['current_deck'],session['decks'][deck_name]['dealt_cards'])

@app.route("/display")
def display():
    deck_name = request.args.get('deck')
    return "'deck name' : {}, <br/><br/>'cards':{},<br/><br/> 'dealt cards': {}".format(deck_name, session['decks'][deck_name]['current_deck'],session['decks'][deck_name]['dealt_cards'])