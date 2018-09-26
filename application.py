from flask import Flask
app = Flask(__name__)
deck = list(itertools.product(range(1,14),['Spade','Heart','Diamond','Club']))
@app.route("/")
def hello():
    return "Hello Azure!"

@app.route("/getcards")
def hello():
    return [card for card in deck]