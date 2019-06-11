import numpy as np


class TTT:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.player = 0
        self.winner = 0
        self.finished = False

    def randomize_player(self):
        who_starts = np.random.rand()
        if who_starts <= 0.5:
            self.player = 1
        else:
            self.player = -1

    def restart(self):
        self.board = np.zeros((3, 3))
        self.randomize_player()
        self.winner = 0
        self.finished = False

    def check_victory(self):

        for i in range(0, 3):
            row = np.sum(self.board[i, :])
            col = np.sum(self.board[:, i])
            diag_1 = np.sum(np.diagonal(self.board))
            diag_2 = np.sum(np.diagonal(np.fliplr(self.board)))

            if row==3 or col==3 or diag_1==3 or diag_2==3:
                self.winner = 1
                return True

            if row==-3 or col==-3 or diag_1==-3 or diag_2==-3:
                self.winner = -1
                return True

        if np.prod(self.board) == 0:
            return False
        else:
            return True

    def make_move(self, x, y):
        if self.winner == 0:
            if self.board[x][y] == 0:
                self.board[x][y] = self.player
                self.player *= -1

                if self.check_victory():
                    self.finished = True
                return True
        return False
