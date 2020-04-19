from abc import ABC, abstractmethod

class IServer(ABC):
    """ A Server allows remote clients to sign up for a tournament

    A Server allows remote clients to sign up for a tournament. After waiting for a limited 
    amount of time and signing up a certain minimal number of players, the Server creates a
    Tournament manager from the players and runs a complete tournament. The Server is under
    no obligation to accept connections while a tournament is in progress.
    """

    @abstractmethod
    def run(self):
        """ run the server

        After this run method is called, the Server will get the configuration from STDIN 
        if not specified and set itself up according to the config: wait for a limited 
        amount of time and signing up a certain minimal number of players. Then, Server 
        create a Tournament manager from the players and runs a complete tournament.
        """
        pass
