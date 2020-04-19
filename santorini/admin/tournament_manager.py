"""Tournament Manager component for Santorini."""
import importlib.util
import itertools
import json
import sys
from santorini.admin.referee import Referee
from santorini.common.board import Board
from santorini.design.itournament_manager import ITournamentManager
from santorini.lib import echo


class TournamentManager(ITournamentManager):
    """Tournament Manager manages a round-robin tournament of players."""

    def __init__(self, path_or_players=None):
        """ Initialize the Tournament Manager.

        meetups holds the tuples of two players that have had matched.
        observers holds the list of Observer objects.
        misbehavers holds the list of misbehaved player names.

        :param RuleChecker rulechecker:
        """
        self.meetups = []
        self.observers = []
        self.players = []
        self.misbehavers = []
        self.result = []
        if path_or_players == None or type(path_or_players) == str:
            self.set_configuration(self.get_configuration(path_or_players))
        elif type(path_or_players) == list:
            self.players = path_or_players

    def run_tournament(self, rulechecker):
        """ Run the tournament between players.

        Ensure unique player names. For any broken players, it ensures the
        following: the broken player is removed from any future matches, all
        past matches involving the player are counted as won by the opponent. 

        At the end of the tournament, it delivers the list of misbehavers, and
        the list of matches.

        :param RuleChecker rulechecker: the rulechecker
        :return tuple: a list of misbheavers and a list of meetups
        """
        self.ensure_unique_names()

        matches = list(itertools.combinations(self.players, 2))

        while matches:
            player = matches[0][0]
            opponent = matches[0][1]
            referee = Referee(Board(), player, opponent)
            self.add_observers(referee, self.observers)

            game_result = referee.best_of(3, rulechecker)
            game_winner = game_result[0]
            game_misbehaver = game_result[1]

            self.meetups.append((game_winner, player.name
                 if player.name != game_winner else opponent.name))
            
            if game_misbehaver:
                self.players.remove(player
                    if player.name != game_winner else opponent)
                self.misbehavers.append(game_misbehaver)
                self.update_meetups()
                matches = self.remove_matches(matches, game_misbehaver)
                self.result.append([game_winner, player.name 
                    if player.name != game_winner else opponent.name, "irregular"])
            else:
                self.result.append([game_winner, player.name 
                    if player.name != game_winner else opponent.name])
            matches = self.remove_matches(matches, player.name, opponent.name)
        self.inform_players()
        return (self.misbehavers, self.meetups)

    def ensure_unique_names(self): 
        """ Changes the non-unique names into unique ones.
        
        :param List players: list of players
        :return List: list of players with unique names
        """
        seen = set()
        maxlen = 0

        for player in self.players:
            if player.name in seen:
                new_name = player.name + '1' * maxlen
                player.set_name(new_name)
                seen.add(new_name)
            else:
                pname_len = len(player.name)
                maxlen = pname_len if maxlen < pname_len else maxlen
                seen.add(player.name)

    def add_observers(self, referee, observers):
        """Registers the given observers to referee.

        :param Referee referee: the referee
        :param List[Observer] observers: the list of Observers
        """
        for observer in observers:
            referee.add_observer(observer)

    def get_configuration(self, file_path=None):
        """Get the configuration from stdin/filepath.

        :param str file_path: file path in string format
        """
        if file_path == None:
            json_config = sys.stdin.read()
        else:
            with open(file_path, 'r') as file:
                json_config = file.read().replace('\n', '')

        config = json.loads(json_config)

        return config

    def set_configuration(self, config):
        """Set the given configuration.
        
        :param Dictionary config: configuration 
        """
        players = config["players"]
        observers = config["observers"]

        # for each player, initialize as Player objects, add to self.players
        for player_config in players:
            self.player_config_to_player(player_config)

        for obsvr_config in observers:
            self.observer_config_to_observer(obsvr_config)

    def player_config_to_player(self, config):
        """Given [Kind, Name, PathString], convert to Player object."""
        kind = config[0]
        name = config[1]
        path = config[2]

        spec = importlib.util.spec_from_file_location("module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if kind == "good":
            player = module.GoodPlayer(name)
        elif kind == "breaker":
            player = module.BreakingPlayer(name)
        elif kind == "infinite":
            player = module.LoopingPlayer(name)

        self.players.append(player)

    def observer_config_to_observer(self, config):
        """Given [Name, PathString], convert to Observer object."""
        name = config[0]
        path = config[1]

        spec = importlib.util.spec_from_file_location("module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        observer = module.Observer(name)

        self.observers.append(observer)

    def remove_matches(self, matches, player1, player2=None):
        """Removes the matches that contain given player names

        :param list matches: list of meetups
        :param str player1: player1 name
        :param str player2: player2 name
        :return: edited list of matches
        """
        if player2==None:
            return [match for match in matches if match[0].name !=
                           player1 and match[1].name != player1]
        else:
            return [(p1, p2) for p1, p2 in matches if not (
                p1.name == player1 and p2.name == player2)]

    def update_meetups(self):
        """Update the meetups if there were any new misbehavers added."""
        idx = len(self.meetups) - 1
        while idx >= 0:
            meetup = self.meetups[idx]
            if meetup[0] in self.misbehavers and meetup[1] in self.misbehavers:
               del self.meetups[idx]
            elif meetup[0] in self.misbehavers:
                self.meetups[idx] = (meetup[1], meetup[0])
            idx -= 1

    def inform_players(self):
        for player in self.players:
            player.tournament_result(self.result)
