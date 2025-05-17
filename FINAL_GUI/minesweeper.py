import tkinter as tk
import random

class Cell(tk.Button):
    def __init__(self, master, x, y, game):
        super().__init__(master, width=2, font=('Helvetica', 12), relief='raised')
        self.master = master
        self.x = x
        self.y = y
        self.game = game
        self.is_mine = False
        self.is_open = False
        self.is_flagged = False
        self.bind("<Button-1>", self.left_click)  
        self.bind("<Button-3>", self.right_click)
        self.bind("<Control-Button-1>", self.right_click) 

    def left_click(self, event):
        if self.is_open or self.is_flagged:
            return
        if self.is_mine:
            self.config(text='💣', bg='red')
            self.game.game_over(False)
        else:
            self.reveal()
            if self.game.check_win():
                self.game.game_over(True)

    def right_click(self, event):
        if self.is_open:
            return
        if self.is_flagged:
            self.config(text='', bg='SystemButtonFace')
            self.is_flagged = False
        else:
            self.config(text='🚩', bg='lightyellow')
            self.is_flagged = True

    def reveal(self):
        if self.is_open or self.is_flagged:
            return
        self.is_open = True
        count = self.game.count_adjacent_mines(self.x, self.y)
        self.config(relief='sunken', bg='lightgrey', text=str(count) if count > 0 else '')
        if count == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        self.game.reveal_cell(self.x + dx, self.y + dy)

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        self.mines = mines
        self.window = tk.Tk()
        self.window.title("Minesweeper")

        self.cells = {}
        for x in range(width):
            for y in range(height):
                cell = Cell(self.window, x, y, self)
                cell.grid(row=y, column=x)
                self.cells[(x, y)] = cell

        self.place_mines()

    def place_mines(self):
        all_positions = list(self.cells.keys())
        for pos in random.sample(all_positions, self.mines):
            self.cells[pos].is_mine = True

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (nx, ny) in self.cells and self.cells[(nx, ny)].is_mine:
                    count += 1
        return count

    def reveal_cell(self, x, y):
        if (x, y) in self.cells:
            self.cells[(x, y)].reveal()

    def game_over(self, win):
        for cell in self.cells.values():
            if cell.is_mine:
                cell.config(text='💣', bg='red')
        msg = "You Win!" if win else "Game Over!"
        result = tk.Label(self.window, text=msg, font=('Helvetica', 14), fg='green' if win else 'red')
        result.grid(row=self.height, column=0, columnspan=self.width)

    def check_win(self):
        for cell in self.cells.values():
            if not cell.is_mine and not cell.is_open:
                return False
        return True

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Minesweeper()
    game.run()
