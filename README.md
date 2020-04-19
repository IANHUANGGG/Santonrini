Santorini
=======================================================
`./santorini` contains the following directories:
  *  `/admin`
  *  `/aux`
  *  `/common`
  *  `/design`
  *  `/lib`
  *  `/observer`
  *  `/player`



Design
------
In the Design directory is the contents of the board interface for Santorini and our plan 
for designing Santorini.

`iboard.py`, is the interface for the Santorini board. In it contains
a class for the Board with methods to place and move Workers, and build a Building on 
the board. The Board class itself has two internal attributes, the `_board` attribute
and the `_workers` attribute. `_board` is a 2-d array of Buildings, all starting with 0
floors. `_workers` is a dictionary mapping wokers to their position on the board. 

`iobserverable.py`, is the interface for the Observable. It is inherited by the Referee for the Observers to observe its actions.

`iobserver.py`, is the interface for the Observer. It is initialized with an object that inherits the IObservable interface. It is able to observe each player's turn, the correponding board result, any misbehavior, and the game result. All observations are printed out via stdout.

`iplayer.py`, is the interface for the Santorini player. In it contains a class for
the Player with methods to initialize a player in the game, place a worker, play a turn, and end the game. 

`ireferee.py`, is the interface for the Santorini referee. In it contains an AbstractReferee class
that has a list of players in the current game. The class contains two methods, run_game and complete_turn. run_game
will startup the game with the associated players and surpervise turns being played. complete_turn will execute
any turn given by the player's strategy in the game. 

`irulechecker.py`, is the interface for the Santorini RuleChecker. In itcontains a class for the RuleChecker with methods to check all of the defined rules for Santorini. These rules include whether a worker can 
be placed/moved and if a floor can be built in a building. To check these rules, these methods will take in 
a copy of the current board and a worker with a direction. 

`istrategy.py` is the interface for the Santorini strategy. In it contains two methods for 
constructing a strategy to play Santorini, plan_turn and plan_placement. Plan_placement returns a valid placement 
for a worker on the board, and plan_turn returns a valid move and build request. 

`itournament_manager.py` is the interface for the Tournament Manager of Santorini. Its main method is `run_tournament` that runs a Santorini tournament between all the players given in the configuration file when initialized. The tournament is held in a round-robin fashion, meaning all players will be matched up with all other players. The tournament manager also handles misbehaving players by reverting its past meetup results, and removing them from their future meetups.

`plan.pdf`, is the design plan for implementing Santorini. In it contains
what we think we'll need to implement the game and the specific classes/methods/etc that
we outlined for using the create the game in our eyes. 

`remote_protocol.md` is the design plan for implementing remote agents for a Santorini tournament.

Admin
-----
Admin directory contains game components utilized only by the administrators of the game Santorini.

The files contained:
  * `referee.py`
  * `tournament_manager.py`

`referee.py` holds the Referee class. The Referee organizes a game between two different players and  enforces the rules of the game with the RuleChecker. It guides the two players in a game through initialization, steady-state and game-over stages. If at any point of the game, a player misbehaves by not returning a valid turn or timing out, the referee automatically assigns the other player as the winner and concludes the game.

`tournament_manager.py` holds the TournamentManager class. The tournament manager oversees a Santorini tournament of multiple players. It is able to match all players through a round-robin fashion; each meetup consisting of (currently) three rounds. It is initialized with a filepath to a JSON config file containing the players and observers of the tournament. Its `run_tournament` function runs the tournament with the given RuleChecker. Additional functionalities of the tournament manager include ensuring unique names between all given players, and misbehaving player handling; reversing past meetup results and removing them from future meetups. 

Aux
---
Aux directory contains auxiliary files.

The files contained:
  * `misbehaviors.py`
  * `settings.py`
  * `timeout.py`

Misbehaviors is an Enum class defining the possible type of misbehaviors. NORMAL implies there were no misbehaviors. TIMEOUT implies there was a timeout misbehavior. INVALIDCOMMAND implies there was a invalid command misbehavior. Misbehaviors class contains a function `misbehave_msg` that returns a string message of the corresponding Misbehaviors enum. This allows the administrator to announce the misbehavior to the player/observer with ease.

Settings.py contain all constants that rule our implementation of Santorini such as the board size, number of workers per player, and total number of player per game.

Timeout.py hold our custom timeout exception and decorator to capture any foreign components from infinitely looping and judge misbehavior. 

Common
------

The files contained:
  * `board.py`
  * `building.py`
  * `direction.py`
  * `rulechecker.py`
  * `worker.py`


The Board class, which includes two class attributes, the internal
representation of the board and a dictionary of Worker objects associated with their
current board position. The class also includes methods for movement, placement, building, 
getting board attributes, and getting a position on the board. 

The Building class, which has a single class attribute for the number
of floors in a building. It also has class methods building a floor onto a building and getting
the current number of floors. 

The Direction enum, which we define as the different possible directions
a Worker can move on the board. This is used for any movement to ensure that workers can only
ever move in 1-square increments.

The RuleChecker class, which includes two methods for checking if you can move and can build.
This will return True/False statements based on the input worker and direction and the current
board state.

The Worker class, which has class attributes for the player's name its 
associated with and the piece number associated with itself. We also re-define equality and 
hash representations for use later in our logic checking. 

Observer
--------
Files contained:
  * `action.py`
  * `observer.py`

`action.py` contains the Action Enum class. It defines the kinds of message update_observer is sending to the Observer for it to parse it correctly.

`observer.py` contains the Observer class. It inherites from `IObserver` class in `/design` and is able to observe the game through a Referee. 

Player
------

In the player directory is our implementation of our Player interface, along with player strategies. 

`player.py` includes:

* The Player class, which is our skeleton of what a player will look like in Santorini. The Player
includes its name as a string, a list of Worker objects, a Strategy object, and a RuleChecker object. 
This class also includes four methods, initialize, play_placement, play_turn, and game_over. Over the 
course of a game, the player will initialize itself, play a placement and turns by passing its information
(i.e. workers and current board state) onto the strategy object, which will in turn return a valid turn to 
pass to the referee object to execute.

`place_strat.py` includes:
* The two placement strategies, PlaceStratDiagonal and PlaceStratFar, which are both classes. PlaceStratDiagonal
will return player placement along the diagonal of the game board, and PlaceStratFar will return player placement
the furthest possible away from opposing players. 

`tree_strat.py` includes:
* The TurnStrategy implementation, TreeStrategy. This is a class that has a depth attribute for the look-ahead, 
and methods to get the turn derived by the strategy, find the next turn derived by the strategy, and determine
if the player can survive for a finite amount of turns (get_turn, next_turn, and do_survive, respectively). 

Tests
-----

In the Tests directory are our unit tests for implemented game pieces. Instructions on how to run these tests
can be found in `testme.md`

Lib
---

In the Lib directory are all of the external methods that we've used to ease development. 

`echo.py` includes

* The function `json_echo`, which we use to parse input to pass onto our test harness. 