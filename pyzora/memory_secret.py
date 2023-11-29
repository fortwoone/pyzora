from pyzora.secret import *


class MemorySecret(BaseSecret):
    """A memory secret to transfer between two NPCS in Holodrum and Labrynna."""

    __args = ("game_id", "game_region", "target_game", "memory", "is_return_secret")
    __game_id = 0
    __target_game = TargetGame.AGES
    __memory = MemoryEnum.CLOCKSHOP_OR_KINGZORA
    __is_return = False

    def __set_memory(self, value:int):
        if value < 0:
            raise ValueError("expected a positive value")
        self.__memory = MemoryEnum(value)

    memory = property(lambda self: self.__memory, __set_memory,
                      doc="""The event tied to this secret. See MemoryEnum for more
                      details.""")

    def __set_target_game(self, value:TargetGame):
        self.__target_game = TargetGame(value)

    target_game = property(lambda self: self.__target_game, __set_target_game,
                           doc="""The secret's target game. See GameSecret.target_game
                           for more details.""")

    def __set_return(self, value:bool):
        if not isinstance(value, (bool, int, float)):
            raise TypeError("expected a boolean value")
        self.__is_return = bool(value)

    is_return_secret = property(lambda self: self.__is_return, __set_return,
                                doc="""Set this if this secret should be returned to the non-completed
                                file.""")

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

    @classmethod
    def load(cls, secret: bytearray | bytes | str, region: GameRegion):
        if isinstance(secret, str):
            # Secret string. Parse it before doing anything else.
            # Allows the user to give the region only once
            return cls.load(parse_secret(secret, region), region)
        if len(secret) != 5:
            raise SecretError("secret must contain exactly 5 bytes")
        decoded_bytes = cls.decode_bytes(secret, region)
        decoded_secret = byte_array_to_string(decoded_bytes)
        cloned_bytes = decoded_bytes.copy()
        cloned_bytes[4] = 0
        checksum = calculate_checksum(cloned_bytes)
        if (decoded_bytes[4] & 0xF) != (checksum & 0xF):
            raise ChecksumError(f"the two values ({decoded_bytes[4]} and {checksum}) do not match")
        if decoded_secret[3:5] != "11":
            raise NotAMemoryCodeError("given secret is not a memory code")
        game_id = int(reverse_substring(decoded_secret, 5, 15), 2)
        memory = MemoryEnum(int(reverse_substring(decoded_secret, 20, 4), 2))
        target_game = TargetGame(decoded_secret[24] != decoded_secret[25])
        is_return_secret = bool(int(decoded_secret[24]))
        return MemorySecret(game_id=game_id, memory=memory,
                            target_game=target_game, is_return_secret=is_return_secret)

    def __bytes__(self):
        if self.target_game:
            cipher = 2 - self.__is_return
        else:
            cipher = 3*self.__is_return
        cipher |= (self.memory & 1) << 2
        cipher = ((self.game_id >> 8) + (self.game_id & 255) + cipher) & 7
        cipher = int(reverse_string(integer_string(cipher).rjust(3, "0")), 2)
        unencoded_secret = "".join((
                integer_string(cipher).rjust(3, "0"), "11",
                reverse_string(integer_string(cipher).rjust(15, "0")),
                reverse_string(integer_string(self.memory).rjust(4, "0"))
        ))
        if self.target_game:
            mask = 1 + self.__is_return
        else:
            mask = 3*self.__is_return
        unencoded_bytes = string_to_byte_array(unencoded_secret)
        unencoded_bytes[4] = calculate_checksum(unencoded_bytes) | (mask << 4)
        return self._encode_bytes(unencoded_bytes, self.region)
