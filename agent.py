import numpy as np


def print_board(board):
    for i in range(3):
        line = ''
        for j in range(3):
            if board[i][j] == 0:
                line += ' _'
            else:
                if board[i][j] == 1:
                    line += ' X'
                else:
                    line += ' O'
        print(line)


class SelfPlay:
    def __init__(self):
        self.epsilon = 0.8
        self.gamma = 1
        self.alfa = 0.2
        self.verbose = False

    def play_game(self, table):
        moves = []
        board = np.zeros((3, 3))
        sign = 2 * np.random.randint(0, 2) - 1
        while not self.is_game_over(board):
            # if self.verbose:
            #     print()
            #     print()
            #     print_board(board)
            if np.random.rand() < self.epsilon:
                q = table.get_Q(board, sign)
                x, y = self.get_best_move_index(board, q)
                # print('exploit move')
            else:
                x, y = self.get_random_move(board)
                # print('explore move')
            moves.append((x, y, sign))
            if board[x][y] != 0:
                print(x, y, sign)
                print_board(board)
                raise ValueError
            board[x][y] = sign
            sign = -sign

        winner = self.get_who_wins(board)

        for i in range(len(moves) - 1, -1, -1):

            reward, next_q = 0, 0
            if i == len(moves) - 1:
                if winner == 0:
                    reward = 0.5
                else:
                    if winner == moves[len(moves) - 1][2]:
                        reward = 1.0
                    else:
                        reward = 0.0
            else:
                next_q = 1 - np.max(table.get_Q(board, -moves[i][2]))
            board[moves[i][0]][moves[i][1]] = 0
            if self.verbose:
                print('now moving', moves[i][2])
                print_board(board)
            index = table.get_index(board, moves[i][2])

            move_index = 3 * moves[i][0] + moves[i][1]
            target = reward + self.gamma * next_q

            table.q_table[index][move_index] = (1.0 - self.alfa) * table.q_table[index][move_index] + self.alfa * target
            if self.verbose:
                print(i, reward, next_q)
                print(table.q_table[index])
                print()

    def get_random_move(self, board):
        best_possible_moves = []
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i][j] == 0:
                    best_possible_moves.append((i, j))

        tmp = np.random.randint(0, len(best_possible_moves))
        return best_possible_moves[tmp]

    def get_best_move_index(self, board, q_values):
        mask = np.abs(np.reshape(board, 9))
        tmp_q = (1 - mask) * q_values - mask
        max_v = np.max(tmp_q)
        # if self.verbose:
        #     print('printing Q')
        #     print(np.round(np.reshape(tmp_q, (3, 3)), 2))

        best_possible_moves = []
        for i in range(tmp_q.shape[0]):
            if tmp_q[i] == max_v:
                best_possible_moves.append(i)

        tmp = np.random.randint(0, len(best_possible_moves))
        x = best_possible_moves[tmp] // 3
        y = best_possible_moves[tmp] % 3
        return x, y

    def get_who_wins(self, board):
        for i in range(0, 3):
            row = np.sum(board[i, :])
            col = np.sum(board[:, i])
            diag_1 = np.sum(np.diagonal(board))
            diag_2 = np.sum(np.diagonal(np.fliplr(board)))

            if row == 3 or col == 3 or diag_1 == 3 or diag_2 == 3:
                return 1

            if row == -3 or col == -3 or diag_1 == -3 or diag_2 == -3:
                return -1
        return 0

    def is_game_over(self, board):
        winner = self.get_who_wins(board)
        if winner == 0:
            if np.sum(np.abs(board)) == 9:
                return True
            else:
                return False
        else:
            return True


from q_table import QTable

table = QTable()
game = SelfPlay()
game.verbose = False
game.epsilon = 0.8
for k in range(50000):
    game.play_game(table)
    print(k)
table.save_q_table_to_file('q_table.npy')

game.verbose = True
game.epsilon = 1
# table.load_q_table_from_file('q_table.npy')
game.play_game(table)

board = np.array(
    [[-1, 1, 0],
     [1, 0, -1],
     [-1, 1, 0]])

print_board(board)
print(table.get_Q(board, 1))
