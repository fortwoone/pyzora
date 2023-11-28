from pyzora.secret import *
from pyzora.ring_types import *


class RingSecret(BaseSecret):
    """A ring secret. Ring secrets can be used to transfer a player's ring
    collection from one game to another.

    You can check if a ring is contained in a secret with the 'in' keyword.

    For example, if you want to check if the player already has the Friendship
    Ring, you can do this :

    if FRIENDSHIP in secret:
        do_whatever_you_want()"""
    __args = ("game_id", "rings", "ring_str")
    __rings = 0
    __ring_str = ""

    def __set_rings(self, value: int):
        if value > int(AllRings):
            raise ValueError("cannot set a value higher than AllRings")
        if value < 0:
            raise ValueError("value must be an unsigned integer")
        # Converting the parameter into an integer in case we've been given a RingType instance
        self.__rings = int(value)
        self.__ring_str = bin(int(value))[2:].rjust(64, "0")

    rings = property(lambda self: self.__rings, __set_rings,
                     doc="""Get the rings stored in the secret as an integer.""")

    @property
    def ring_count(self):
        """Count how many rings the player has."""
        return self.__ring_str.count("1")

    def __init__(self, *args, **kwargs):
        for pos, arg in enumerate(self.__args):
            kwargs.setdefault(arg, None)
            if kwargs.get(arg) is None:
                try:
                    setattr(self, arg, args[pos])
                except Exception:
                    pass
            else:
                try:
                    setattr(self, arg, kwargs.get(arg))
                except Exception:
                    pass

    def __contains__(self, item):
        if item is NoRings:
            return not self.rings
        elif item is AllRings:
            return self.rings == int(AllRings)
        else:
            return item | self.rings

    @classmethod
    def load(cls, secret: bytearray | bytes, region: GameRegion):
        """Load a secret encoded with a certain region."""
        if len(secret) != 15:
            raise SecretError("secret is expected to have exactly 15 bytes")
        decoded_bytes = cls.decode_bytes(secret, region)
        decoded_secret = byte_array_to_string(decoded_bytes)
        cloned_bytes = decoded_bytes.copy()
        cloned_bytes[14] = 0
        checksum = calculate_checksum(cloned_bytes)
        if (decoded_bytes[14] & 0xF) != (checksum & 0xF):
            raise ChecksumError(f"checksum {checksum} does not match expected value : {decoded_bytes[14]}")
        if decoded_secret[3] != "0" or decoded_secret[4] != "1":
            raise NotARingCodeError(f"given secret is not a ring code")
        game_id = int(reverse_substring(decoded_secret, 5, 15))
        ring_str = "".join((reverse_substring(decoded_secret, 36, 8),
                            reverse_substring(decoded_secret, 76, 8),
                            reverse_substring(decoded_secret, 28, 8),
                            reverse_substring(decoded_secret, 60, 8),
                            reverse_substring(decoded_secret, 44, 8),
                            reverse_substring(decoded_secret, 68, 8),
                            reverse_substring(decoded_secret, 20, 8),
                            reverse_substring(decoded_secret, 52, 8)))
        rings = int(ring_str, base=2)
        return RingSecret(game_id=game_id, rings=rings, ring_str=ring_str)

    def __bytes__(self):
        ring_row1 = self.rings
        ring_row2 = ring_row1 >> 8
        ring_row3 = ring_row1 >> 16
        ring_row4 = ring_row1 >> 24
        ring_row5 = ring_row1 >> 32
        ring_row6 = ring_row1 >> 40
        ring_row7 = ring_row1 >> 48
        ring_row8 = ring_row1 >> 56
        cipher_key = ((self.game_id >> 8) + (self.game_id & 255)) & 7
        unencoded_secret = (
                reverse_string(integer_string(cipher_key).rjust(3, "0")) + "01"
        )
        secret_strings = map(reverse_string, (
            integer_string(self.game_id).rjust(15, "0"),
            integer_string(ring_row2).rjust(8, "0"),
            integer_string(ring_row6).rjust(8, "0"),
            integer_string(ring_row8).rjust(8, "0"),
            integer_string(ring_row4).rjust(8, "0"),
            integer_string(ring_row1).rjust(8, "0"),
            integer_string(ring_row5).rjust(8, "0"),
            integer_string(ring_row3).rjust(8, "0"),
            integer_string(ring_row7).rjust(8, "0"),
        ))
        unencoded_secret += "".join(secret_strings)
        unencoded_bytes = string_to_byte_array(unencoded_secret)
        del (
            ring_row1,
            ring_row2,
            ring_row3,
            ring_row4,
            ring_row5,
            ring_row6,
            ring_row7,
            ring_row8,
            secret_strings,
            unencoded_secret,
        )
        unencoded_bytes[14] = calculate_checksum(unencoded_bytes)
        secret = self._encode_bytes(unencoded_bytes, self.region)
        return bytes(secret)

    def to_list(self):
        """Return self as a list of ring types."""
        return list(filter(lambda tp:tp.integer | self.__rings, RING_TYPES))

    def __hash__(self):
        return hash((self.__game_id, self.__rings))

