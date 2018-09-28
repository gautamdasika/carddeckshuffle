from application import app
import unittest, flask
from math import floor

class FlaskTestCase(unittest.TestCase):

    # Ensure that home page loads correctly
    def test_index_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Welcome to deck of cards' in response.data)

    # Ensure that display page loads correctly
    def test_display_loads(self):
        with app.test_client() as c:
            c.get('/createdeck')
            rv = c.get('/display?deck=deck1')
            self.assertEqual(rv.status_code, 200)
            assert 'decks' in flask.session
            assert 'deck1' in flask.session['decks']
            assert 'current_deck' in flask.session['decks']['deck1']
            assert 'dealt_cards' in flask.session['decks']['deck1']
            assert len(flask.session['decks']['deck1']['current_deck']) == 52
            assert len(flask.session['decks']['deck1']['dealt_cards']) == 0
            assert b'deck name' in rv.data
            assert b'cards' in rv.data
            assert b'dealt cards' in rv.data

    # Ensure that create deck loads correctly
    def test_create_deck_loads(self):
        with app.test_client() as c:
            rv = c.get('/createdeck')
            self.assertEqual(rv.status_code, 200)
            assert 'decks' in flask.session
            assert 'deck1' in flask.session['decks']
            assert 'current_deck' in flask.session['decks']['deck1']
            assert 'dealt_cards' in flask.session['decks']['deck1']
            assert len(flask.session['decks']['deck1']['current_deck']) == 52
            assert len(flask.session['decks']['deck1']['dealt_cards']) == 0
            assert b'deck name' in rv.data
            assert b'cards' in rv.data
            assert b'dealt cards' in rv.data

    # Ensure that pop deck loads correctly
    def test_pop_deck_loads(self):
        with app.test_client() as c:
            c.get('/createdeck')
            rv = c.get('/pop?deck=deck1')
            self.assertEqual(rv.status_code, 200)
            assert len(flask.session['decks']['deck1']['current_deck']) == 51
            assert len(flask.session['decks']['deck1']['dealt_cards']) == 1
            assert b'deck name' in rv.data
            assert b'cards' in rv.data
            assert b'dealt cards' in rv.data


    # Ensure that shuffle deck loads correctly
    def test_shuffle_deck_loads(self):
        with app.test_client() as c:
            ru = c.get('/createdeck')
            old_deck = flask.session['decks']['deck1']['current_deck']
            rv = c.get('/shuffle?deck=deck1')
            self.assertEqual(rv.status_code, 200)
            new_deck = flask.session['decks']['deck1']['current_deck']
            assert old_deck != new_deck
            assert len(flask.session['decks']['deck1']['current_deck']) == 52
            assert len(flask.session['decks']['deck1']['dealt_cards']) == 0
            assert b'deck name' in rv.data
            assert b'cards' in rv.data
            assert b'dealt cards' in rv.data

    # Ensure that cut deck loads correctly
    def test_cut_deck_loads(self):
        with app.test_client() as c:
            ru = c.get('/createdeck')
            old_deck = flask.session['decks']['deck1']['current_deck']
            rv = c.get('/cut?deck=deck1')
            self.assertEqual(rv.status_code, 200)
            new_deck = flask.session['decks']['deck1']['current_deck']
            assert old_deck != new_deck
            assert old_deck[:floor(len(old_deck)/2)] == new_deck[floor(len(old_deck)/2):]
            assert new_deck[:floor(len(old_deck)/2)] == old_deck[floor(len(old_deck)/2):]
            assert len(flask.session['decks']['deck1']['current_deck']) == 52
            assert len(flask.session['decks']['deck1']['dealt_cards']) == 0
            assert b'deck name' in rv.data
            assert b'cards' in rv.data
            assert b'dealt cards' in rv.data

if __name__ == '__main__':
    unittest.main()