"""pyzora - Python library to help parsing secrets from Zelda OoS/OoA

MemorySecret test file. See pyzora.memory_secret for more details.

(c) 2023 fortwoone.
All rights reserved.

This file is part of pyzora.

pyzora is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

pyzora is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with pyzora. If not, see <https://www.gnu.org/licenses/>.
"""
import unittest
from pyzora.memory_secret import *


class MemorySecretTest(unittest.TestCase):
    def setUp(self):
        self._SECRET_STRINGS = (
            (("ほやあさめ", "んぺさが2"), ("●=q(T", "6NN*@")),
            (("やだうぼが", "ぼ87ぷめ"), ("+mR&■", "→●2?(")),
            (("ほやあわゆ", "んぺさぴえ"), ("●=q3g", "6NNn2")),
            (("やだうむあ", "ぼ875ゆ"), ("+mRwd", "→●2s↓")),
            (("ほやあ3こ", "んぺさ4く"), ("●=q)j", "6NNm=")),
            (("やだうだち", "ぼ87めこ"), ("+mR?-", "→●2&→")),
            (("ほやあきへ", "んぺさど1"), ("●=q5d", "6NN:4")),
            (("やだう9ぞ", "ぼ877へ"), ("+mRsg", "→●2w9")),
            (("ほやあざり", "んぺさだた"), ("●=q=S", "6NN/→")),
            (("やだう4だ", "ぼ87もり"), ("+mR%▲", "→●2y="))
        )

    def runTest(self):
        self.test_load_bulk()

    def test_load_bulk(self):
        for region in map(GameRegion, range(2)):
            for expected_secret, item in zip(map(MemoryEnum, range(10)), self._SECRET_STRINGS):
                for is_return in (False, True):
                    msecret = MemorySecret.load(item[region][is_return], region)
                    self.assertEqual(msecret.game_id, 21437)
                    self.assertEqual(msecret.is_return_secret, is_return)
                    self.assertEqual(msecret.memory, expected_secret)
