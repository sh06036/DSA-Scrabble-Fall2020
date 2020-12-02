class Word:
    def __init__(self, word, location, player, direction, board):
        self.word = word.upper()
        self.location = location
        self.player = player
        self.direction = direction.lower()
        self.board = board

    def check_word(self):
        #Checks validity of the word by comparing it to the list in the dic.txt file, and that the location falls within bounds.
        #Also controls the overlapping of words.
        global round_number, players
        word_score = 0
        global dictionary 
        if "dictionary" not in globals():
            dictionary = open("dic.txt").read().splitlines()

        current_board_ltr = ""
        needed_tiles = ""
        blank_tile_val = ""

        #Assuming that the player is not skipping the turn:
        if self.word != "":

            #Allows for players to declare the value of a blank tile.
            if "#" in self.word:
                while len(blank_tile_val) != 1:
                    blank_tile_val = input("Enter the letter that you want to appoint to the blank tile: ")
                self.word = self.word[:word.index("#")] + blank_tile_val.upper() + self.word[(word.index("#")+1):]

            #Reads in the board's current values where the word that is being played will go. Gives an error if the position is invalid.
            if self.direction == "right":
                for i in range(len(self.word)):
                    if self.board[self.location[0]][self.location[1]+i][1] == " " or self.board[self.location[0]][self.location[1]+i] == "TLS" or self.board[self.location[0]][self.location[1]+i] == "TWS" or self.board[self.location[0]][self.location[1]+i] == "DLS" or self.board[self.location[0]][self.location[1]+i] == "DWS" or self.board[self.location[0]][self.location[1]+i][1] == "*":
                        current_board_ltr += " "
                    else:
                        current_board_ltr += self.board[self.location[0]][self.location[1]+i][1]
            elif self.direction == "down":
                for i in range(len(self.word)):
                    if self.board[self.location[0]+i][self.location[1]] == "   " or self.board[self.location[0]+i][self.location[1]] == "TLS" or self.board[self.location[0]+i][self.location[1]] == "TWS" or self.board[self.location[0]+i][self.location[1]] == "DLS" or self.board[self.location[0]+i][self.location[1]] == "DWS" or self.board[self.location[0]+i][self.location[1]] == " * ":
                        current_board_ltr += " "
                    else:
                        current_board_ltr += self.board[self.location[0]+i][self.location[1]][1]
            else:
                return "Error: please enter a valid direction."

            #Gives an error if the word being played is not in the scrabble dictionary (dic.txt).
            if self.word not in dictionary:
                return "Please enter a valid word.\n"

            #Ensures that the words overlap correctly. If there are conflicting letters it gives an error.
            for i in range(len(self.word)):
                if current_board_ltr[i] == " ":
                    needed_tiles += self.word[i]
                elif current_board_ltr[i] != self.word[i]:
                    print("Current_board_ltr: " + str(current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                    return "The letters don't overlap, Please choose another word or Re-enter the word position."

            #If there is a blank tile, remove it's given value from the tiles needed to play the word.
            if blank_tile_val != "":
                needed_tiles = needed_tiles[needed_tiles.index(blank_tile_val):] + needed_tiles[:needed_tiles.index(blank_tile_val)]

            #Ensures that the word will be connected to other words on the playing board.
            if (round_number != 1 or (round_number == 1 and players[0] != self.player)) and current_board_ltr == " " * len(self.word):
                print("Current_board_ltr: " + str(current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                return "The word is not connected to a previously played word. Please try again."

            #Gives an error, if the availability check, of the letter tiles in the player rack, fails..
            for letter in needed_tiles:
                if letter not in self.player.get_rack_str() or self.player.get_rack_str().count(letter) < needed_tiles.count(letter):
                    return "You don't have the letter tiles for this word\n"

            #Gives an error if the location of the word is out of bounds.
            if self.location[0] > 14 or self.location[1] > 14 or self.location[0] < 0 or self.location[1] < 0 or (self.direction == "down" and (self.location[0]+len(self.word)-1) > 14) or (self.direction == "right" and (self.location[1]+len(self.word)-1) > 14):
                return "Word location is out of bounds.\n"

            #Ensures that the first letter of the word played is placed at the center of the board (7,7).
            if round_number == 1 and players[0] == self.player and self.location != [7,7]:
                return "The first letter must begin at location (7, 7).\n"
            return True

        #If the player skips their turn, confirm. If the player replies with "Y", skip the player's turn. Otherwise, allow the player to continue.
        else:
            if input("Are you sure you would like to skip your turn? (y/n)").upper() == "Y":
                if round_number == 1 and players[0] == self.player:
                    return "You can't skip the first turn."
                return True
            else:
                return "Please enter a word."

    def calculate_word_score(self):
        #Calculates the score of the word played, while considering the points of the premium-points squares.
        global LETTER_VALUES, premium_spots
        word_score = 0
        for letter in self.word:
            for spot in premium_spots:
                if letter == spot[0]:
                    if spot[1] == "TLS":
                        word_score += LETTER_VALUES[letter] * 2
                    elif spot[1] == "DLS":
                        word_score += LETTER_VALUES[letter]
            word_score += LETTER_VALUES[letter]
        for spot in premium_spots:
            if spot[1] == "TWS":
                word_score *= 3
            elif spot[1] == "DWS":
                word_score *= 2
        self.player.increase_score(word_score)

    def set_word(self, word):
        self.word = word.upper()

    def set_location(self, location):
        self.location = location

    def set_direction(self, direction):
        self.direction = direction

    def get_word(self):
        return self.word

def turn(player, board, bag):
    #Begins a turn, by displaying the game board, getting the information to play a turn, and creates a recursive loop to allow the next person to play.
    global round_number, players, skipped_turns

    #If the number of skipped turns is less than 6 in a row, and there are tiles in the bag, or no players have run out of tiles, play the turn.
    #Otherwise, end the game.	

    if (skipped_turns < 6) or (player.rack.get_rack_length() == 0 and bag.get_remaining_tiles() == 0):

        #Displays whose turn it is, the current board, and the player's rack.
        print("\nRound " + str(round_number) + ": " + player.get_name() + "'s turn \n")
        print(board.get_board())
        print("\n" + player.get_name() + "'s Rack: " + player.get_rack_str())

        #Gets information in order to play a word.
        word_to_play = input("Word to Play: ")
        location = []
        col = input("Column Number: ")
        row = input("Row Number: ")
        if (col == "" or row == "") or (col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
            location = [-1, -1]
        else:
            location = [int(row), int(col)]
        direction = input("Direction of Word to place (right or down): ")

        word = Word(word_to_play, location, player, direction, board.board_array())

        #If the first word throws an error, creates a recursive loop until the information is given correctly.
        checked = word.check_word()
        while checked != True:
            print(checked)
            word_to_play = input("Word to Play: ")
            word.set_word(word_to_play)
            location = []
            col = input("Column Number: ")
            row = input("Row Number: ")
            if (col == "" or row == "") or (col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
                location = [-1, -1]
            else:
                word.set_location([int(row), int(col)])
                location = [int(row), int(col)]
            direction = input("Direction of word to place (right or down): ")
            word.set_direction(direction)
            checked = word.check_word()

        #If the player has confirmed that they would like to skip their turn, skip it.
        #Otherwise, play the word and display on the board.

        if word.get_word() == "":
            print("Turn skipped successfully.")
            skipped_turns += 1
        else:
            board.place_word(word_to_play, location, direction, player)
            word.calculate_word_score()
            skipped_turns = 0

        #Prints the current player's score
        print("\n" + player.get_name() + "'s score is: " + str(player.get_score()))

        #Gets the next player.
        if players.index(player) != (len(players)-1):
            player = players[players.index(player)+1]
        else:
            player = players[0]
            round_number += 1

        #Recursively calls the function in order to play the next turn.
        turn(player, board, bag)

    #If the number of skipped turns has crossed 6 or the bag and the player is out of tiles, end the game
    else:
        end_game()

def start_game():
    #Begins the game and calls the turn function.
    global round_number, players, skipped_turns
    board = Board()
    bag = Bag()

    #Asks the player for the number of players.
    num_of_players = int(input("\nEnter the number of players (2-4): "))
    while num_of_players < 2 or num_of_players > 4:
        num_of_players = int(input("This number is invalid. Please enter again: "))

    #Welcomes players to the game and allows players to enter their name.
    print("\nWelcome to Scrabble! Please enter the names of the players below.")
    print("\nMake sure you have read all rules listed below:")
    print("\nYou will be displayed a 7 Tile rack to chose your word from.")
    print("\nFor the first turn. The first letter of the word played should be on 7,7.")
    print("\nAfter the first turn, all words must have at least one letter that interlocks with previous words.")
    print("\nIf there are no words that you can think to create using your current tile rack, simply submit a blank word.")
    print("\nThe game ends if 6 collective turns have been skipped, or the bag and player runs out of tiles.") 
    players = []
    for i in range(num_of_players):
        players.append(Player(bag))
        players[i].set_name(input("Please enter player " + str(i+1) + "'s name: "))

    #Sets the default value of global variables.
    round_number = 1
    skipped_turns = 0
    current_player = players[0]
    turn(current_player, board, bag)

def end_game():
    #Forces the game to end when the bag runs out of tiles.
    global players
    highest_score = 0
    winning_player = ""
    for player in players:
        if player.get_score > highest_score:
            highest_score = player.get_score()
            winning_player = player.get_name()
    print("Game Over !!!! " + winning_player + ", wins!")

    if input("\nWould you like to play again? (y/n)").upper() == "Y":
        start_game()

start_game()

