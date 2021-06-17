# write your code here
import random
from itertools import combinations

from numpy import empty, reshape, where


class TicTacToe:
    def __init__(self, rows=3, columns=3):
        self.field = empty((rows, columns), dtype=str, order='F')
        self.rows = rows
        self.columns = columns
        self.turn = None
        self.player_1 = None
        self.player_2 = None

    def menu(self):
        CHOICES = ('easy', 'medium', 'hard', 'user')
        while True:
            command = input('Input command: ').split()
            if command[0] == 'exit':
                quit()
            elif len(command) == 3 and command[0] == 'start' \
                    and all([i in CHOICES for i in command[1:2]]):
                self.player_1, self.player_2 = command[1], command[2]

                print(f'{self.player_1=}, {self.player_2=}')
                break
            else:
                print('Bad parameters!')

    def easy_ai(self):
        print('Making move level "easy"')
        self.turn = self.current_player()
        possible_moves = tuple(zip(*where(self.field == ' ')))
        self.field[random.choice(possible_moves)] = self.turn

    def medium_ai(self):
        pass

    def hard_ai(self):
        pass

    def current_player(self):
        return 'X' if (self.field == 'O').sum() >= (self.field == 'X').sum() else 'O'

    # REPLACE TO ONLY EVALUATE THIS ONCE
    def play(self, player):
        if player == 'user':
            self.player_move()
        elif player == 'easy':
            self.easy_ai()
        elif player == 'medium':
            self.medium_ai()
        elif player == 'hard':
            self.hard_ai()

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
        indices = tuple(i for i in range(len(flat_field)) if flat_field[i] == self.turn)
        if any([i in winners for i in list(combinations(indices, 3))]):
            print(f'{self.turn} wins')
            quit()
        elif ' ' not in flat_field:
            print('Draw')
            quit()
        else:
            pass

    def player_move(self):
        self.turn = self.current_player()
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
                    self.field[row_pos, col_pos] = self.turn
                    break
            except ValueError:
                print('You should enter numbers!')


if __name__ == '__main__':
    a = TicTacToe()
    a.start_setup(list('_________'))
    # a.start_setup()
    a.menu()
    a.print_field()
    while True:
        a.play(a.player_1)
        a.print_field()
        a.evaluate_game()
        a.play(a.player_2)
        a.print_field()
        a.evaluate_game()
