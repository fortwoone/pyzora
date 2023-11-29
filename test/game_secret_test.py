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
        self.assertNotEqual(gsecret1.animal, gsecret2.animal)
        self.assertNotEqual(gsecret3.animal, gsecret2.animal)
        self.assertNotEqual(gsecret1.animal, gsecret3.animal)
