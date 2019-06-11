from appJar import gui
from random import randint
from tictactoe import TTT
from q_table import QTable
import numpy as np

app = gui("TTT", "400x400")
app.setSticky("news")
app.setStretch("both")
app.setFont(40)

game_ttt = TTT()
q_table = QTable()
q_table.load_q_table_from_file("q_table.npy")


def refresh_buttons():
    for x in range(0, 3):
        for y in range(0, 3):
            title = 3 * x + y
            if game_ttt.board[x][y] == 0:
                app.setButton(title, "")
            elif game_ttt.board[x][y] == 1:
                app.setButton(title, "X")
            elif game_ttt.board[x][y] == -1:
                app.setButton(title, "O")


def restart():
    game_ttt.restart()
    refresh_buttons()
    game_ttt.randomize_player()

    if game_ttt.player == -1:
        # ai_move_random()
        ai_move_q_table()


def ai_move_random():
    while True:
        tmp = randint(0, 8)
        x = tmp // 3
        y = tmp % 3

        if game_ttt.make_move(x, y):
            refresh_buttons()

            if game_ttt.finished:
                endgame()
            return


def ai_move_q_table():
    idx = np.argmax(q_table.get_Q(game_ttt.board, -1))
    x = int(idx // 3)
    y = int(idx % 3)

    if game_ttt.make_move(x, y):
        refresh_buttons()

        if game_ttt.finished:
            endgame()
        return


def endgame():
    message = ""
    if game_ttt.winner == 0:
        message = "Remis\nRestart?"
    elif game_ttt.winner == 1:
        message = "Twoje jest wygranko!\nRestart?"
    elif game_ttt.winner == -1:
        message = "Przegranko!\nRestart?"

    if app.yesNoBox("", message, parent=None):
        restart()


def press(button):
    x, y = int(button) // 3, int(button) % 3
    if game_ttt.make_move(x, y):
        refresh_buttons()

        if game_ttt.finished:
            endgame()
        else:
            # ai_move_random()
            ai_move_q_table()
    return


def run_game():
    for x in range(0, 3):
        for y in range(0, 3):
            title = 3 * x + y
            app.addNamedButton("", title, press, x, y)
            app.setButtonHeight(title, 10)
            app.setButtonWidth(title, 10)

    game_ttt.randomize_player()
    if game_ttt.player == -1:
        # ai_move_random()
        ai_move_q_table()

    app.go()


run_game()
