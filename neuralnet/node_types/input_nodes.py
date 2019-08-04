from neuralnet.nodes import Node
from neuralnet.node_types import node_type

@node_type()
class InputNode(Node):
    
    accepts = []
    
    def input(self, data):
        self.data = data
        self.wakeup()
        
    def run(self):
        for synapse in self.outputs:
            data = {}
            for signal, intensity in self.data.items():
                i = int(intensity/len(self.outputs))
                if i == 0:
                    i = 1
                data[signal] = i
            synapse.add_data(data)
        self.data = {}
        super(InputNode, self).run()
            
@node_type()
class IntInputNode(InputNode):
    
    accepts = [int]
    
    def input(self, data):
        self.data = data
        self.wakeup()
                    
@node_type()
class StrInputNode(InputNode):
    
    accepts = [str]
    
    def input(self, data):
        self.data = data
        self.wakeup()
                    
