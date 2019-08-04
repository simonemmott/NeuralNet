import logging

logger = logging.getLogger(__name__)

node_types = []

def node_type():
    def inner(cls):
        node_types.append(cls)
        return cls
    return inner

from .input_nodes import *

def for_signal(signal):
    types = []
    for node_type in node_types:
        logger.debug('Checking whether {nt} accepts {sig}'.format(nt=node_type, sig=signal))
        if node_type.accepts_signal(signal):
            types.append(node_type)
    return types
    

    
    