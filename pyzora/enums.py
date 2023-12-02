"""pyzora - Python library to help parsing secrets from Zelda OoS/OoA

All enums used by the library. Check each one's documentation for more details.

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
License along with pyzora. If not, see <https://www.gnu.org/licenses/>."""
from enum import IntEnum


class GameRegion(IntEnum):
    """A secret's game region.
    Note that US/PAL secrets do NOT work with Japanese ROMS,
    and vice-versa."""

    JP = 0
    """Indicates the current operation should be realised with the Japanese ciphers."""

    US_PAL = 1
    """Indicates the current operation should be achieved using the international ciphers (
    US and PAL cartridges use the same characters and encryption-decryption methods)."""


class TargetGame(IntEnum):
    """The game targeted by the secret, represented by one bit in the secret
    (position differs depending on the secret type).

    Secrets meant for one game will not work with the other one.
    This is only relevant for game and memory secrets, since ring secrets are
    game-independent."""

    AGES = 0
    """Indicates the current secret's target game is Oracle of Ages."""

    SEASONS = 1
    """Indicates the current secret's target game is Oracle of Seasons."""


class ObtainedCompanion(IntEnum):
    """The animal friend tied to this secret.

    The NONE value technically is possible to encounter in Hero's Secrets,
    but its use is otherwise discouraged, bar non-linked secrets.
    You might end up with unexpected results otherwise."""

    NONE = 0
    """The player has no animal friend yet. This value normally only gets used in
    Hero's Secrets (non-Hero secrets should also work with this value, provided
    they aren't linked)."""

    RICKY = 0x0b
    """The player has obtained Ricky the Kangaroo's Flute in the completed file."""

    DIMITRI = 0x0c
    """The player has obtained Dimitri the Dodongo's Flute in the finished save."""

    MOOSH = 0x0d
    """The player obtained Moosh the Flying Bear's Flute in the original file."""


class MemoryEnum(IntEnum):
    """The corresponding memory secret.
    Names are formatted like "A_OR_B", where A is
    the memory in linked Ages and B the memory in Linked Seasons.
    Each member's description explains the name chosen for it."""

    CLOCKSHOP_OR_KINGZORA = 0
    """Ages : in Present Labrynna, just south of the Lynna Shop, an old woman spawns
    and tells you to dig behind the Clock Shop in Horon Village after you complete 
    the Wing Dungeon.
    
    Seasons : a Zora spawns in Hero's Cave after you get the Roc's Feather in 
    Poison Moth's Lair, and tells you to meet King Zora in Labrynna."""

    GRAVEYARD_OR_FAIRY = 1
    """Ages : in Present Labrynna, a Ghini spawns under Syrup's Potion Shop in
    the Yoll Graveyard after you complete Spirit's Grave. It tells you to find another
    Ghini under a flowerless grave in the Western Coast Graveyard in Holodrum.
    
    Seasons : right after you talk with the Maku Tree for the first time, a woman spawns next to Horon Village's fountain. 
    She wants you to tell the "happiness" secret to the Blue Fairy in Fairies' Woods in Labrynna."""

    SUBROSIAN_OR_TROY = 2
    """Ages : after you beat the Crown Dungeon, a Subrosian appears in a cave in eastern
    Rolling Ridge in the present. He asks you to get in touch with his golden brother back in Subrosia.
    
    Seasons : after you complete Poison Moth's Lair, a kid spawns in the Eastern Suburbs.
    He gives you a secret to give to Dr. Troy in Present Labrynna, who went to the Target Carts in Rolling Ridge."""

    DIVER_OR_PLEN = 3
    """Ages : after you beat Mermaid's Cave, a diver spawns above Zora Village in the present. He asks you to tell a 
    secret to the Master Diver, who lives in the Sunken City in Holodrum.
    
    Seasons : once you get the Rod of Seasons infused with the Power of Autumn, a golden Subrosian spawns at Lava 
    Lake. He wants you to go thank Mayor Plen in Lynna City in his stead."""

    SMITH_OR_LIBRARY = 4
    """Ages : after you complete the Crown Dungeon, a Subrosian spawns next to the
    Mysterious Tree at eastern Rolling Ridge in the past. He gives you a secret to 
    tell to the Subrosian Smithy.
    
    Seasons : after you help the Piratians, a Ghini spawns inside the deserted house
    on the Western Coast. It tells you a secret to carry to the Eyeglass Isle Library in past Labrynna."""

    PIRATE_OR_TOKAY = 5
    """Ages : a little girl spawns just south of the Black Tower in the past after you get the Roc's Feather in the 
    Wing Dungeon. She wants you to give her luck secret to one of the Piratians still stranded on Subrosia, because she
    forgot to gave it to him earlier.
    
    Seasons : after destroying Moblin's Keep and visiting their refuge in the Sunken City, a Moblin will spawn in the fortress's
    ruins and tell you a secret to be passed to the Wild Tokay Museum curator on Crescent Island in the present."""

    TEMPLE_OR_MAMAMU = 6
    """Ages : after you complete the Wing Dungeon, a Fairy appears over its ruins in Fairies' Woods. She has a secret for you
    to give to another Fairy living in the innermost room of the Temple of Seasons.
    
    Seasons : once you complete Poison Moth's Lair, an old woman will spawn inside the Floodgate Keeper's house.
    Her secret will have to be carried to Mamamu Yan, who lives in Lynna City in the present."""

    DEKU_OR_TINGLE = 7
    """Ages : after you complete the Spirit's Grave, a Deku Scrub spawns in the Deku Forest in the past. It sings a 
    then-popular song, and the end of it is a secret. You will need to give it to another Deku Scrub living near Moblin's 
    Keep in Holodrum.
    
    Seasons : after completing Snake's Remains, a Fairy will spawn in a cave east of the dungeon. She has a secret
    for you to tell to Tingle, who's living in the Forest of Time in present Labrynna."""

    BIGGORON_OR_ELDER = 8
    """Ages : once you beat the Crown Dungeon, a Goron will spawn in a cave in eastern Rolling Ridge in the present.
    He has a secret you need to pass on to Biggoron, who can be reached atop Goron Mountain in Holodrum.
    
    Seasons : after you cure Biggoron's cold with the Lava Soup, a red Goron will spawn in a cave right under Biggoron.
    He wants you to ask his ancestor (found in the Goron Shooting Gallery) in the past the meaning of a secret he found in 
    his ancestor's diary."""

    RUUL_OR_SYMMETRY = 9
    """Ages : once you beat the Wing Dungeon, Mayor Plen's grandmother appears alongside him in his house. She has a secret 
    you will need to tell to Mayor Ruul in Horon Village.
    
    Seasons : after beating the Snake's Remains, a girl spawns in Holly's house in Holodrum. She wants you to thank the authors
    of her favourite book, the Middle House Twins from Symmetry Village, by telling them a touching secret."""


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
    TEN = 2
    FIFTY = 5
    ONE_HUNDRED_AND_FIFTY = 8


class SleepMethod(IntEnum):
    """Represent the method you recommended to Blossom to help her son sleep."""
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
