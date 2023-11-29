"""pyzora - Python library to help parsing secrets from Zelda OoS/OoA

Base secret class.

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
import unicodedata
import re
import sys
from .enums import *
from .exceptions import *

_udata_lookup = unicodedata.lookup

U_HEART = U_GURMUKHI_THREE = _udata_lookup("GURMUKHI DIGIT THREE")
U_ASTERISK = chr(42)
U_DOLLAR_SIGN = chr(36)
U_DIAMOND = chr(9830)
U_SPADE = chr(0x2660)
U_CLUB = chr(0x2663)
U_COMMERCIAL_AT = chr(0x0040)
U_AMPERSAND = chr(0x0026)
U_PERCENT = chr(0x0025)
U_SQUARE = chr(0x25A0)
U_CIRCLE = chr(0x25CF)
U_TRIANGLE = chr(0x25B2)
U_UPWARDS_ARROW = _udata_lookup("UPWARDS ARROW")
U_DOWNWARDS_ARROW = _udata_lookup("DOWNWARDS ARROW")
U_RIGHTWARDS_ARROW = _udata_lookup("RIGHTWARDS ARROW")
U_LEFTWARDS_ARROW = _udata_lookup("LEFTWARDS ARROW")

_SYMBOL_REGEXES = (
    # Japan
    {
        r"a": "あ", r"i": "い", r"u": "う", r"e": "え", r"o": "お",
        r"ka": "か", r"ki": "き", r"ku": "く", r"ke": "け", r"ko": "こ",
        r"sa": "さ", r"si": "し", r"su": "す", r"se": "せ", r"so": "そ",
        r"ta": "た", r"ti": "ち", r"tu": "つ", r"te": "て", r"to": "と",
        r"na": "な", r"ni": "に", r"ne": "ね", r"no": "の",
        r"ha": "は", r"hi": "ひ", r"hu": "ふ", r"he": "へ", r"ho": "ほ",
        r"ma": "ま", r"mi": "み", r"mu": "む", r"me": "め", r"mo": "も",
        r"ya": "や", r"yu": "ゆ", r"yo": "よ",
        r"ra": "ら", r"ri": "り", r"ru": "る", r"re": "れ",
        r"za": "ざ",
        r"wa": "わ", r"wo": "を",
        r"ga": "が", r"go": "ご",
        r"zo": "ぞ",
        r"da": "だ", r"do": "ど",
        r"pi": "ぴ", r"pu": "ぷ", r"pe": "ぺ",
        r"bo": "ぼ",
        r"n": "ん",
        r"shi": "し",
        r"chi": "ち",
        r"tsu": "つ",
        r"fu": "ふ",
        r"\s+": ""
    },
    # US/PAL
    {
        r"\{?spade\}?": U_SPADE,
        r"\{?heart\}?": U_HEART,
        r"\{?diamond\}?": U_DIAMOND,
        r"\{?club\}?": U_CLUB,
        r"\{?circle\}?": U_CIRCLE,
        r"\{?square\}?": U_SQUARE,
        r"\{?triangle\}?": U_TRIANGLE,
        r"\{?up\}?": U_UPWARDS_ARROW,
        r"\{?down\}?": U_DOWNWARDS_ARROW,
        r"\{?left\}?": U_LEFTWARDS_ARROW,
        r"\{?right\}?": U_RIGHTWARDS_ARROW,
        r"<": "(",
        r">": ")",
        r" ": "",
    }
)

_VALID_CHARS_SELECT = (
    ('え', 'か', 'く', '0', 'け', 'つ', '1', 'し',
     'に', 'ね', 'そ', 'ぺ', '2', 'た', 'せ', 'い',
     'て', 'み', 'ほ', 'す', 'う', 'お', 'ら', 'の',
     '3', 'ふ', 'さ', 'ざ', 'き', 'ひ', 'わ', 'や',
     'こ', 'は', 'ゆ', 'よ', 'へ', 'る', 'な', 'と',
     '5', '6', '7', 'を', 'ぷ', 'も', 'め', 'り',
     'ち', 'ま', 'あ', 'ん', 'ぞ', 'れ', '8', 'ご',
     'ど', 'む', 'ぴ', '9', '4', 'ぼ', 'が', 'だ'),
    ("B", "D", "F", "G", "H", "J", "L", "M",
     "♠", "♥", "♦", "♣", "#", "N", "Q",
     "R", "S", "T", "W", "Y", "!", "●", "▲",
     "■", "+", "-", "b", "d", "f", "g", "h",
     "j", "m", "$", "*", "/", ":", "~", "n",
     "q", "r", "s", "t", "w", "y", "?", "%", "&",
     "(", "=", ")", "2", "3", "4", "5", "6", "7",
     "8", "9", "↑", "↓", "←", "→", "@",)
)


def parse_secret(secret_string: str, region: GameRegion) -> bytearray:
    """Convert a secret string into a byte array.

    :param secret_string: The secret string to convert.
    :param region: The game region to use. Be aware that not
    setting the correct region before parsing might net you some unexpected errors.
    :raise SecretError: if the secret string contains invalid symbols.
    """
    for key, value in _SYMBOL_REGEXES[region].items():
        secret_string = re.sub(key, value, secret_string, 0, re.IGNORECASE)
    secret_length = len(secret_string)  # storing that to avoid iterating over the string twice
    data = bytearray(secret_length)
    for pos, value in enumerate(secret_string):
        try:
            symbol = _VALID_CHARS_SELECT[region.value].index(value)
            if symbol < 0 or symbol > 63:
                raise SecretError(f"Secret contains invalid value : {value}")
        except ValueError:
            # There's a chance the user has used the wrong region
            raise SecretError(f"Secret contains invalid value : {value}. Perhaps you used the wrong region?")
        data[pos] = symbol
    return data


def create_string(data: bytearray, region: GameRegion) -> str:
    """Produces a secret string from a byte array with a given region.

    :param data: The array to convert.
    :param region: The game region to use during conversion.
    :raise SecretError: if the byte array contains invalid values."""
    secret_chars = []
    for pos, value in enumerate(data):
        if value > 63:
            raise SecretError("given data contains invalid values")
        secret_chars.append(_VALID_CHARS_SELECT[region][value])
        if pos % 5 == 4:
            secret_chars.append(" ")
    return "".join(secret_chars)


def calculate_checksum(secret: bytearray) -> int:
    """Calculate the checksum for a given secret."""
    return sum(secret) & 0xF


def transform_byte_to_bitstring(byte: int) -> str:
    """Return a bitstring from a byte integer."""
    return bin(byte)[2:].rjust(6, "0")


def byte_array_to_string(array: bytearray) -> str:
    return "".join(map(transform_byte_to_bitstring, array))


def _byte(integer: str):
    byteorder = sys.byteorder
    return int.from_bytes(bytearray(int(integer, 2).to_bytes(1, byteorder)), byteorder)


Byte = _byte  # Name aliasing since these functions need to act as a class
Byte.__name__ = "Byte"
Byte.__qualname__ = Byte.__qualname__.replace("_b", "B")


def string_to_byte_array(string: str):
    secret_length = len(string) // 6 + 1
    secret = bytearray(secret_length)
    for x in range(secret_length):
        multi = x * 6
        substr = string[multi: multi + 6]
        if not substr:
            break
        else:
            secret[x] = Byte(substr)
    return secret


def reverse_substring(string, start, length):
    return "".join(reversed(string[start: start + length]))


def integer_string(number: int) -> str:
    """Return the binary string for an integer."""
    return bin(number)[2:]  # starting at the third character to skip the prefix


def reverse_string(string: str) -> str:
    """Return the reversed version of a string."""
    return "".join(reversed(string))


class BaseSecret:
    """Base secret class for all secret objects.

    This class contains all base methods other secret classes can rely on.
    It should not be instantiated directly."""
    _CIPHERS = (
        # Japan
        bytes((0x31, 0x09, 0x29, 0x3b, 0x18, 0x3c, 0x17, 0x33,
               0x35, 0x01, 0x0b, 0x0a, 0x30, 0x21, 0x2d, 0x25,
               0x20, 0x3a, 0x2f, 0x1e, 0x39, 0x19, 0x2a, 0x06,
               0x04, 0x15, 0x23, 0x2e, 0x32, 0x28, 0x13, 0x34,
               0x10, 0x0d, 0x3f, 0x1a, 0x37, 0x0f, 0x3e, 0x36,
               0x38, 0x02, 0x16, 0x3d, 0x2c, 0x0e, 0x1b, 0x12)),
        # US/PAL
        bytes(
            (21, 35, 46, 4, 13, 63, 26, 16,
             58, 47, 30, 32, 15, 62, 54, 55,
             9, 41, 59, 49, 2, 22, 61, 56,
             40, 19, 52, 50, 1, 11, 10, 53,
             14, 27, 18, 44, 33, 45, 37, 48,
             25, 42, 6, 57, 60, 23, 51, 24)
        )
    )
    __game_id = 0  # Can be any possible value between 0 and 32766.
    __region = GameRegion.US_PAL
    __required_length__ = 0

    def __set_game_id(self, value: int):
        if value > 32766 or value < 0:
            raise SecretError(f"invalid game ID : {value}")
        self.__game_id = value

    game_id = property(lambda self: self.__game_id, __set_game_id,
                       doc="""The secret's game ID. A game ID is generated upon creating
                       a normal save file in either Ages or Seasons, and is kept when using a secret
                       to start a linked save in the other game. After being first input
                       through the Labrynna/Holodrum secret, this ID will be compared
                       against further secret inputs' game IDs, which means that all further
                       secrets will have to use the same ID.""")

    def __set_region(self, value: GameRegion | int):
        self.__region = GameRegion(value)

    region = property(lambda self: self.__region, __set_region,
                      doc="""The secret's region. It's needed to parse correctly
                      data for a given secret string.""")

    def __bytes__(self):
        """Convert self to a byte array."""
        return bytes(20)

    def __hash__(self):
        return hash((self.__game_id, self.__region))

    def __str__(self):
        """Return a password string from self.

        WARNING : PLEASE NOTE THAT OUTPUT SECRET STRINGS MIGHT
        BE DIFFERENT FROM THE INPUT SECRET. IN MOST CASES,
        YOU DON'T NEED TO BOTHER ABOUT IT, SINCE THE INFORMATION STORED
        WILL BE THE SAME. YOU CAN CHECK WITH AN EQUALITY TEST IF THE
        OUTPUT IS DIFFERENT."""
        return create_string(bytearray(bytes(self)), self.__region)

    def __eq__(self, other: "BaseSecret"):
        if type(self) is not type(other):
            return False
        return self.game_id == other.game_id and other.region == self.region

    @classmethod
    def _encode_bytes(cls, data: bytearray, region: GameRegion):
        """Encode the given data."""
        cipher_key = data[0] >> 3
        cipher_pos = cipher_key * 4
        secret = bytearray(len(data))
        cipher = cls._CIPHERS[region]
        for key, value in enumerate(data):
            secret[key] = value ^ cipher[cipher_pos + key]
        secret[0] = (secret[0] & 7) | (cipher_key << 3)
        return secret

    __repr__ = __str__

    @classmethod
    def decode_bytes(cls, secret: bytearray | str, region: GameRegion):
        """Decode a secret string or byte array with a certain region."""
        if isinstance(secret, str):
            bsecret = bytes(secret, "utf-8")
        else:
            bsecret = bytes(secret)
        cipher = cls._CIPHERS[region.value]
        cipher_key = bsecret[0] >> 3
        cipher_pos = cipher_key * 4
        decoded_bytes = bytearray(len(bsecret))
        for key, value in enumerate(bsecret):
            decoded_bytes[key] = value ^ cipher[cipher_pos + key]
        decoded_bytes[0] &= 7 | (cipher_key << 3)
        return decoded_bytes
