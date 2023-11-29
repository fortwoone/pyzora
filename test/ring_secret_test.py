import unittest
from pyzora.ring_secret import *


class RingSecretTest(unittest.TestCase):
    def test_load_empty(self):
        rsecret = RingSecret.load("L←■!N @bS9& hmR→↓", GameRegion.US_PAL)
        self.assertTrue(NoRings in rsecret, "the secret should not contain any rings")
        rsecret_jp = RingSecret.load("くのてを3 4のんれか ぺそちはと", GameRegion.JP)
        self.assertTrue(NoRings in rsecret_jp)
        self.assertEqual(rsecret.game_id, rsecret_jp.game_id)

    def test_load_all(self):
        rsecret = RingSecret.load("L←■d) B~&JS $j(D8", GameRegion.US_PAL)
        self.assertTrue(AllRings in rsecret)
        rsecret_jp = RingSecret.load("くのてへと 052そが ぞれいわゆ", GameRegion.JP)
        self.assertTrue(AllRings in rsecret_jp)

    def test_write_to_string(self):
        rsecret = RingSecret(game_id=21437, region=GameRegion.US_PAL,
                             rings=FRIENDSHIP | POWER_1 | GREEN,
                             ring_str=integer_string(FRIENDSHIP | POWER_1 | GREEN).rjust(64, "0"))
        rsecret_jp = RingSecret(game_id=21437, region=GameRegion.JP,
                             rings=FRIENDSHIP | POWER_1 | GREEN,
                             ring_str=integer_string(FRIENDSHIP | POWER_1 | GREEN).rjust(64, "0"))
        self.assertIn(FRIENDSHIP, RingSecret.load(str(rsecret), GameRegion.US_PAL))
        self.assertIn(POWER_1, RingSecret.load(str(rsecret), GameRegion.US_PAL))
        self.assertIn(GREEN, RingSecret.load(str(rsecret), GameRegion.US_PAL))
        self.assertIn(FRIENDSHIP, RingSecret.load(str(rsecret_jp), GameRegion.JP))
        self.assertIn(POWER_1, RingSecret.load(str(rsecret_jp), GameRegion.JP))
        self.assertIn(GREEN, RingSecret.load(str(rsecret_jp), GameRegion.JP))
