class TicTacToe:
    def __init__(self):
        self.board = [' ']*9
        self.player = 'X'
        self.winner = None

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.player
            if self.player == 'X':
                self.player = 'O'
            else:
                self.player = 'X'
            self.check_winner()

    def check_winner(self):
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for pos in winning_positions:
            if self.board[pos[0]] == self.board[pos[1]] == self.board[pos[2]] != ' ':
                self.winner = self.board[pos[0]]
                return

    def game_over(self):
        return self.winner is not None or ' ' not in self.board
