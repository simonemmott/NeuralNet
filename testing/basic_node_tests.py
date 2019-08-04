from unittest import TestCase
import logging
from neuralnet.nodes import Node, Network
import json

logger = logging.getLogger(__name__)

class BasicNodeTests(TestCase):

    def setUp(self):
        self.network = Network()
        self.network.clear()
    
    def test_new_node_has_unique_id(self):
        n1 = Node()
        self.assertIsNotNone(n1.id)
        n2 = Node()
        self.assertIsNotNone(n2.id)
        self.assertNotEqual(n1.id, n2.id)
        
    def test_new_node_has_location(self):
        n1 = Node()
        self.assertEqual(n1.loc, (0,0,0))
        
    def test_list_proximate_node_locations(self):
        n1 = Node()
        pl = n1._proximate_locations(1)
        self.assertTrue((-1,1,-1) in pl)
        self.assertTrue((-1,1,0) in pl)
        self.assertTrue((-1,1,1) in pl)
        self.assertTrue((0,1,-1) in pl)
        self.assertTrue((0,1,0) in pl)
        self.assertTrue((0,1,1) in pl)
        self.assertTrue((1,1,-1) in pl)
        self.assertTrue((1,1,0) in pl)
        self.assertTrue((1,1,1) in pl)
        self.assertTrue((-1,0,-1) in pl)
        self.assertTrue((-1,0,0) in pl)
        self.assertTrue((-1,0,1) in pl)
        self.assertTrue((0,0,-1) in pl)
        self.assertTrue((0,0,1) in pl)
        self.assertTrue((1,0,-1) in pl)
        self.assertTrue((1,0,0) in pl)
        self.assertTrue((1,0,1) in pl)
        self.assertTrue((-1,-1,-1) in pl)
        self.assertTrue((-1,-1,0) in pl)
        self.assertTrue((-1,-1,1) in pl)
        self.assertTrue((0,-1,-1) in pl)
        self.assertTrue((0,-1,0) in pl)
        self.assertTrue((0,-1,1) in pl)
        self.assertTrue((1,-1,-1) in pl)
        self.assertTrue((1,-1,0) in pl)
        self.assertTrue((1,-1,1) in pl)
        self.assertTrue((0,0,0) not in pl)

    def test_join(self):
        n1 = Node()
        n2 = Node()
        self.assertEqual(0, len(n1.outputs))
        self.assertEqual(0, len(n2.inputs))
        n1.join(n2)
        self.assertEqual(1, len(n1.outputs))
        self.assertEqual(1, len(n2.inputs))
        self.assertEqual(n1.outputs[0].node, n2)
        self.assertEqual(n1.outputs[0], n2.inputs[0])
        n1.join(n2)
        self.assertEqual(1, len(n1.outputs))
        self.assertEqual(1, len(n2.inputs))
        self.assertEqual(n1.outputs[0].node, n2)
        self.assertEqual(n1.outputs[0], n2.inputs[0])
