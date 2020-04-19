from santorini.player.player import Player
from santorini.aux.timeout import Timeout, TimeoutError
from santorini.common.board import Board
from santorini.aux import settings
from santorini.common.worker import Worker
from santorini.common.direction import Direction
from santorini.aux.misbehaviors import Misbehaviors
import json
import socket

class RemoteProxyPlayer(Player):
    """ A Remote Proxy Player

    By passing in a socket connect from Server to RemoteProxyPlayer, it allows Server to 
    create player "object" that plug into tournament manager and referee.
    """

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.name = self.receive_msg("name")
        if self.name == False:
            self.name = None


    def place_worker(self, cur_board):
        """ place_worker ask remote player to place a worker

        place_worker first get information of placed workers from cur_board and pass it
        to remote player. Then it wait for remote player to send back a placement
        :param Board cur_board: the current board
        :rtype tuple
        """
        my_workers = cur_board.player_workers[self.name] if self.name in cur_board.player_workers else []
        msg = self.place_msg(cur_board)
        #print("place_worker: ", msg, "to player: ", self.name)
        self.conn.sendall(json.dumps(msg).encode())

        posn = self.receive_msg("worker placement")
        #print("received posn:   ", posn)
        if type(posn) == list and len(posn) == 2:
            new_worker = Worker(self.name, 1 if len(my_workers) == 0 else 2)
            print("new_placed_worker: ", new_worker)
            return (new_worker, tuple(posn))
        else:
            # The invalid case, should be handled by referee
            return posn


    def play_turn(self, cur_board):
        """ play_turn ask remote player to return a turn.

        play_turn first transform a Board object to list representation and pass it to 
        remote player. Then wait for remote player to send back a Turn 
        :param Board cur_board: the current board
        :rtype tuple: (worker_id, Direction, Direction)
                      or (worker_id, Direction, None)
                      or remote_player name which represent it is giving up
        """
        board_repr = cur_board.board_into_list()
        #print("play_turn_board", board_repr)
        self.conn.sendall(json.dumps(board_repr).encode())
        received = self.receive_msg("turn")
        #TODO IMPORTANT need to improve rulechecker later

        if type(received) == list and len(received) == 5:
            p_workers = cur_board.player_workers[self.name]
            #print("p_workers: ", p_workers, " received: ", received)
            worker = p_workers[0] if received[0] == p_workers[0].name else p_workers[1]
            move_dir = Direction.str_to_dir(received[1], received[2])
            build_dir = Direction.str_to_dir(received[3], received[4])
            #print("proxy_player_play_turn, move_dir: ", move_dir, "worker: ", worker)
            return  (worker, move_dir, build_dir)
        else:
            return received
            
        
    def set_name(self, new_name):
        """ send the given new_name to remote player

        :param str new_name: the new name for remote player
        """
        #print("set_name ", new_name)
        self.name = new_name
        self.conn.sendall(json.dumps(["playing-as", new_name]).encode())

    def misbehaved(self):
        self.conn.sendall(json.dumps("you misbehaved").encode())
        self.conn.close()

    def match_begin(self, opname):
        """ inform remote player that a match with a opponent has begun

        :param str opname: the name of opponent
        """
        #print("match_begin ", opname)
        self.conn.sendall(json.dumps(opname).encode())

    def tournament_result(self, results):
        """ inform remote player the result of tournament

        :param list results: A Results is an array of EncounterOutcomes. 
            where EncounterOutcome is one of the following:
            - [String, String], which is the name of the winner followed by the loser
            - [String, String, "irregular"], which is like the first alternative but signals
              that the losing player misbehaved
        """
        print("tournament_result ", results)
        print("player_name in tournament_result", self.name)
        self.conn.sendall(json.dumps(results).encode())
        self.conn.close()

    def parse_clet_msg(self, msg):
        """ parse the message from client

            Given a client message, parse_clet_msg check if the message is in valid format.
            If correct, parse the message to proper 
        """
        pass

    def receive_msg(self, wait_type):
        """ try to receive message from remote player and time out if no response shows within
            limited time

        :param str wait_type: can either be "name", "placement", "turn"
        :rtype json received: message received from remote player
        """
        wait_time = 0
        if wait_type == "name":
            wait_time = settings.NAME_WAITTIME
        elif wait_type == "worker placement":
            wait_time = settings.PLACEMENT_WAITTIME
        elif wait_type == "turn":
            wait_time = settings.TURN_WAITTIME
        try:
            with Timeout(wait_time):
                received = self.conn.recv(1024)
                #print('REMOTE PROXY PLAYER RECEIVED:', received)
                decoded = received.decode()
                print("type:", type(decoded), "content: ", decoded)
        except TimeoutError:
            self.conn.sendall(json.dumps("Time out on receiving a " + wait_type).encode())
            self.conn.close()
            return Misbehaviors.TIMEOUT
        try:
            loaded = json.loads(decoded)
            return loaded
        except ValueError:
            return Misbehaviors.INVALIDCOMMAND

    def place_msg(self, cur_board):
        """ return a placement message based on the workers on the board
        
        Arguments:
            cur_board {Board} -- The current board
        
        Returns:
            list -- the message representing the placed workers
        """

        workers = cur_board.workers
        #my_workers = cur_board.player_workers[self.name] if self.name in cur_board.player_workers else []
        msg = []
        for worker in workers: 
            posn = cur_board.worker_position(worker)
            placement = [worker.name, posn[0], posn[1]]
            msg.append(placement)
        return msg

        