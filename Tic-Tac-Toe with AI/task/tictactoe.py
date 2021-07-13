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
        # empty_indices = self.get_positions_indices(' ')
        enemy_indices = self.get_positions_indices(self.opposing_player())
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
        m, px, py = self.max_alpha_beta(-2, 2)
        self.field[px, py] = self.current_player()

    def player_move(self):
        while True:
            move = input('Enter the coordinates: ')
            if move == 'exit':
                quit()
            try:
                move = move.replace('  ', ' ')
                row_pos, col_pos = map(int, move.strip().split(' '))
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

    def opposing_player(self):
        return 'O' if self.current_player() == 'X' else 'X'

    def print_field(self):
        print(9 * '-')
        for i in range(self.rows):
            print('|', *self.field[i], '|', sep=' ')
        print(9 * '-')

    def evaluate_game(self):
        result = self.is_end()
        if result == ' ':
            print('Draw')
            quit()
        elif result is None:
            pass
        else:
            print(result + ' wins')
            quit()

    def is_end(self):
        flat_field = self.field.flatten().tolist()
        if ' ' not in flat_field:
            return ' '
        for sign in 'XO':
            occupied_indices = self.get_positions_indices(sign)
            if any([i in TicTacToe.winners for i in list(combinations(occupied_indices, 3))]):
                return sign
        return None

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

    # From here
    def max_alpha_beta(self, alpha, beta):

        # Possible values for maxv are:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        # We're initially setting it to -2 as worse than the worst case:
        maxv = -2

        px = None
        py = None

        result = self.is_end()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win
        if result == self.opposing_player():
            return -1, 0, 0
        elif result == self.current_player():
            return 1, 0, 0
        elif result == ' ':
            return 0, 0, 0

        for row_pos in range(self.rows):
            for col_pos in range(self.columns):
                if self.field[row_pos, col_pos] == ' ':
                    # On the empty field player 'O' makes a move and calls Min
                    # That's one branch of the game tree.
                    self.field[row_pos, col_pos] = self.current_player()
                    m, min_row_pos, min_col_pos = self.min_alpha_beta(alpha, beta)
                    # Fixing the maxv value if needed
                    if m > maxv:
                        maxv = m
                        px = row_pos
                        py = col_pos
                    # Setting back the field to empty
                    self.field[row_pos, col_pos] = ' '
                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if maxv >= beta:
                        return maxv, px, py

                    if maxv > alpha:
                        alpha = maxv
        return maxv, px, py

    def min_alpha_beta(self, alpha, beta):

        # Possible values for minv are:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # We're initially setting it to -2 as worse than the worst case:
        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == self.current_player():
            return -1, 0, 0
        elif result == self.opposing_player():
            return 1, 0, 0
        elif result == ' ':
            return 0, 0, 0

        for row_pos in range(self.rows):
            for col_pos in range(self.columns):
                if self.field[row_pos, col_pos] == ' ':
                    self.field[row_pos, col_pos] = self.current_player()
                    m, max_row_pos, max_col_pos = self.max_alpha_beta(alpha, beta)

                    if m < minv:
                        minv = m
                        qx = row_pos
                        qy = col_pos
                    # Setting back the field to empty
                    self.field[row_pos, col_pos] = ' '
                    if minv <= alpha:
                        return minv, qx, qy

                    if minv < beta:
                        beta = minv
        return minv, qx, qy


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
