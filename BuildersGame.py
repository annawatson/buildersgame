# Author: YU AN PAN
# Date: 12/03/2020
# Description: Write a class called BuildersGame that represents the board for a two-player game that is played on a 5x5 grid.
# During the game, each players' builders will move around the board and add levels to towers.
# The winner is the first one to move a builder on top of a 3-story tower.
# First, x places her two builders on the board, then o places her two builders on the board.
# Throughout the game, no two builders can ever occupy the same square.
# After the initial placements are complete,
# x must move either one of her builders to an adjacent square
# (one square orthogonally or diagonally).

class BuildersGame:
    """
    A builder game class
    """
    def __init__(self):
        """
        initialize player board and tower board
        """
        self._board = [[' '] * 5 for i in range(5)]  # self._board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self._tower_board = [[0] * 5 for j in range(5)]  # self._tower_board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self._current_state = "UNFINISHED"
        self._turn = 0
        self._have_made_their_initial_placements = False
        self.player_to_turn = {}

    def get_current_state(self):
        """
        return current state
        """
        return self._current_state

    def initial_placement(self, builder1_row, builder1_col, builder2_row, builder2_col, player):
        """
        initialize board placement with builder1_row, builder1_col, builder2_row, builder2_col, player
        """
        # 1. If one of the chosen squares is already occupied, initial_placement should return False.
        if self._board[builder1_row][builder1_col] != ' ' or self._board[builder2_row][builder2_col] != ' ':
            return False
        if (builder1_row == builder2_row) and (builder1_col == builder2_col):
            return False
        # 2. Also, if the player placing builders doesn't match the player whose turn it is,
        # 3. or if this method is called for a player that has already made a valid initial placement, then it should return False.
        if self._turn < 2:
            if player == 'x' or player == 'o':
                if player not in self.player_to_turn:
                    self.player_to_turn[player] = self._turn
                else:
                    return False
            else:
                return False

        #if player == 'x' and (self._turn % 2) == 1:  # player1 just moved, so should not move in this term
        #    return False
        #if player == 'o' and (self._turn % 2) == 0:  # player2 just moved, so should not move in this term
        #    return False
        # 4. Otherwise, it should update the board, update whose turn it is, and return True.
        self._board[builder1_row][builder1_col] = player  # first x builder
        self._board[builder2_row][builder2_col] = player  # second x builder
        # 5. take turns plus one
        self._turn += 1
        # 6. if valid initial placements are all set
        if self._turn > 2:
            return False
        if self._turn < 2:
            return False
        if self._turn == 2:
            self._have_made_their_initial_placements = True
        return True

    def _is_move_valid(self, from_row, from_col, to_row, to_col):
        """
        check can move or not
        """
        # If the move is invalid, make_move should return False.
        # 0
        if from_row < 0 or from_col > 4 or to_row < 0 or to_col > 4:
            return False
        # 1 occupied return false
        if self._board[from_row][from_col] != 'o' and self._board[from_row][from_col] != 'x':
            return False
        # Also, if the builder being moved doesn't belong to the player whose turn it is
        #if self._board[from_row][from_col] == 'x' and (self._turn % 2) == 1:  # player1 just moved, so should not move in this term
        if self.player_to_turn[self._board[from_row][from_col] == 'x'] != self._turn % 2:  # player1 just moved, so should not move in this term
            return False
        #if self._board[from_row][from_col] == 'o' and (self._turn % 2) == 0:  # player2 just moved, so should not move in this term
        #    return False
        # 2 invalid to: 如果後兩個數代表的那格不是周圍的，return false
        # 2.0 not in adjacent 8 grids
        if abs(to_row - from_row) > 1 or abs(to_col - from_col) > 1 or (to_row == from_row and to_col == from_col):
            return False

        # 2.1 invalid move: 如果已經有 o 或 x 了不能走
        if self._board[to_row][to_col] == 'o' or self._board[to_row][to_col] == 'x':
            return False

        from_height = self._tower_board[from_row][from_col]
        to_height = self._tower_board[to_row][to_col]
        # to_height is too high
        if from_height + 1 < to_height:
            return False
        return True

    def _is_tower_valid(self, to_row, to_col, tower_row, tower_col):
        """
        check can build tower or not
        """
        # 1 check tower place validation
        if tower_row < 0 or tower_row > 4 or tower_col < 0 or tower_col > 4:
            return False
        if abs(tower_row - to_row) > 1 or abs(tower_col - to_col) > 1 or (tower_row == to_row and tower_col == to_col):
            return False
        tower_player = self._tower_board[tower_row][tower_col]
        if tower_player == 'o' or tower_player == 'x':
            return False
        if self._tower_board[tower_row][tower_col] == 4:
            return False
        return True

    def _make_move(self, from_row, from_col, to_row, to_col):
        """
        make a move
        """
        self._board[to_row][to_col] = self._board[from_row][from_col]
        self._board[from_row][from_col] = ' '

    def _build_tower(self, tower_row, tower_col):
        """
        build a tower
        """
        self._tower_board[tower_row][tower_col] += 1

    def _check_and_update_loser(self, from_row, from_col):
        """
        check if a player has lost (can not move to any adjacent grid)
        """
        directions = [(row, col) for row in range(-1, 2) for col in range(-1, 2) if row != 0 or col != 0]
        for direction in directions:
            neighbor_row = from_row + direction[0]
            neighbor_col = from_col + direction[1]
            # 2.1 invalid: 如果小於0或大於4
            if neighbor_row < 0 or neighbor_row > 4 or neighbor_col < 0 or neighbor_col > 4:
                continue
            # 2.2 invalid move: 如果高度比較高一層可以走，如果高度差不是一階層不能走，低度可以無限低，return false
            from_height = self._tower_board[from_row][from_col]
            neighbor_height = self._tower_board[neighbor_row][neighbor_col]
            # neighbor is too high
            if from_height + 1 < neighbor_height:
                continue
            # 2.3 invalid move: 如果已經有 o 或 x 了不能走
            if self._board[neighbor_row][neighbor_col] == 'o' or self._board[neighbor_row][neighbor_col] == 'x':
                continue
            return
        # all moves are invalid"
        if self._board[from_row][from_col] == 'x':
            self._current_state = "O_WON"
        else:
            self._current_state = "X_WON"

    def _check_and_update_winner(self, to_row, to_col):
        """
        check if a player has won (move to a level-3 tower)
        """
        # 3. Check who wins : "X_WON", "O_WON", "UNFINISHED" or "DRAWN"
        # 1 x or o + height == 3
        if self._tower_board[to_row][to_col] == 3:
            if self._board[to_row][to_col] == 'x':
                self._current_state = "X_WON"
                return
            if self._board[to_row][to_col] == 'o':
                self._current_state = "O_WON"
        # others = drawn
        return

    def make_move(self, from_row, from_col, to_row, to_col, tower_row, tower_col):  # game.make_move(2, 2, 1, 1, 1, 0)
        """
        external method for making a move
        """
        # make move & build tower
        # 0. If this method is called before both players have made their initial placements, then it should return False.
        if not self._have_made_their_initial_placements:
            return False
        # game is over
        if not self._current_state == "UNFINISHED":
            return False
        # 1. If the move is invalid, return False
        if not self._is_move_valid(from_row, from_col, to_row, to_col):
            if from_row < 0 or from_col > 4 or to_row < 0 or to_row > 4:
                return False
            self._check_and_update_loser(from_row, from_col)
            return False
        # 2. If the tower is invalid, return False
        if not self._is_tower_valid(to_row, to_col, tower_row, tower_col):
            return False

        # 3. Make a move and build a tower
        self._make_move(from_row, from_col, to_row, to_col)
        self._build_tower(tower_row, tower_col)

        # 4 update the current state
        self._check_and_update_winner(to_row, to_col)

        # 5 update whose turn it is
        self._turn += 1
        return True
