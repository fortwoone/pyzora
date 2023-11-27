import unicodedata
import re
from .enums import *

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
_VALID_JPCHARS = bytes(map(ord, ('え', 'か', 'く', '0', 'け', 'つ', '1', 'し',
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

def parse_secret(secret_string:str, region:GameRegion) -> bytearray:
    """Convert a secret string into a byte array.

    :param secret_string: The secret string to convert.
    :param region: The game region to use. Be aware that not setting the correct region before parsing might net you some unexpected errors.
    """

