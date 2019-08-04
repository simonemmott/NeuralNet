from unittest import TestCase
import logging
from neuralnet.nodes import Synapse, Node, _reward
import json

logger = logging.getLogger(__name__)

class SynapseTests(TestCase):

    def test_add_to_synapse(self):
        s = Synapse(Node())
        self.assertFalse(s.has_signal('S1'))
        self.assertEqual(0, s.intensity('S1'))
        s.add('S1', 10)
        self.assertTrue(s.has_signal('S1'))
        self.assertEqual(10, s.intensity('S1'))
        
    def test_add_data_to_synapse(self):
        s = Synapse(Node())
        self.assertFalse(s.has_signal('S1'))
        self.assertEqual(0, s.intensity('S1'))
        self.assertFalse(s.has_signal('S2'))
        self.assertEqual(0, s.intensity('S2'))
        s.add_data({'S1': 10, 'S2': 20})
        self.assertTrue(s.has_signal('S1'))
        self.assertEqual(10, s.intensity('S1'))
        self.assertTrue(s.has_signal('S2'))
        self.assertEqual(20, s.intensity('S2'))
        
    def test_consume_from_synapse(self):
        s = Synapse(Node())
        s.add_data({'S1': 10, 'S2': 20, 123: 20})
        self.assertTrue(s.has_signal('S1'))
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, {'S1': 1, 'S2': 1})
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, {'S1': 1, 'S2': 1})
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, {'S1': 1, 'S2': 2})
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, {'S1': 1, 'S2': 2})
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, {'S1': 1, 'S2': 3})
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, {'S1': 1, 'S2': 4})
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, {'S1': 2, 'S2': 4})
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, {'S1': 2, 'S2': 3})
        c = s.consume(str)
        _reward(10)
        self.assertEqual(c, None)
        
    def test_age_synapse(self):
        s = Synapse(Node())
        s.add_data({'S1': 10, 'S2': 20})
        s.age()
        self.assertEqual({'S1': 5, 'S2': 10}, s.data)
        s.age()
        self.assertEqual({'S1': 2, 'S2': 5}, s.data)
        s.age()
        self.assertEqual({'S1': 1, 'S2': 2}, s.data)
        s.age()
        self.assertEqual({'S2': 1}, s.data)
        s.age()
        self.assertEqual({}, s.data)
        
    def test_synapse_node_has_synapse_input(self):
        n = Node()
        s = Synapse(n)
        self.assertTrue(s in n.inputs)
        
        