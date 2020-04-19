from santorini.design.iclient_proxy import IClientProxy
from santorini.common.board import Board
from santorini.common.direction import Direction
from santorini.common.worker import Worker
from santorini.aux.timeout import Timeout, TimeoutError
from santorini.observer.action import Action
from santorini.aux import settings
import copy
from enum import Enum
import importlib
import socket
import json

class ServerMessage(Enum):
    OPPONENT = 0
    SET_NAME = 1
    PLACEMENT = 2
    TURN = 3
    RESULT = 4
    EMPTY = 5

    @staticmethod
    def define_type(msg):
        #takes in a server message and determines its type
#
        #:param List/Str msg: server message
        #:rtype ServerMessage
        if msg == None:
            return ServerMessage.EMPTY
        if type(msg) == str:
            return ServerMessage.OPPONENT
        elif type(msg) == list:
            if len(msg) == 0:
                #print("DETERMINED AS PLACEMENT")
                return ServerMessage.PLACEMENT
            elif type(msg[0]) == list:
                if all([len(placement) == 3 for placement in msg]):
                    if type(msg[0][1]) == int:
                        #print('DETERMINED MSG AS A PLACEMENT REQUEST')
                        return ServerMessage.PLACEMENT
                else:
                    if all([len(meetup) <= 3 for meetup in msg]):
                        #print('DETERMINED MSG AS A RESULT')
                        return ServerMessage.RESULT
                    else:
                        #print('DETERMINED MSG AS A TURN REQUEST')
                        return ServerMessage.TURN
            elif type(msg[0]) == str and msg[0] == "playing-as":
                return ServerMessage.SET_NAME


class ClientProxy(IClientProxy):
    """ client_proxy proxies the interaction between client's Player and the Server

    By linking this proxy with the player implementation, it establish a TCP-based communication
    link between the client side and the server side at the appropriate level (individual games,
    best-of game series, and tournament)
    """

    def __init__(self, player_config, observer_configs, ip, port):
        self.player = self.player_config_to_player(player_config)
        #print(self.player)
        self.opponent_id = None
        self.ip = ip
        self.port = port
        self.connected = True
        self.sock = None
        self.observers = []
        for ob_config in observer_configs:
            self.observer_config_to_observer(ob_config)

    def connect(self):
        """ connect Client Proxy with remote player through TCP.
        
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        self.sock.send(json.dumps(self.player.name).encode())

        while self.connected == True:
            msg_primal = self.sock.recv(1024).decode()
            #('player: ', self.player.name, ' RECEIVED MSG PRIMAL:', msg_primal)
            self.parse(json.loads(msg_primal))
        
    def parse(self, msg):
        """ parse the messsage received from server and ask player perform specific action
        
        Arguments:
            msg {json} -- message from server
        """
        #print('{}  parsing... MESSAGE:{}'.format(self.player.name,msg))
        msg_type = ServerMessage.define_type(msg)

        if msg_type == ServerMessage.OPPONENT:
            self.opponent_id = msg
        elif msg_type == ServerMessage.SET_NAME:
            player_name = msg[1]
            self.player.set_name(player_name)
        elif msg_type == ServerMessage.PLACEMENT:
            self.request_placement(msg)
        elif msg_type == ServerMessage.TURN:
            self.request_turn(msg)
        elif msg_type == ServerMessage.RESULT:
            self.update_observers(Action.RESULTS, msg)
            #print(msg) # print results
            self.connected = False
            self.sock.close()
        elif msg_type == ServerMessage.EMPTY:
            exit()
        

    def request_placement(self, placements):
        """ initialize a board through the given worker placements and ask player to decide
            another worker placement and send to server
        
        Arguments:
            placements {list} -- a JSON list of the WorkerPlace which is
                a JSON array: [Worker,Coordinate,Coordinate]
        """
        #print("WORKER PLACEMENT")
        workers_dict = {}
        for place in placements:
            id = place[0]
            player_name = id[:-1]
            worker_num = int(id[-1])
            row = place[1]
            col = place[2]

            worker = Worker(player_name, worker_num)
            workers_dict[worker] = (row, col)

        board = Board([], workers_dict)
        #print("placement_board: ", board)
        self.update_observers(Action.BOARD, copy.deepcopy(board))
        placement = self.player.place_worker(board)
        #print("placement_type ", type(placement), "content: ", placement)

        self.update_observers(Action.PLACEMENT, placement)
        self.send("placement", placement)
    
    def request_turn(self, list_b):
        """ initialize a board through the list representation of board and ask player to
            decide a turn and send to server
        
        Arguments:
            list_b {undefined} -- 
                (worker_id, Direction, Direction)
                or (worker_id, Direction, None)
                or remote_player name which represent it is giving up
        """
        #print("request_turn, board_list ", list_b)
        board = Board(list_b)
        #print("in request turn, board object: ", board)
        turn = self.player.play_turn(board)
        #print("player_name: ", self.player.name, " turn: ", turn)
        if turn == self.player.name:
            self.update_observers(Action.MESSAGE,
                    "{} wins. {} gave up".format(self.opponent_id, self.player.name))
        else:
            self.update_observers(Action.MOVE_BUILD, turn)
        self.send("turn", turn)

    
    def send(self, type, content):
        """ send message with correct format according to the given type
        
        Arguments:
            type {str} -- either "placement" or "turn"
            content {undefined type} -- either turn or placement
        """
        #print('{} SENDING... TYPE: {} CONTENT: {}'.format(self.player.name, type, content))
        to_send = ""
        if type == "placement":
            to_send = [content[1][0], content[1][1]]
            self.sock.send(json.dumps(to_send).encode())
        elif type == "turn":
            if content == self.player.name:
                self.sock.send(json.dumps(content).encode())
            elif len(content) == 2:
                move_dir = Direction.separate_ew_ns(content[1])
                to_send = [content[0].name, move_dir[0], move_dir[1]]
                self.sock.send(json.dumps(to_send).encode())
            elif len(content) == 3:
                move_dir = Direction.separate_ew_ns(content[1])
                build_dir = Direction.separate_ew_ns(content[2])
                to_send = [content[0].name, move_dir[0], move_dir[1], build_dir[0], build_dir[1]]
                self.sock.send(json.dumps(to_send).encode())

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
        return player

    def observer_config_to_observer(self, config):
        """Given [Name, PathString], convert to Observer object."""
        name = config[0]
        path = config[1]

        spec = importlib.util.spec_from_file_location("module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        observer = module.Observer(name)

        self.add_observer(observer)

    def add_observer(self, observer):
        """ Add an observer to the Referee.

        :param Observer observer: observer to be added to this Referee
        """
        if observer not in self.observers:
            self.observers.append(observer)

    def update_observers(self, action, message):
        """Update all observers registered to the Referee..

        If the observer times out while being updated, the timed out observer is
        removed from the Referee's list of observers and not updated anymore. 

        :param Action action: type of action to be updated
        :param str/board/turn/placment message: message 
        """
        #TODO: ValueError: signal only works in main thread
        for observer in self.observers:
            observer.update(action, message)

