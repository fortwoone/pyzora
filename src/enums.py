from enum import IntEnum


class GameRegion(IntEnum):
    """A secret's game region.
    Note that US/PAL secrets do NOT work with Japanese ROMS,
    and vice-versa."""
    JP = 0
    US_PAL = 1


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
    BIGGORON_OR_ELDER = 8
    RUUL_OR_SYMMETRY = 9


class ChildBehaviour(IntEnum):
    """Represents Bipin and Blossom's son's state of growth and
    personality based on Link's choices."""
    NONE = 0
    CURIOUS = 1
    SHY = 2
    BOUNCY = 3


class RupeesGiven(IntEnum):
    """Represents how many Rupees you gave to Blossom to help her care for
    her child."""
    ONE = 0
    TEN = 5
    FIFTY = 5
    ONE_HUNDRED_AND_FIFTY = 8


class SleepMethod(IntEnum):
    """Represent the advice you gave to Blossom to help her son sleep."""
    SING = 0
    PLAY = 10


class ChildKind(IntEnum):
    """Represents which personality you told Blossom you had as a kid."""
    NONE = 0
    WEIRD = 1
    QUIET = 5
    HYPERACTIVE = 8


class ChildQuestion(IntEnum):
    """Represents the answer you gave to the child's question.
    The bits set are the same regardless of the question asked."""
    NO_OR_EGG = 0
    YES_OR_CHICKEN = 4
