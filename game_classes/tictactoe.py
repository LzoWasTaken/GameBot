class TicTacToe:
    """Blueprint for a tic tac toe game."""
    possible_wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)) # If 3 of a piece land in order of any of the tuples, then the respective player wins 
    def __init__(self, player1, player2):
        # if the player tries to play with themselves
        if player1 == player2:
            raise Exception("You cannot play against yourself.")
        # The ":word:" is what is needed to create emojis in discord
        self.player1 = {"User": player1, "Piece": ":x:"}
        self.player2 = {"User": player2, "Piece": ":o:"}
        self.active_player = self.player1 # Set first as self.player1 because player for the first game will be player 1.
        self.board = [":one:", ":two:", ":three:",
                      ":four:", ":five:", ":six:",
                      ":seven:", ":eight:", ":nine:"]

    def display_board(self):
        """Returns the board in a 'tictactoeish' format."""
        return f"""
               {self.board[0]} {self.board[1]} {self.board[2]}
               {self.board[3]} {self.board[4]} {self.board[5]}
               {self.board[6]} {self.board[7]} {self.board[8]}"""

    def check_wins(self):
        """Checks the board for possible wins. If there is a win, then True is returned"""
        for spot1, spot2, spot3 in TicTacToe.possible_wins:
            if self.board[spot1] == self.active_player["Piece"] and self.board[spot2] == self.active_player["Piece"] and self.board[spot3] == self.active_player["Piece"]:
                return True # Maybe return false too?

    def modify_board(self, spot):
        """Will modify or will not modify the board based on whether or not the supplied spot is taken """
        spot -= 1 # This subtracts spot by one because list indexes start at 0.

        # Check if the spot chosen is out of range
        if spot > len(self.board) or spot < 0:
            raise Exception("The spot you have chosen is out of range")

        # Make sure that the spot is not already taken
        if self.board[spot] in [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]:
            self.board[spot] = self.active_player["Piece"]
        else:
            raise Exception("The spot that you have chosen is taken")


    def change_active_player(self):
        """Changes the active player."""
        if self.active_player == self.player1:
            self.active_player = self.player2
        elif self.active_player == self.player2:
            self.active_player = self.player1
