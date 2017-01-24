# Copyright 2017 Bright Computing Holding BV.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import unittest

thisdir = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(thisdir, ".."))

import nameranges.parser as range_parser # noqa
from nameranges.parser import RangeParseError # noqa


class TestHostnameParsing(unittest.TestCase):
    def test_node001_as_an_with_one_element(self):
        description = "node001"

        nodes = range_parser.parse(description)

        self.assertEquals(1, len(nodes))

        node001_in_nodes = "node001" in nodes
        self.assertTrue(node001_in_nodes)

    def test_advanced_grouping(self):
        description = "node001,node009..node011"

        nodes = range_parser.parse(description)

        self.assertEquals(4, len(nodes))

        node001_in_nodes = "node001" in nodes
        node009_in_nodes = "node009" in nodes
        node010_in_nodes = "node010" in nodes
        node011_in_nodes = "node011" in nodes

        self.assertTrue(node001_in_nodes)
        self.assertTrue(node009_in_nodes)
        self.assertTrue(node010_in_nodes)
        self.assertTrue(node011_in_nodes)

    def test_grouping_on_mic_node_names(self):
        description = "node001-mic[0..1]"

        nodes = range_parser.parse(description)

        self.assertEquals(2, len(nodes))
        self.assertEquals(["node001-mic0", "node001-mic1"], nodes)

    def test_malformed_grouping_generates_exception(self):
        description = "node001,node00a..node011"

        try:
            range_parser.parse(description)
            self.assertTrue(False)
        except RangeParseError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
