from neuralnet.nodes import Node
from neuralnet.node_types import node_type
import time

@node_type()
class OutputNode(Node):
    
    accepts = [str]
    
    def __init__(self, node):
        super(OutputNode, self).__init__(node)
        self.threshold = 10

        
    def run(self):
        found = False
        while(True):
            has_data = False
            for synapse in self.inputs:
                if synapse.has_data():
                    has_data = True
                    c = synapse.consume(str)
                    synapse.age()
                    if c == None:
                        continue
                    found = True
                    for signal, intensity in c:
                        if signal in self.data:
                            self.data[signal] = self.data[signal] + intensity
                        else:
                            self.data[signal] = intensity
            if not has_data:
                break
            p = False
            for signal, intensity in self.data.items():
                if intensity >= threshold:
                    print(signal)
                    p=True
            if p:
                self.data = {}
                    
            time.sleep(0.01)          
        super(InputNode, self).run()
            
