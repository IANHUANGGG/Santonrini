from abc import ABC, abstractmethod

class IClientProxy:
    """ Interface for client proxys. 

    Establish a connection between client's proxy to server
    """

    @abstractmethod
    def connect(self):
        """ connect Client Proxy with remote player through TCP.
        
        """
        pass