# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

import referee.game.constants as constants
import copy


# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict) -> None:
        """
        Initialise the agent.
        """
        self._color = color
        self.board = Board()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Returns best minimax action to take
        """
        max_value = float('-inf')
        best_move = None
        new_color = PlayerColor.RED if self._color == PlayerColor.BLUE else PlayerColor.BLUE
        depth = 2
        None_check = True
        
        moves = order_moves(self.board, self._color, self._color)
        for move in moves:
            new_board = copy.deepcopy(self.board)
            new_board.apply_move(move, self._color)
            value = minimax(new_board, depth-1, float('-inf'), float('inf'), self._color, new_color)
            if value > max_value:
                None_check = False
                max_value = value
                best_move = move

        # Select first move if all moves result in a loss
        if None_check:
            best_move = moves[0]

        return best_move

    def turn(self, color: PlayerColor, action: Action, **referee: dict) -> None:
        """
        Update the agent with the last player's action.
        """
        self.board.apply_move(action, color)
                    

class Board:
    MIN_POWER = 1
    CLR_IND = 0
    PWR_IND = 1

    def __init__(self) -> None:
        self.board = {}
    
    def add_cell(self, cell: HexPos, color: PlayerColor) -> None:
        '''
        Add or update a cell on the board.
        '''
        if cell not in self.board:
            self.board[cell] = (color, self.MIN_POWER)
        else:
            self.board[cell] = (color, self.board[cell][self.PWR_IND] + 1)

            # Remove if power is maxed out
            if self.board[cell][self.PWR_IND] > constants.MAX_CELL_POWER:
                del self.board[cell]
    
    def del_cell(self, cell: HexPos) -> None:
        '''
        Delete the cell at the given position.
        '''
        del self.board[cell]

    def apply_move(self, move: Action, color: PlayerColor) -> None:
        '''
        Apply the given move to the board.
        '''
        match move:
            case SpawnAction(cell):
                self.add_cell(cell, color)
                
            case SpreadAction(cell, direction):
                new_cell = cell
                for i in range(self.board[cell][self.PWR_IND]):
                    new_cell = new_cell.__add__(direction)  
                    self.add_cell(new_cell, color)
                self.del_cell(cell)

    def is_game_over(self) -> bool:
        '''
        Return if the game is not over or not
        '''
        colors = set()
        for cell in self.board:
            colors.add(self.board[cell][self.CLR_IND])
            if len(colors) > 1:
                return False
        return True
    
    def get_powers(self) -> dict[PlayerColor, int]:
        '''
        Return a dictionary of the total power of each color
        '''
        powers = {PlayerColor.RED: 0, PlayerColor.BLUE: 0}
        for cell in self.board:
            powers[self.board[cell][self.CLR_IND]] += self.board[cell][self.PWR_IND]
        return powers
    
    def evaluate(self, color: PlayerColor) -> float:
        '''
        Return the evaluation of the board
        '''
        powers = self.get_powers()
        min_color = PlayerColor.RED if color == PlayerColor.BLUE else PlayerColor.BLUE
        if powers[min_color] == 0:
            return float('inf')
        elif powers[color] == 0:
            return float('-inf')
        return powers[color] - powers[min_color]
    
    def get_moves(self, color: PlayerColor) -> list[Action]:
        '''
        Return a list of all possible moves for the given color
        '''
        moves = []
        power = 0

        # Adding Spread Action moves
        for cell in self.board:
            power += self.board[cell][self.PWR_IND]
            if self.board[cell][self.CLR_IND] == color:
                for direction in HexDir:
                    moves.append(SpreadAction(cell, direction))
        # Adding Spawn Action moves
        if power < constants.MAX_TOTAL_POWER:
            for r in range(constants.BOARD_N):
                for q in range(constants.BOARD_N):
                    cell = HexPos(r, q)
                    if cell not in self.board:
                        moves.append(SpawnAction(cell))
        
        return moves
    
def order_moves(board: Board, color: PlayerColor, maximizing_player: PlayerColor) -> list[Action]:
    '''
    Orders move list by its evaluation for branch prioritisation
    '''
    moves = board.get_moves(color)
    return sorted(moves, key=lambda move: board.evaluate(color) if move == maximizing_player else -board.evaluate(color), reverse=True)


def minimax(board: Board, depth: int, alpha: float, beta: float, maximizing_player: PlayerColor, color: PlayerColor) -> float:
    '''
    Minimax with alpha-beta pruning implementation for Infexion
    '''
    if board.is_game_over() or depth == 0:
        return board.evaluate(maximizing_player)
    
    new_color = PlayerColor.RED if color == PlayerColor.BLUE else PlayerColor.BLUE

    if maximizing_player == color:
        max_value = float('-inf')
        for move in board.get_moves(color):
            new_board = copy.deepcopy(board)
            new_board.apply_move(move, color)
            value = minimax(new_board, depth - 1, alpha, beta, maximizing_player, new_color)
            max_value = max(max_value, value)
            alpha = max(alpha, max_value)
            if beta <= alpha:
                break
        return max_value
    else:
        min_value = float('inf')
        for move in board.get_moves(color):
            new_board = copy.deepcopy(board)
            new_board.apply_move(move, color)
            value = minimax(new_board, depth - 1, alpha, beta, maximizing_player, new_color)
            min_value = min(min_value, value)
            beta = min(beta, min_value)
            if beta <= alpha:
                break
        return min_value
    
