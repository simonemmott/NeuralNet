from unittest import TestCase
import logging
from neuralnet import node_types
import json

logger = logging.getLogger(__name__)

class NodeTypesTests(TestCase):

    def test_for_signal(self):
        types = node_types.for_signal('S1')
        self.assertTrue(node_types.InputNode in types)
        self.assertFalse(node_types.IntInputNode in types)
        self.assertTrue(node_types.StrInputNode in types)
        
        types = node_types.for_signal(123)
        self.assertTrue(node_types.InputNode in types)
        self.assertTrue(node_types.IntInputNode in types)
        self.assertFalse(node_types.StrInputNode in types)
        
        
        