# write your code here
from numpy import empty, reshape, ndarray
from itertools import combinations


class TicTacToe:
    def __init__(self, rows=3, columns=3):
        self.field = empty((rows, columns), dtype=str, order='F')
        self.rows = rows
        self.columns = columns
        self.player = None

    def current_player(self):
        return 'X' if (self.field == 'O').sum() >= (self.field == 'X').sum() else 'O'

    def start_setup(self, *setup: str):
        if not setup:
            while True:
                setup = input('Input starting field state:\n')
                if len(setup) != 9:
                    print('Incorrect length of start input')
                elif any([i not in 'XO_' for i in setup]):
                    print('Incorrect character in start input')
                else:
                    break
        self.field = reshape(list(setup), (self.columns, self.rows))
        self.field[self.field == '_'] = ' '

    def print_field(self):
        print(9 * '-')
        for i in range(self.rows):
            print('|', *self.field[i], '|', sep=' ')
        print(9 * '-')

    def evaluate_game(self):
        winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        flat_field = self.field.flatten().tolist()
        indices = tuple(i for i in range(len(flat_field)) if flat_field[i] == self.player)
        if any([i in winners for i in list(combinations(indices, 3))]):
            print(f'{self.player} wins')
            quit()
        elif ' ' not in flat_field:
            print('Draw')
            quit()
        else:
            print('Game not finished')

    def ask4move(self):
        self.player = self.current_player()
        while True:
            move = input('Enter the coordinates: ')
            if move == 'exit':
                quit()
            try:
                row_pos, col_pos = map(int, move.split(' '))
                row_pos -= 1
                col_pos -= 1

                if (row_pos > self.rows - 1) or (col_pos > self.columns - 1):
                    print(f'Coordinates should be from 1 to {self.columns}!')
                elif self.field[row_pos, col_pos] != ' ':
                    print('This cell is occupied! Choose another one!')
                else:
                    self.field[row_pos, col_pos] = self.player
                    self.print_field()
                    break
            except ValueError:
                print('You should enter numbers!')


if __name__ == '__main__':
    a = TicTacToe()
    # a.start_setup(list('_XXOO_OX_'))
    a.start_setup()
    a.print_field()
    while True:
        a.ask4move()
        a.evaluate_game()


