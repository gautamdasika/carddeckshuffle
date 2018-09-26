from flask import Flask
import itertools
app = Flask(__name__)
deck = list(itertools.product(range(1,14),['Spade','Heart','Diamond','Club']))
@app.route("/")
def hello():
    return "Hello Azure!"

@app.route("/getcards")
def getCards():
    return [card for card in deck]