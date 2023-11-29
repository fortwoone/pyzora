"""pyzora - Python library to help parsing secrets from Zelda OoS/OoA

GameSecret test file. See pyzora.game_secret for more details.

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

from pyzora.game_secret import *


class GameSecretTest(unittest.TestCase):
    def test_load_empty(self):
        # Secrets CAN be used to start normal games, as weird as it seems
        gsecret = GameSecret.load("H←■!@ ←2♦y& GB5●5 6♥s↑6", GameRegion.US_PAL)
        self.assertTrue(gsecret.game_id == 21437, "wrong game ID for secret")
        self.assertTrue(gsecret.region == GameRegion.US_PAL, "wrong encoding used")
        self.assertFalse(gsecret.is_linked_game, "gsecret is shown as a linked game whereas it shouldn't")
        self.assertFalse(gsecret.is_hero_quest, "gsecret is shown as a Hero's Secret, whereas it's not actually one")
        self.assertFalse(gsecret.was_given_free_ring, "gsecret counts Vasu's free ring as given, whereas it shouldn't")
        self.assertTrue(gsecret.animal == ObtainedCompanion.NONE, "gsecret is shown with a friend, whereas the player "
                                                                  "shouldn't have one")
        self.assertTrue(gsecret.behaviour == ChildBehaviour.NONE, "the secret contains a value for the behaviour, "
                                                                  "whereas it shouldn't")
        # We need to count the spaces here, as the returned string will always take up 5 characters
        self.assertTrue(gsecret.link_name == "Link ", "gsecret doesn't correctly store Link's name")
        self.assertTrue(gsecret.child_name == "Pip  ", "gsecret doesn't correctly store the child's name")
        self.assertTrue(gsecret.target_game == TargetGame.AGES, "gsecret doesn't correctly decode the target game")

    def test_load_empty_jp(self):
        gsecret = GameSecret.load("えのてを7 ががむとか の7ふにも るこぴりみ", GameRegion.JP)
        self.assertTrue(gsecret.region == GameRegion.JP, "wrong region for secret")
        self.assertTrue(gsecret.game_id == 21437, "wrong game ID for secret")
        self.assertFalse(gsecret.is_linked_game, "gsecret is shown as a linked game whereas it shouldn't")
        self.assertFalse(gsecret.is_hero_quest, "gsecret is shown as a Hero's Secret, whereas it's not actually one")
        self.assertFalse(gsecret.was_given_free_ring, "gsecret counts Vasu's free ring as given, whereas it shouldn't")
        self.assertTrue(gsecret.animal == ObtainedCompanion.NONE, "gsecret is shown with an animal, whereas the player "
                                                                  "shouldn't have one")
        self.assertTrue(gsecret.behaviour == ChildBehaviour.NONE, "the secret contains a value other than NONE "
                                                                  "whereas it shouldn't")
        # We need to count the spaces here, as the returned string will always take up 5 characters
        self.assertTrue(gsecret.link_name == "LINK ", "gsecret doesn't correctly deduce Link's name")
        self.assertTrue(gsecret.child_name == "PIP  ", "gsecret doesn't correctly deduce the child's name")
        self.assertTrue(gsecret.target_game == TargetGame.AGES, "gsecret doesn't correctly deduce the target game")

    def test_load_linked(self):
        gsecret1 = GameSecret.load("H←■!@ ←2♦y& GB5●y 6♥?↑4", GameRegion.US_PAL)
        gsecret2 = GameSecret.load("H←■!@ ←2♦y& GB5●( 6♥?↑=", GameRegion.US_PAL)
        gsecret3 = GameSecret.load("H←■!@ ←2♦y& GB5●m 6♥?↑=", GameRegion.US_PAL)
        self.assertTrue(gsecret1.region == gsecret2.region == gsecret3.region == GameRegion.US_PAL,
                        "wrong region for secrets")
        self.assertTrue(gsecret1.game_id == gsecret2.game_id == gsecret3.game_id == 21437, "the game ID is different "
                                                                                           "between the expected "
                                                                                           "value and at least one of "
                                                                                           "the secrets")
        self.assertNotEqual(gsecret2.animal, gsecret1.animal)
        self.assertNotEqual(gsecret3.animal, gsecret2.animal)
        self.assertNotEqual(gsecret1.animal, gsecret3.animal)
        self.assertEqual(gsecret1.animal, ObtainedCompanion.RICKY)
        self.assertEqual(gsecret2.animal, ObtainedCompanion.DIMITRI)
        self.assertEqual(gsecret3.animal, ObtainedCompanion.MOOSH)
        self.assertEqual(gsecret1.link_name, gsecret2.link_name)
        self.assertEqual(gsecret3.link_name, gsecret2.link_name)
        self.assertEqual(gsecret3.link_name, gsecret1.link_name)
        self.assertEqual(gsecret1.link_name, "Link ")
        self.assertEqual(gsecret1.child_name, gsecret2.child_name)
        self.assertEqual(gsecret3.child_name, gsecret2.child_name)
        self.assertEqual(gsecret1.child_name, gsecret3.child_name)
        self.assertEqual(gsecret1.child_name, "Pip  ")
        self.assertEqual(gsecret1.was_given_free_ring, gsecret2.was_given_free_ring)
        self.assertEqual(gsecret1.was_given_free_ring, gsecret3.was_given_free_ring)
        self.assertEqual(gsecret3.was_given_free_ring, gsecret3.was_given_free_ring)
        self.assertFalse(gsecret1.was_given_free_ring)

    def test_load_linked_jp(self):
        gsecret1 = GameSecret.load("えのてを7 ががむとか の7ふにご るこがりす", GameRegion.JP)
        gsecret2 = GameSecret.load("えのてを7 ががむとか の7ふにを るこがりの", GameRegion.JP)
        gsecret3 = GameSecret.load("えのてを7 ががむとか の7ふに9 るこがりの", GameRegion.JP)
        self.assertTrue(gsecret1.region == gsecret2.region == gsecret3.region == GameRegion.JP,
                        "wrong encoding for secrets")
        self.assertTrue(gsecret1.game_id == gsecret2.game_id == gsecret3.game_id == 21437, "the game ID is different "
                                                                                           "between the correct "
                                                                                           "value and at least one of "
                                                                                           "the secrets")
        self.assertNotEqual(gsecret1.animal, gsecret2.animal)
        self.assertNotEqual(gsecret3.animal, gsecret2.animal)
        self.assertNotEqual(gsecret1.animal, gsecret3.animal)
        self.assertEqual(gsecret1.animal, ObtainedCompanion.RICKY)
        self.assertEqual(gsecret2.animal, ObtainedCompanion.DIMITRI)
        self.assertEqual(gsecret3.animal, ObtainedCompanion.MOOSH)
        self.assertEqual(gsecret1.link_name, gsecret2.link_name)
        self.assertEqual(gsecret3.link_name, gsecret2.link_name)
        self.assertEqual(gsecret3.link_name, gsecret1.link_name)
        self.assertEqual(gsecret1.link_name, "LINK ")
        self.assertEqual(gsecret1.child_name, gsecret2.child_name)
        self.assertEqual(gsecret3.child_name, gsecret2.child_name)
        self.assertEqual(gsecret1.child_name, gsecret3.child_name)
        self.assertEqual(gsecret1.child_name, "PIP  ")
        self.assertEqual(gsecret1.was_given_free_ring, gsecret2.was_given_free_ring)
        self.assertEqual(gsecret1.was_given_free_ring, gsecret3.was_given_free_ring)
        self.assertEqual(gsecret3.was_given_free_ring, gsecret3.was_given_free_ring)
        self.assertFalse(gsecret1.was_given_free_ring)
