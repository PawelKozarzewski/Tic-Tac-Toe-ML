import numpy as np


q_table = np.zeros((19683, 18))


class QTable:
    def __init__(self):
        self.q_table = np.zeros((19683, 9))
        self.q_table += 0.5
        self.init()

    def init(self):
        for i in range(self.q_table.shape[0]):
            tmp = i
            for j in range(9):
                if tmp % 3 != 0:
                    self.q_table[i][j] = 0
                tmp = tmp // 3

    def get_Q(self, board, sign_to_move):
        return self.q_table[self.get_index(board, sign_to_move)]

    def get_index(self, board, sign_to_move):
        index = 0
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i][j] != 0:
                    if board[i][j] == sign_to_move:
                        index += 3 ** (3 * i + j)
                    else:
                        index += 2 * 3 ** (3 * i + j)
        return index

    def save_q_table_to_file(self, filename):
        np.save(filename, self.q_table)

    def load_q_table_from_file(self, filename):
        self.q_table = np.load(filename)
