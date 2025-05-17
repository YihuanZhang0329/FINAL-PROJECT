import tkinter as tk
from tkinter import messagebox

class TicTacToeController:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_turn = "X"
        self.windows = []

    def register_window(self, window):
        self.windows.append(window)

    def make_move(self, row, col, symbol):
        if self.board[row][col] != "" or self.current_turn != symbol:
            return False

        self.board[row][col] = symbol
        self.current_turn = "O" if symbol == "X" else "X"
        self.update_all_windows()
        return True

    def update_all_windows(self):
        for window in self.windows:
            window.update_board()

    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != "":
                return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] != "":
                return b[0][i]
        if b[0][0] == b[1][1] == b[2][2] != "":
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] != "":
            return b[0][2]
        return None

    def is_draw(self):
        return all(self.board[r][c] != "" for r in range(3) for c in range(3))


class LocalTicTacToeWindow:
    def __init__(self, controller, symbol):
        self.controller = controller
        self.symbol = symbol
        self.window = tk.Toplevel()
        self.window.title(f"Tic Tac Toe - You are {symbol}")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.status_label = tk.Label(self.window, text="", font="Helvetica 12")
        self.status_label.grid(row=3, columnspan=3)

        self.create_board()
        self.controller.register_window(self)
        self.update_board()

    def create_board(self):
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.window, text="", font="Helvetica 24 bold",
                                width=5, height=2,
                                command=lambda row=r, col=c: self.handle_click(row, col))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def handle_click(self, row, col):
        if self.controller.make_move(row, col, self.symbol):
            winner = self.controller.check_winner()
            if winner:
                self.show_result_dialog(f"{winner} wins!")
            elif self.controller.is_draw():
                self.show_result_dialog("It's a tie!")


    def show_result_dialog(self, result_text):
        dialog = tk.Toplevel(self.window)
        dialog.title("The game is over.")
        dialog.geometry("250x100")
        dialog.transient(self.window)
        dialog.grab_set()

        label = tk.Label(dialog, text=result_text, font=("Helvetica", 12))
        label.pack(pady=10)

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=5)

        ok_btn = tk.Button(btn_frame, text="OK", command=dialog.destroy)
        ok_btn.pack(side="left", padx=5)

        close_all_btn = tk.Button(btn_frame, text="Close all windows", command=lambda:self.close_all_windows(dialog))
        close_all_btn.pack(side="left", padx=5)

    def close_all_windows(self, dialog):
        dialog.destroy()  
        for win in self.controller.windows:
            win.window.destroy()  


    def update_board(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = self.controller.board[r][c]
                self.buttons[r][c]["state"] = (
                    "normal" if self.controller.board[r][c] == "" and
                    self.controller.current_turn == self.symbol else "disabled"
                )

        turn = self.controller.current_turn
        self.status_label.config(text=f"Now it is: {turn} ({'Your turn' if turn == self.symbol else 'Please wait'})")
