from unittest import TestCase
import uuid
import logging
from neuralnet import nodes
from neuralnet.nodes import Node, Network, _nodes

logger = logging.getLogger(__name__)

class BasicNetworkTests(TestCase):
    
    def setUp(self):
        self.network = Network()
        self.network.clear()
    
    def test_len_network(self):
        self.assertEqual(len(self.network), 0)
        n1 = Node()
        self.assertEqual(len(self.network), 1)
        n2 = Node()
        self.assertEqual(len(self.network), 2)
        self.network.clear()
        self.assertEqual(len(self.network), 0)
        
    def test_get_node(self):
        n1=Node()
        n2=Node()
        gn1 = self.network.get(n1.id)
        self.assertEqual(gn1, n1)
        gn2 = self.network.get(n2.id)
        self.assertEqual(gn2, n2)
        
    def test_clear_network(self):
        n1 = Node()
        n2 = Node()
        self.assertGreater(len(self.network), 0)
        self.network.clear()
        self.assertEqual(len(self.network), 0)
        
    def test_network_contains_nodes(self):
        n1=Node()
        self.assertTrue(n1.id in self.network)
        self.assertTrue(n1 in self.network.values())
        n2=Node()
        self.assertTrue(n1.id in self.network)
        self.assertTrue(n1 in self.network.values())
        
    def test_network_is_iterable(self):
        n1 = Node()
        n2 = Node()        
        for key in self.network:
            self.assertTrue(key in _nodes)
            
    def test_network_is_subscriptable(self):
        n1 = Node()
        n2 = Node()  
        self.assertEqual(n1, self.network[n1.id])      
        self.assertEqual(n2, self.network[n2.id])
        
    def test_network_contains(self):    
        n1 = Node()
        n2 = Node()
        self.assertTrue(n1.id in self.network)
        self.assertTrue(n2.id in self.network)
        
    def test_network_keys(self):
        n1 = Node()
        n2 = Node()
        self.assertTrue(n1.id in self.network.keys())
        self.assertTrue(n2.id in self.network.keys())
        
    def test_network_values(self):
        n1 = Node()
        n2 = Node()
        self.assertTrue(n1 in self.network.values())
        self.assertTrue(n2 in self.network.values())
        
    def test_network_get(self):
        n1 = Node()
        n2 = Node()
        self.assertEqual(n1, self.network.get(n1.id, 'NOT_FOUND'))
        self.assertEqual(n2, self.network.get(n2.id, 'NOT_FOUND'))
        self.assertEqual('NOT_FOUND', self.network.get(uuid.uuid1(), 'NOT_FOUND'))
        

