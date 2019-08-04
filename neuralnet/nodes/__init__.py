import uuid
import logging
from platform import node
from neuralnet.exception import LocationException, LocationOccupied
import threading

logger = logging.getLogger(__name__)

_nodes = {}
_origin = (0,0,0)
_next_node_dist = 0
_located_nodes = {}
_activated_synapses = {}

def _activate_synapse(synapse, signal_type):
    if synapse in _activated_synapses:
        activation = _activated_synapses[synapse]
    else:
        activation = {}
        _activated_synapses[synapse] = activation
    if signal_type in activation:
        activation[signal_type] = activation[signal_type]+1
    else:
        activation[signal_type] = 1
        
def _reward(reward):
    updates = []
    min_activation = 0
    for synapse, activation in _activated_synapses.items():
        for signal_type, count in activation.items():
            if len(updates) < reward:
                updates.append((synapse, signal_type, count))
                if min_activation == 0:
                    min_activation = count
                else:
                    if count < min_activation:
                        min_activation = count
            else:
                if count > min_activation:
                    min = None
                    for i in range(reward):
                        u_synapse, u_signal_type, u_count = updates[i]
                        if u_count == min_activation:
                            updates[i] = (synapse, signal_type, count)
                        if not min or u_count < min:
                            min = u_count
                    min_activation = min
    for synapse, signal_type, count in updates:
        synapse.reward(signal_type)
    _activated_synapses.clear()
                        
        

def register_node(node):
    if not node.id:
        node.id = uuid.uuid1()
    if not node.loc:
        node.loc = _next_free_location()
    _locate_node(node)
    _nodes[node.id] = node
    
def _proximate_locations(loc, dist=1):
    if dist <= 0:
        return [loc]
    pl = []
    # top plane
    y=dist
    for x in range(-dist, dist+1):
        x = -x
        for z in range(-dist, dist+1):
            z = -z
            pl.append((x+loc[0],y+loc[1],z+loc[2]))
    # side planes
    for y in range(-(dist-1), dist):
        x = dist
        for z in range(-dist, dist+1):
            z = -z
            pl.append((x+loc[0],y+loc[1],z+loc[2]))
        x = -dist
        for z in range(-dist, dist+1):
            z = -z
            pl.append((x+loc[0],y+loc[1],z+loc[2]))
        z = dist
        for x in range(-(dist-1), dist):
            x = -x
            pl.append((x+loc[0],y+loc[1],z+loc[2]))
        z = -dist
        for x in range(-(dist-1), dist):
            x = -x
            pl.append((x+loc[0],y+loc[1],z+loc[2]))
    # bottom plane  
    y=-dist
    for x in range(-dist, dist+1):
        x = -x
        for z in range(-dist, dist+1):
            z = -z
            pl.append((x+loc[0],y+loc[1],z+loc[2]))
    return pl

def _next_free_location():
    global _next_node_dist
    pl = _proximate_locations(_origin, _next_node_dist)
    for loc in pl:
        if not _loc_is_occupied(loc):
            return loc
    _next_node_dist = _next_node_dist + 1
    return _next_free_location()

def _loc_is_occupied(loc):
    return loc in _located_nodes

def _get_node(index, default=None):
    if isinstance(index, uuid.UUID):
        return _nodes.get(index, default)
    if isinstance(index, str):
        return _nodes.get(uuid.UUID(index), default)       
    if isinstance(index, tuple):
        return _located_nodes.get(index, default)
    return default
        

def _locate_node(node):
    if node.loc not in _located_nodes:
        _located_nodes[node.loc] = node
    else:
        if node != _located_nodes[node.loc]:
            raise LocationOccupied(node=node)

    
class Network(object):
    
    def __iter__(self):
        self._iter = _nodes.__iter__()
        return self
    
    def __next__(self):
        return self._iter.__next__()
    
    def __len__(self):
        return len(_nodes)
    
    def __getitem__(self, index):
        return _nodes[index]
    
    def __contains__(self, item):
        return item in _nodes
    
    def keys(self):
        return _nodes.keys()
    
    def items(self):
        return _nodes.items()
    
    def values(self):
        return _nodes.values()
    
    def get(self, index, default=None):
        return _get_node(index, default)
    
    def reward(self, r):
        _reward(r)
    
    def clear(self):
        _nodes.clear()
        global _next_node_dist
        _next_node_dist = 0
        _located_nodes.clear()
        
    def nodes_report(self):
        rpt = ''
        for n in _nodes.values():
            rpt = rpt+'Node: {id} at {loc}\n'.format(id=n.id, loc=n.loc)
        return rpt
    
class Synapse(object):

    def __init__(self, node):
        self.node = node
        self.efficiency = {}
        node.inputs.append(self)
        self.data = {}
        
    def has_data(self):
        return len(self.data) == 0
        
    def has_signal(self, signal):
        return signal in self.data
        
    def intensity(self, signal):
        return self.data.get(signal, 0)
        
    def add(self, signal, intensity):
        self.data[signal] = self.data.get(signal,0)+intensity
        self.node.wakeup()
    
    def add_data(self, data):
        for signal, intensity in data.items():
            self.add(signal, intensity)
            
    def consume(self, signal_type):
        efficiency = self.efficiency.get(signal_type, 0)+1
        candidates = {}
        total_intensity = 0
        for signal, intensity in self.data.items():
            if isinstance(signal, signal_type):
                candidates[signal] = intensity
                total_intensity = total_intensity + intensity
        if total_intensity == 0:
            return None
        consumption = efficiency / total_intensity
        resp = {}
        for signal, intensity in candidates.items():
            i = int(intensity * consumption)
            if i == 0:
                i = 1
            if i > self.data[signal]:
                i = self.data[signal]
            resp[signal] = i
            self.data[signal] = self.data[signal] - i

            if self.data[signal] <= 0:
                del self.data[signal]
        _activate_synapse(self, signal_type)
        return resp
    
    def reward(self, signal_type):
        self.efficiency[signal_type] = self.efficiency.get(signal_type, 0)+1
        
        
            
    def age(self):
        data = {}
        for signal, intensity in self.data.items():
            intensity = int(intensity/2)
            if intensity != 0:
                data[signal] = intensity
        self.data = data
            


class Node(object):
    
    accepts = []

    def __init__(self):
        self.id = None
        self.loc = None
        self.inputs = []
        self.outputs = []
        self.thread = None
        register_node(self)
        
    def _proximate_locations(self, dist):
        return _proximate_locations(self.loc, dist)
    
    @property
    def x(self):
        return self.loc[0]
                        
    @property
    def y(self):
        return self.loc[1]
                        
    @property
    def z(self):
        return self.loc[2]
    
    def join(self, node):
        for s in self.outputs:
            if s.node == node:
                return
        self.outputs.append(Synapse(node))
        
    @classmethod
    def accepts_signal(cls, signal):
        if cls.accepts == []:
            return True
        for accept in cls.accepts:
            if isinstance(signal, accept):
                return True
        return False
        
    def wakeup(self):
        if self.thread:
            return
        self.thread = threading.Thread(target=self.__class__.run, args=(self,))
        self.thread.start()
    
    def run(self):
        self.thread = None
        
            
    
        
                        
        
    