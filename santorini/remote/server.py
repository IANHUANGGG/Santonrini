from santorini.design.iserver import IServer
from santorini.aux.timeout import Timeout, TimeoutError
from santorini.remote.remote_proxy_player import RemoteProxyPlayer
from santorini.aux import settings
from santorini.admin.tournament_manager import TournamentManager
from santorini.common.rulechecker import RuleChecker
import copy
import json
import time
import socket
import sys
import time
from threading import Timer

class Server(IServer):

    def __init__(self):
        self.players = []
        self.min_players = 0
        self.port = 0
        self.ip = "localhost"
        self.wait_time = 0
        self.repeat = False

    def run(self, file_path):
        config = self.get_config(file_path)
        self.set_config(config)
        self.start()
        while self.repeat:
            self.start()

    def get_config(self, file_path=None):
        """Get the configuration from stdin/filepath.

        :param str file_path: file path in string format
        """
        if file_path == None:
            json_config = sys.stdin.read()
        else:
            config_file = open(file_path)
            json_config = config_file.readlines()
            config_file.close()

        config = json.loads(json_config)

        return config

    def set_config(self, config):
        """ set up the server according to the configuration

        :param Dictionary config: configuration
        """
        self.min_players = config["min players"]
        self.port = config["port"]
        self.wait_time = config["waiting for"]
        self.repeat = config["repeat"]
        # self.add_connections()

    def add_connections(self):
        """ listen for remote player' connections.

        add_connection wait for limited time as specified in config and sign up certain minimal
        number of players. Server will keep waiting until minimal amount of players are signed up
        even if the limited time has passed.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.listen(10)
        #print("add_connections ")
        timeout = time.time() + self.wait_time

        while timeout > time.time() or len(self.players) < self.min_players:
            s.settimeout(10.0)
            try:
                #print("num of players", len(self.players))
                conn, addr = s.accept()
                player = RemoteProxyPlayer(conn, addr)
                #print("player object", player)
                if player.name != None:
                    self.players.append(player)
            except socket.timeout:
                pass

    def run_tournament(self):
        """ Initialize a Tournament Manager with connected remote players and run tournament"""
        tm = TournamentManager(self.players)
        rc = RuleChecker()
        tm.run_tournament(rc)        

    def results_to_encounter_outcomes(self, misbehaviors, meetups):
        """ Change format of Tournament Manager results into a list of 
        EncounterOutcomes.

        EncounterOutcome is one of:
            - [String, String]: sequence of winner, loser
            - [String, String, "irregular"]: sequence of winner, misbehavior
        """
        #TODO redo changes in tournament manager
        outcomes = copy.deepcopy(meetups)

        for match in outcomes:
            if match[1] in misbehaviors:
                match.append('irregular')

        return outcomes

    def start(self):
        """ remove all existing players and find new players to start tournament
        """
        self.players = []
        self.add_connections()
        self.run_tournament()        
