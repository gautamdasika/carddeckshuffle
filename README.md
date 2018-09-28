# Python Flask app on Azure Web App for shuffling a deck of cards

This is a card deck shuffle app that can create, shuffle, pop, display, cut a deck of cards.

I ended up using Fisher Yates algorithm for shuffling, which takes O(n) time and O(1) in space.

A couple of other algorithms I came up with, that I considered:

1. Generating a random integer with range as deck length and removing the number at that index into a new array, updating the length.
This takes O(n) time and O(n) in space.

2. Generating a random value between 0 and 1 for each value in the list and sorting according to those random values.
This takes O(nlogn) time (for sorting) and O(1) in space.

The unit tests are in the test.py file. Each function tests each functionality of the a
Go to https://carddeckshuffle.azurewebsites.net/
The index page(/) shows all your available decks. (Initially none)
To create a deck, go to /createdeck
For the following, replace <deck_name> with the deck you want to operate on
To pop from a deck, go to /pop?deck=<deck_name>
To shuffle a deck, go to /shuffle?deck=<deck_name>
To display a deck, go to /display?deck=<deck_name>
To cut a deck, go to /cut?deck=<deck_name>

If you make an invalid request, you will get a standard 404
