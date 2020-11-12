  
from random import shuffle

"""
Scrabble Game
Classes:
Tile - keeps track of the tile letter and value
Rack - keeps track of the tiles in a player's rack
Bag - keeps track of the tiles remaining in the bag
Word - checks the validity of a word and its placement
Board - keeps track of the tiles location on the board
"""

#Keeps track of the value of each letter-tile.
LETTER_VALUES = {"A": 1,
                 "B": 3,
                 "C": 3,
                 "D": 2,
                 "E": 1,
                 "F": 4,
                 "G": 2,
                 "H": 4,
                 "I": 1,
                 "J": 1,
                 "K": 5,
                 "L": 1,
                 "M": 3,
                 "N": 1,
                 "O": 1,
                 "P": 3,
                 "Q": 10,
                 "R": 1,
                 "S": 1,
                 "T": 1,
                 "U": 1,
                 "V": 4,
                 "W": 4,
                 "X": 8,
                 "Y": 4,
                 "Z": 10,
                 "#": 0}


class Tile:
    """
    Class that allows for the creation of a tile. Initializes using an uppercase string of one letter,
    and an integer representing that letter's score.
    """
    def __init__(self, letter, letter_values):
        #Initializes the tile class. Takes the letter as a string, and the dictionary of letter values as arguments.
        self.letter = letter.upper()
        if self.letter in letter_values:
            self.score = letter_values[self.letter]
        else:
            self.score = 0

    def get_letter(self):
        #Returns the tile's letter (string).
        return self.letter

    def get_score(self):
        #Returns the tile's score value.
        return self.score

class Bag:
    """
    Creates the bag of all tiles that will be available during the game. Contains 98 letters and two blank tiles.
    Takes no arguments to initialize.
    """
    def __init__(self):
        #Creates the bag full of game tiles, and calls the initialize_bag() method, which adds the default 100 tiles to the bag.
        #Takes no arguments.
        self.bag = []
        self.initialize_bag()

    def add_to_bag(self, tile, quantity):
        #Adds a certain quantity of a certain tile to the bag. Takes a tile and an integer quantity as arguments.
        for i in range(quantity):
            self.bag.append(tile)

    def initialize_bag(self):
        #Adds the intiial 100 tiles to the bag.
        global LETTER_VALUES
        self.add_to_bag(Tile("A", LETTER_VALUES), 9)
        self.add_to_bag(Tile("B", LETTER_VALUES), 2)
        self.add_to_bag(Tile("C", LETTER_VALUES), 2)
        self.add_to_bag(Tile("D", LETTER_VALUES), 4)
        self.add_to_bag(Tile("E", LETTER_VALUES), 12)
        self.add_to_bag(Tile("F", LETTER_VALUES), 2)
        self.add_to_bag(Tile("G", LETTER_VALUES), 3)
        self.add_to_bag(Tile("H", LETTER_VALUES), 2)
        self.add_to_bag(Tile("I", LETTER_VALUES), 9)
        self.add_to_bag(Tile("J", LETTER_VALUES), 9)
        self.add_to_bag(Tile("K", LETTER_VALUES), 1)
        self.add_to_bag(Tile("L", LETTER_VALUES), 4)
        self.add_to_bag(Tile("M", LETTER_VALUES), 2)
        self.add_to_bag(Tile("N", LETTER_VALUES), 6)
        self.add_to_bag(Tile("O", LETTER_VALUES), 8)
        self.add_to_bag(Tile("P", LETTER_VALUES), 2)
        self.add_to_bag(Tile("Q", LETTER_VALUES), 1)
        self.add_to_bag(Tile("R", LETTER_VALUES), 6)
        self.add_to_bag(Tile("S", LETTER_VALUES), 4)
        self.add_to_bag(Tile("T", LETTER_VALUES), 6)
        self.add_to_bag(Tile("U", LETTER_VALUES), 4)
        self.add_to_bag(Tile("V", LETTER_VALUES), 2)
        self.add_to_bag(Tile("W", LETTER_VALUES), 2)
        self.add_to_bag(Tile("X", LETTER_VALUES), 1)
        self.add_to_bag(Tile("Y", LETTER_VALUES), 2)
        self.add_to_bag(Tile("Z", LETTER_VALUES), 1)
        self.add_to_bag(Tile("#", LETTER_VALUES), 2)
        shuffle(self.bag)

    def take_from_bag(self):
        #Removes a tile from the bag and returns it to the user. This is used for replenishing the rack.
        return self.bag.pop()

    def get_remaining_tiles(self):
        #Returns the number of tiles left in the bag.
        return len(self.bag)
