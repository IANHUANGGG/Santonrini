"""Timeout decorator and exception."""
import os
import signal
import sys

class TimeoutError(Exception):
    """Custom timeout exception for foreign components."""
    def __init__(self, value= 'Timed out'):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

class Timeout:
    """Timeout decorator to determine timeout misbehavior of foreign
    components.
    """
    def __init__(self, seconds):
        self.seconds = seconds
        
    def handler(self, signum, frame):
        raise TimeoutError()

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)
