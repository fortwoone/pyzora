from more_itertools import *


class __NoRingsType:
    """A singleton representing a game with no rings obtained."""
    __INST = 0
    __slots__ = ()

    def __new__(cls):
        if not cls.__INST:
            cls.__INST += 1
            return super().__new__(cls)
        else:
            return NoRings

    def __del__(self):
        self.__class__.__INST -= 1

    def __or__(self, other):
        return int(self) | other

    def __ror__(self, other):
        return self.__or__(other)

    def __int__(self):
        return 0

    def __bool__(self):
        return False


NoRings = __NoRingsType()


class RingType:
    def __init__(self, integer, name, description):
        self.integer, self.name, self.description = integer, name, description

    def __repr__(self):
        return self.name

    def __int__(self):
        return self.integer

    def __and__(self, other):
        return int(self) & other

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        return int(self) | other

    def __ror__(self, other):
        return self.__or__(other)

    def __eq__(self, other):
        if type(self) is type(other):
            return self is other
        return int(self) == int(other)

    @classmethod
    def from_integer(cls, integer:int):
        """Returns the first ring type with the corresponding integer.
        If nothing matches, NoRings is returned instead."""
        if integer > int(AllRings):
            raise ValueError("given value exceeds AllRings' value")
        elif integer < 0:
            raise ValueError("given value is negative")
        return first(filter(lambda tp:integer == tp.integer, RING_TYPES), NoRings)


class __AllRingsType:
    """A singleton representing all obtainable rings in a game."""
    __INST = 0
    __slots__ = ()

    def __new__(cls):
        if not cls.__INST:
            cls.__INST += 1
            return super().__new__(cls)
        else:
            return AllRings

    def __del__(self):
        self.__class__.__INST -= 1

    def __or__(self, other):
        return int(self) | other

    __ror__ = __or__

    def __int__(self):
        return 18446744073709551615

    def __bool__(self):
        return True


AllRings = __AllRingsType()

