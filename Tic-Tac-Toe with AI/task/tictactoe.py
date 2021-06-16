# write your code here
from numpy import empty, reshape


class TicTacToe:
    def __init__(self, rows=3, columns=3):
        self.field = empty((rows, columns), dtype=str, order='F')
        self.rows = rows
        self.columns = columns

    def start_setup(self, *setup):
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

    def print_field(self):
        print(*self.field, sep='\n')

    def ask4move(self):
        while True:
            row_pos, col_pos = map(int, input('Enter the coordinates: ').split(' '))
            row_pos -= 1
            col_pos -= 1

            if self.field[col_pos, row_pos] != '_':
                print


if __name__ == '__main__':
    a = TicTacToe()
    a.start_setup(list('XXXOOO___'))

