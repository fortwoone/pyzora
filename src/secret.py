import unicodedata
import re
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

_VALID_CHARS = bytes(
    (0x41,
     0x42,
     0x43,
     0x44,
     0x45,
     0x46,
     0x47,
     0x48,
     0x49,
     0x4A,
     0x4B,
     0x4C,
     0x4D,
     0x4E,
     0x4F,
     0x50,
     0x51,
     0x52,
     0x53,
     0x54,
     0x55,
     0x56,
     0x57,
     0x58,
     0x59,
     0x5A,
     0x20,
     0x2E,
     0x2C,
     0x5F,
     0x80,
     0x81,
     0x82,
     0x83,
     0x84,
     0x20,
     0x85,
     0x86,
     0x87,
     0x88,
     0x89,
     0x8A,
     0x8B,
     0x8C,
     0x8D,
     0x8E,
     0x8F,
     0x90,
     0x21,
     0x27,
     0x2D,
     0x3A,
     0x3B,
     0x3D,
     0x11,
     0x12,
     0xBD,
     0x13,
     0x28,
     0x29,
     0x00,
     0x61,
     0x62,
     0x63,
     0x64,
     0x65,
     0x66,
     0x67,
     0x68,
     0x69,
     0x6A,
     0x6B,
     0x6C,
     0x6D,
     0x6E,
     0x6F,
     0x70,
     0x71,
     0x72,
     0x73,
     0x74,
     0x75,
     0x76,
     0x77,
     0x78,
     0x79,
     0x7A,
     0x20,
     0x2E,
     0x2C,
     0x5F,
     0xA0,
     0xA1,
     0xA2,
     0xA3,
     0xA4,
     0x20,
     0xA5,
     0xA6,
     0xA7,
     0xA8,
     0xA9,
     0xAA,
     0xAB,
     0xAC,
     0xAD,
     0xAE,
     0xAF,
     0xB0,
     0x21,
     0x27,
     0x2D,
     0x3A,
     0x3B,
     0x3D,
     0x11,
     0x12,
     0xBD,
     0x13,
     0x28,
     0x29,
     0x00,)
)
_VALID_JPCHARS = tuple(map(ord, ('え', 'か', 'く', '0', 'け', 'つ', '1', 'し',
                                 'に', 'ね', 'そ', 'ぺ', '2', 'た', 'せ', 'い',
                                 'て', 'み', 'ほ', 'す', 'う', 'お', 'ら', 'の',
                                 '3', 'ふ', 'さ', 'ざ', 'き', 'ひ', 'わ', 'や',
                                 'こ', 'は', 'ゆ', 'よ', 'へ', 'る', 'な', 'と',
                                 '5', '6', '7', 'を', 'ぷ', 'も', 'め', 'り',
                                 'ち', 'ま', 'あ', 'ん', 'ぞ', 'れ', '8', 'ご',
                                 'ど', 'む', 'ぴ', '9', '4', 'ぼ', 'が', 'だ')))

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

_VALID_CHAR_SELECT = (_VALID_JPCHARS, _VALID_CHARS)


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
    symbol = 0
    for pos, value in enumerate(secret_string):
        try:
            symbol = _VALID_CHAR_SELECT[region].index(value)
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
        secret_chars.append(_VALID_CHAR_SELECT[region][value])
        if pos % 5 == 4:
            secret_chars.append(" ")
    return "".join(secret_chars)


def calculate_checksum(secret: bytearray) -> int:
    """Calculate the checksum for a given secret."""
    return sum(secret) & 0xF


def transform_byte_to_bitstring(byte:int) -> str:
    """Return a bitstring from a byte integer."""
    return bin(byte)[2:].rjust(6, "0")


def byte_array_to_string(array:bytearray) -> str:
    return "".join(map(transform_byte_to_bitstring, array))


def Byte(integer: str):
    byteorder = sys.byteorder
    return int.from_bytes(bytearray(int(integer, 2).to_bytes(1, byteorder)), byteorder)


def string_to_byte_array(string: str):
    secret_length = len(string) // 6 + 1
    secret = bytearray(secret_length)
    for x in range(secret_length):
        multi = x * 6
        substr = string[multi : multi + 6]
        if not substr:
            break
        else:
            secret[x] = Byte(substr)
    return secret


class BaseSecret:
    """Base secret class for all secret objects."""
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

    game_id = property(lambda self:self.__game_id, __set_game_id,
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
        return create_string(bytearray(self), self.__region)

    def __eq__(self, other: "BaseSecret"):
        if type(self) is not type(other):
            return False
        return self.game_id == other.game_id and other.region == self.region

    @classmethod
    def _encode_bytes(cls, data: bytearray, region:GameRegion):
        """Encode the given data."""
        cipher_key = data[0] >> 3
        cipher_pos = cipher_key * 4
        secret = bytearray(len(data))
        cipher = cls._CIPHERS[region]
        for key, value in enumerate(data):
            secret[key] = value ^ cipher[cipher_pos + key]
        secret[0] = (secret[0] & 7) | (cipher_key << 3)
        return secret

    @classmethod
    def decode_bytes(cls, secret:bytearray | str, region:GameRegion):
        """Decode a secret string or byte array with a certain region."""
        bsecret = bytes(secret, "utf-8")
        cipher = cls._CIPHERS[region]
        cipher_key = bsecret[0] >> 3
        cipher_pos = cipher_key * 4
        decoded_bytes = bytearray(len(bsecret))
        for key, value in enumerate(bsecret):
            decoded_bytes[key] = value ^ cipher[cipher_pos + key]
        decoded_bytes[0] &= 7 | (cipher_key << 3)
        return decoded_bytes
