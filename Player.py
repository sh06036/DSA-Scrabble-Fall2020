class Player:
    "Creates a new player. Initializes the player's rack, and allows to set a player name."

    def __init__(self, bag):
        #Intializes a new player. Creates the player's rack by creating an instance from the previously created class.
        #Takes the bag as an argument, in order to create the rack.
        self.name = ""
        self.rack = Rack(bag)
        self.score = 0

    def set_name(self, name):
        #Sets the player's name.
        self.name = name

    def get_name(self):
        #Gets the player's name.
        return self.name

    def get_rack_str(self):
        #Returns the player's rack.
        return self.rack.get_rack_str()

    def get_rack_arr(self):
        #Returns the player's rack in the form of an array.
        return self.rack.get_rack_arr()

    def increase_score(self, increase):
        #Increases the player's score by a certain amount, according to the tiles played and word created.
        #Takes the gained score(int) as an argument and adds it to the score.
        self.score += increase

    def get_score(self):
        #Returns the player's updated score
        return self.score
