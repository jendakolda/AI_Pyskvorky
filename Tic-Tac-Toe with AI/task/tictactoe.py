# write your code here
import random
from itertools import combinations, product

from numpy import empty, reshape, where


class TicTacToe:
    winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    CHOICES = ('easy', 'medium', 'hard', 'user')

    def __init__(self, rows=3, columns=3):
        self.field = empty((rows, columns), dtype=str, order='F')
        self.rows = rows
        self.columns = columns
        self.turn = None
        self.player_1 = None
        self.player_2 = None

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

    def menu(self):

        while True:
            command = input('Input command: ').split()
            if command[0] == 'exit':
                quit()
            elif len(command) == 3 and command[0] == 'start' \
                    and command[1] in TicTacToe.CHOICES and command[2] in TicTacToe.CHOICES:
                self.player_1, self.player_2 = command[1], command[2]
                # print(f'{self.player_1=}, {self.player_2=}')
                break
            else:
                print('Bad parameters!')

    # TODO Replace with decorators?
    def play(self, player):
        self.turn = self.current_player()
        if player == 'user':
            self.player_move()
        elif player == 'easy':
            print('Making move level "easy"')
            self.easy_ai()
        elif player == 'medium':
            print('Making move level "medium"')
            self.medium_ai()
        elif player == 'hard':
            print('Making move level "hard"')
            self.hard_ai()

    def easy_ai(self):
        self.field[random.choice(self.get_positions(' '))] = self.turn

    def medium_ai(self):
        my_indices = self.get_positions_indices()
        empty_indices = self.get_positions_indices(' ')
        enemy_indices = tuple(i for i in range(9) if i not in my_indices + empty_indices)
        offensive, defensive = False, False
        if len(my_indices) >= 2:
            offensive = self.get_list_of_moves(my_indices)
        if len(enemy_indices) >= 2:
            defensive = self.get_list_of_moves(enemy_indices)

        if not offensive and not defensive:
            self.easy_ai()
        elif len(my_indices) >= 2 and offensive:  # Offense
            selected_move_index = random.choice(offensive)
            self.field[selected_move_index // self.columns, selected_move_index % self.columns] = self.current_player()
        elif len(enemy_indices) >= 2 and defensive:  # Defense
            selected_move_index = random.choice(defensive)
            self.field[selected_move_index // self.columns, selected_move_index % self.columns] = self.current_player()
        else:
            print('Error in medium player')

    def hard_ai(self):
        pass

    def player_move(self):
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

    def current_player(self):
        return 'X' if (self.field == 'O').sum() >= (self.field == 'X').sum() else 'O'

    def print_field(self):
        print(9 * '-')
        for i in range(self.rows):
            print('|', *self.field[i], '|', sep=' ')
        print(9 * '-')

    def evaluate_game(self):
        flat_field = self.field.flatten().tolist()
        occupied_indices = self.get_positions_indices()
        if any([i in TicTacToe.winners for i in list(combinations(occupied_indices, 3))]):
            print(f'{self.turn} wins')
            quit()
        elif ' ' not in flat_field:
            print('Draw')
            quit()
        else:
            pass

    def get_positions_indices(self, sign=None):
        if not sign:
            sign = self.turn
        assert sign in 'XO '
        return tuple(i for i in range(self.rows * self.columns) if self.field.flatten().tolist()[i] == sign)

    def get_positions(self, sign=None):
        if not sign:
            sign = self.turn
        assert sign in 'XO '
        return tuple(zip(*where(self.field == sign)))

    def get_list_of_moves(self, occupied):
        pair_and_empty = product(combinations(occupied, 2), self.get_positions_indices(' '))
        lst = list()
        for i in pair_and_empty:
            _pair, _empty = i
            in_winners = [*_pair, _empty]
            in_winners.sort()
            if tuple(in_winners) in TicTacToe.winners:
                lst.append(_empty)
        return tuple(lst)


if __name__ == '__main__':
    a = TicTacToe()
    a.start_setup(list('_________'))
    a.menu()
    a.print_field()
    while True:
        a.play(a.player_1)
        a.print_field()
        a.evaluate_game()
        a.play(a.player_2)
        a.print_field()
        a.evaluate_game()
