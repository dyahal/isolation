"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    #raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    j, i = game.get_player_location(game.get_opponent(player))
    values = float (((abs(h - y) + abs(w - x)) * own_moves) - ((abs(h - j) + abs(w - i)) *opp_moves))
    return values

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    total_tiles = game.width * game.height
    return float((own_moves *len(game.get_blank_spaces())/total_tiles )- (opp_moves * len(game.get_blank_spaces())/total_tiles))

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    own_moves = len(game.get_legal_moves(player));
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    y, x = game.get_player_location(player);
    w, h = game.get_player_location(game.get_opponent(player));
    median = float(abs(h - y) + abs(w - x))
    if median > 0:
        return float(own_moves / median)**2
    else:
        return 1

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game,self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    
    def minimax(self, game,depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        def MinMaxVal(move,game,d,MaxVal):
            
            #Check timeout
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            #Check if node reached end
            if game.utility(self) != 0 :
                return self.score(game,self);

            if d == 0:
                 return self.score(game,self);

            if MaxVal == True:
                values = float("-inf")
                #Calculate maximum value
                for s in game.get_legal_moves():
                    values = max(values, MinMaxVal(s,game.forecast_move(s),d-1,False))
                return values
            else :
                values =  float("inf")
                #Calculate minimum value
                for s in game.get_legal_moves():
                    values = min(values, MinMaxVal(s,game.forecast_move(s),d-1,True))
                return values
                
        
        #Minimax timeout's check
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Minimax check current game state, if reached end, return current move
        if game.utility(self) != 0 :
            return game.get_player_location(self);

        #Calculate best move
        legal_moves = game.get_legal_moves()              
        move = ( max (legal_moves, key = lambda a: MinMaxVal (a,game.forecast_move(a),depth-1,False)))
        return move
        

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    EndNode = False;
    legal_moves = [];
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        
        self.time_left = time_left
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1,-1)
        
        """
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.alphabeta(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed
        """

        #Check current game state, if reached end, return current move
        if game.utility(self) != 0 :
            return best_move

        #Check if board is empty, return move to the center(position closest to center)
        if game.get_legal_moves() == game.get_blank_spaces():
            return (math.ceil(game.width /2), math.ceil(game.height /2))
           
        try:
            i = 1;

            #Do Loop until node reached end or timeout
            while True:
                best_move = self.alphabeta(game,i);
                i = i+1;
            #return best_move
            
        except SearchTimeout:
            #return best_move
            pass

        return best_move;

        
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), player = "Maximize"):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        def alphabetaprunning(game, depth, alpha, beta, maxVal) :
            #Check timeout
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout();
            
            #Check if the depth reached the max depth
            

            #Check if node reached end
            #if game.utility(self) != 0 :
                #self.EndNode = True;
                #return game.utility(self)
                #return self.score(game,self);

            if maxVal == True :
                if depth == 0:
                    return self.score(game,self)
            
                v = float("-inf")
                #Calculate maximum value
                for s in game.get_legal_moves():
                    v = max(v, alphabetaprunning(game.forecast_move(s),depth-1,alpha,beta, False))
                    if v >= beta:
                        return v
                    alpha = max(alpha, v);
                return v;               
            else:
                if depth == 0:
                    return self.score(game,self)
                v = float("inf")
                #Calculate minimum value
                for s in game.get_legal_moves():
                    v = min(v, alphabetaprunning(game.forecast_move(s),depth-1,alpha,beta, True))
                    if v <= alpha:
                        return v;
                    beta = min(beta, v);
                return v;


        best_value = float("-inf")
        
        best_move = (-1,-1)
        #alpha beta timeout check
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Check if game state is reach end
        if game.utility(self) != 0 :
            self.EndNode = True;
            return game.get_player_location(self);
        
        #alpha beta calculate best move (start recursive function)
        
        legal_moves = game.get_legal_moves()
        for move in legal_moves:
            if self==game.active_player:
                value = alphabetaprunning (game.forecast_move(move), depth-1, alpha,beta ,False);
            elif self == game.inactive_player:
            #    print("here");
                value = alphabetaprunning (game.forecast_move(move), depth-1, alpha,beta ,True);
            if value >= best_value:
                best_move = move;
                best_value = value;
            if best_value >= beta:
                return move;
            alpha = max(alpha, value);
        return best_move;
        
        