FRIENDSHIP = RingType(0x1, "Friendship Ring", "Symbol of a meeting")
POWER_1 = RingType(0x2, "Power Ring L-1", "Sword damage ▲\nDamage taken ▲")
POWER_2 = RingType(0x4, "Power Ring L-2", "Sword damage ▲▲\nDamage taken ▲▲")
POWER_3 = RingType(0x8, "Power Ring L-3", "Sword damage ▲▲▲\nDamage taken ▲▲▲")
ARMOUR_1 = RingType(0x10, "Armour Ring L-1", "Sword Damage ▼\nDamage taken ▼")
ARMOUR_2 = RingType(0x20, "Armour Ring L-2", "Sword Damage ▼▼\nDamage taken ▼▼")
ARMOUR_3 = RingType(0x40, "Armour Ring L-3", "Sword Damage ▼▼▼\nDamage taken ▼▼▼")
RED = RingType(0x80, "Red Ring", "Sword Damage x2")
BLUE = RingType(0x100, "Blue Ring", "Damage taken reduced by 1/2")
GREEN = RingType(0x200, "Green Ring", "Damage taken down by 25%\nSword damage up by 50%")
CURSED = RingType(0x400, "Cursed Ring", "1/2 sword damage\nx2 damage taken")
EXPERTS_RING = RingType(0x800, "Expert's Ring", "Punch when unequipped")
BLAST_RING = RingType(0x1000, "Blast Ring", "Bomb damage ▲")
RANG1 = RingType(0x2000, "Rang Ring L-1", "Boomerang damage ▲")
GBA_TIME = RingType(0x4000, "GBA Time Ring", "Life Advanced!")
MAPLES_RING = RingType(0x8000, "Maple's Ring", "Maple meetings ▲")
STEADFAST = RingType(0x10000, "Steadfast Ring", "Get knocked back less")
PEGASUS = RingType(0x20000, "Pegasus Ring", "Lengthen Pegasus Seed effect")
TOSS_RING = RingType(0x40000, "Toss Ring", "Throwing distance ▲")
HEART1 = RingType(0x80000, "Heart Ring L-1", "Slowly recover lost Hearts")
HEART2 = RingType(0x100000, "Heart Ring L-2", "Recover lost Hearts")
SWIMMERS_RING = RingType(0x200000, "Swimmer's Ring", "Swimming speed ▲")
CHARGE_RING = RingType(0x400000, "Charge Ring", "Spin Attack charges quickly")
LIGHT1 = RingType(0x800000, "Light Ring L-1", "Sword beams at -2 Hearts")
LIGHT2 = RingType(0x1000000, "Light Ring L-2", "Sword beams at -3 Hearts")
BOMBERS_RING = RingType(0x2000000, "Bomber's Ring", "Set two Bombs at once")
GREEN_LUCK = RingType(0x4000000, "Green Luck Ring", "1/2 damage from traps")
BLUE_LUCK = RingType(0x8000000, "Blue Luck Ring", "1/2 damage from beams")
GOLD_LUCK = RingType(0x10000000, "Gold Luck Ring", "1/2 damage from falls")
RED_LUCK = RingType(0x20000000, "Red Luck Ring", "1/2 damage from spiked floors")
GREEN_HOLY = RingType(0x40000000, "Green Holy Ring", "No damage from electricity")
BLUE_HOLY = RingType(0x80000000, "Blue Holy Ring", "No damage from Zora's fire")
RED_HOLY = RingType(0x100000000, "Red Holy Ring", "No damage from small rocks")
SNOWSHOE = RingType(0x200000000, "Snowshoe Ring", "No sliding on ice")
ROCS_RING = RingType(0x400000000, "Roc's Ring", "Cracked floors don't crumble")
QUICKSAND = RingType(0x800000000, "Quicksand Ring", "No sinking in quicksand")
RED_JOY = RingType(0x1000000000, "Red Joy Ring", "Beasts drop double Rupees")
BLUE_JOY = RingType(0x2000000000, "Blue Joy Ring", "Beasts drop double Hearts")
GOLD_JOY = RingType(0x4000000000, "Gold Joy Ring", "Find double items")
GREEN_JOY = RingType(0x8000000000, "Green Joy Ring", "Find double Ore Chunks")
DISCOVERY = RingType(0x10000000000, "Discovery Ring", "Sense soft earth nearby")
RANG2 = RingType(0x20000000000, "Rang Ring L-2", "Boomerang damage ▲▲")
OCTO = RingType(0x40000000000, "Octo Ring", "Become an Octorok")
MOBLIN = RingType(0x80000000000, "Moblin Ring", "Become a Moblin")
LIKE_LIKE = RingType(0x100000000000, "Like Like Ring", "Become a Like-Like")
SUBROSIAN = RingType(0x200000000000, "Subrosian Ring", "Become a Subrosian")
GEN1 = RingType(0x400000000000, "First Gen Ring", "Become something")
SPIN = RingType(0x800000000000, "Spin Ring", "Double Spin Attack")
BOMBPROOF = RingType(0x1000000000000, "Bombproof Ring", "No damage from your own Bombs")
ENERGY = RingType(0x2000000000000, "Energy Ring", "Beam replaces Spin Attack")
DOUBLE_EDGED = RingType(0x4000000000000, "Dbl. Edge Ring", "Sword damage ▲ but you get hurt")
GBA_NATURE = RingType(0x8000000000000, "GBA Nature Ring", "Life Advanced!")
SLAYER = RingType(0x10000000000000, "Slayer's Ring", "1000 beasts slain")
RUPEE = RingType(0x20000000000000, "Rupee Ring", "10,000 Rupees collected")
VICTORY = RingType(0x40000000000000, "Victory Ring", "The Evil King Ganon defeated")
SIGN = RingType(0x80000000000000, "Sign Ring", "100 signs broken")
HUNDREDTH = RingType(0x100000000000000, "100th Ring", "100 rings appraised")
WHISP = RingType(0x200000000000000, "Whisp Ring", "No effect from jinxes")
GASHA = RingType(0x400000000000000, "Gasha Ring", "Grow great Gasha Trees")
PEACE = RingType(0x800000000000000, "Peace Ring", "No explosion if holding Bomb")
ZORA = RingType(0x1000000000000000, "Zora Ring", "Dive without breathing")
FIST = RingType(0x2000000000000000, "Fist Ring", "Punch when not equipped")
WHIMSICAL = RingType(0x4000000000000000, "Whimsical Ring", "Sword damage ▼ Sometimes deadly")
PROTECTION = RingType(0x8000000000000000, "Protection Ring", "Damage taken is always one Heart")


RING_TYPES = (FRIENDSHIP, POWER_1, POWER_2, POWER_3, ARMOUR_1,
              ARMOUR_2, ARMOUR_3, RED, BLUE, GREEN, CURSED, EXPERTS_RING,
              BLAST_RING, RANG1, GBA_TIME, MAPLES_RING, STEADFAST,
              PEGASUS, TOSS_RING, HEART1, HEART2, SWIMMERS_RING,
              CHARGE_RING, LIGHT1, LIGHT2, BOMBERS_RING, GREEN_LUCK,
              BLUE_LUCK, GOLD_LUCK, RED_LUCK, GREEN_HOLY, BLUE_HOLY,
              RED_HOLY, SNOWSHOE, ROCS_RING, QUICKSAND, RED_JOY,
              BLUE_JOY, GOLD_JOY, GREEN_JOY, DISCOVERY, RANG2, OCTO,
              MOBLIN, LIKE_LIKE, SUBROSIAN, GEN1, SPIN, BOMBPROOF,
              ENERGY, DOUBLE_EDGED, GBA_NATURE, SLAYER, RUPEE,
              VICTORY, SIGN, HUNDREDTH, WHISP, GASHA, PEACE, ZORA, FIST,
              WHIMSICAL, PROTECTION)
