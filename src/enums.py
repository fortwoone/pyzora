from enum import IntEnum


class GameRegion(IntEnum):
    """A secret's game region.
    Note that US/PAL secrets do NOT work with Japanese ROMS,
    and vice-versa."""
    JP=0
    US_PAL=1


class TargetGame(IntEnum):
    """The game targeted by the secret."""
    AGES = 0
    SEASONS = 1


class ObtainedCompanion(IntEnum):
    """The animal friend tied to this secret."""
    NONE = 0
    RICKY = 0x0b
    DIMITRI = 0x0c
    MOOSH = 0x0d


class MemoryEnum(IntEnum):
    """The corresponding memory secret.
    Names are formatted like "A_OR_B", where A is
     the memory in linked Ages and B the memory in Linked Seasons."""
    CLOCKSHOP_OR_KINGZORA = 0
    GRAVEYARD_OR_FAIRY = 1
    SUBROSIAN_OR_TROY = 2
    DIVER_OR_PLEN = 3
    SMITH_OR_LIBRARY = 4
    PIRATE_OR_TOKAY = 5
    TEMPLE_OR_MAMAMU = 6
    DEKU_OR_TINGLE = 7
