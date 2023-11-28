from src.secret import *
import copy as mod_copy


class GameSecret(BaseSecret):
    """A secret used to start a game."""

    __link_name = "\0" * 5
    __child_name = mod_copy.deepcopy(__link_name)
    __behaviour = bytearray((0,))
    __animal = mod_copy.deepcopy(__behaviour)
    __target_game = mod_copy.deepcopy(__behaviour)
    __is_hero_quest = False
    __is_linked_game = False
    __was_given_free_ring = False

    __args = (
        "game_id",
        "target_game",
        "link_name",
        "child_name",
        "animal",
        "behaviour",
        "is_linked_game",
        "is_hero_quest",
        "was_given_free_ring",
        "secret_array",
        "checksum",
        "secret_string",
    )

    def __init__(self, *args, **kwargs):
        for arg in self.__args:
            kwargs.setdefault(arg, None)
        for pos, arg in enumerate(self.__args):
            val = kwargs[arg]
            if val is None:
                try:
                    setattr(self, arg, args[pos])
                except Exception:
                    pass
            else:
                try:
                    setattr(self, arg, val)
                except Exception:
                    pass

    def __set_target_game(self, value: TargetGame | int):
        self.__target_game = TargetGame(value)

    target_game = property(lambda self: self.__target_game, __set_target_game,
                           doc="""The game the secret is meant for.
                           If you attempt inputting a secret meant for Ages in Seasons,
                           for example, the input will fail.""")

    def __set_hero_quest(self, value:bool):
        self.__is_hero_quest = value

    is_hero_quest = property(lambda self: self.__is_hero_quest, __set_hero_quest,
                             doc="""A Hero's Secret allows the player to start
                             the game anew and get a special ring.""")

    def __set_linked_game(self, value:bool):
        self.__is_linked_game = value

    is_linked_game = property(lambda self:self.__is_linked_game, __set_linked_game,
                              doc="""If a game is linked, some additional events will happen in the 
                              target game.""")

    def __set_link_name(self, value: str):
        if len(value.strip()) > 5:
            raise ValueError(f"incorrect name for Link : {value}")
        self.__link_name = value.strip().ljust(5, "\0")

    link_name = property(lambda self:self.__link_name, __set_link_name,
                         doc="""Link's name. Takes at most 5 characters to fit in the secret.""")

    def __set_child_name(self, value:str):
        self.__child_name = value.strip().ljust(5, "\0")

    child_name = property(lambda self:self.__child_name, __set_child_name,
                          doc="""Game secrets also store Bipin and Blossom's child's
                          name.""")

    def __set_animal(self, value: ObtainedCompanion | int):
        self.__animal = ObtainedCompanion(value)

    animal = property(lambda self:self.__animal, __set_animal,
                      doc="""The companion Link has obtained.
                      During linked games, this should be set.
                      In linked games, the companion stored in the secret will
                      recognise Link and give him his flute again.""")

    def __get_behaviour(self):
        return self.__behaviour[0]

    def __set_behaviour(self, value):
        self.__behaviour = bytearray((int(value), ))

    behaviour = property(__get_behaviour, __set_behaviour,
                         doc="""Bipin and Blossom's child's behaviour is carried over 
                         through secrets. The same length restrictions as for Link's name
                         apply for the kid's name.""")

    def __set_free_ring_given(self, value: bool):
        self.__was_given_free_ring = value

    was_given_free_ring = property(lambda self: self.__was_given_free_ring, __set_free_ring_given,
                                   doc="""This should be set if the player has already received
                                   the Friendship Ring from Vasu.""")

    @classmethod
    def load(cls, secret: bytes | bytearray) -> "GameSecret":
        """Load a game secret from bytes or a string."""
        if len(secret) != 20:
            raise SecretError("secret must contain exactly 20 bytes")
        decoded_bytes = cls.decode_bytes(secret)
        decoded_secret = byte_array_to_string(decoded_bytes)
        cloned_bytes = mod_copy.deepcopy(decoded_bytes)
        cloned_bytes[19] = 0
        checksum = calculate_checksum(cloned_bytes)
        if decoded_bytes[19] & 0xF != checksum & 0xF:
            raise ChecksumError(
                f"checksum ({checksum}) does not match expected value({decoded_bytes[19]})"
            )
        del cloned_bytes
        game_id = int("".join(reversed(decoded_secret[5:20])))
        decoded_array = bitarray(decoded_secret, endian=sys.byteorder)
        if decoded_secret[3:5] != "00":
            raise NotAGameCodeError("given secret is not a game code")
        is_hero_quest, target_game=(func(itm) for func, itm in zip((bool, int), decoded_array[20:22]))
        is_linked_game = bool(decoded_array[105])
        link_name_array=bytearray((
            Byte_From_Array(reverse_subarray(decoded_array, 22, 8)),
            Byte_From_Array(reverse_subarray(decoded_array, 38, 8)),
            Byte_From_Array(reverse_subarray(decoded_array, 60, 8)),
            Byte_From_Array(reverse_subarray(decoded_array, 77, 8)),
            Byte_From_Array(reverse_subarray(decoded_array, 89, 8))
        ))
        link_name = SecretEncoding.GetString(link_name_array)
        child_name_array=bytearray((
            Byte_From_Array(reverse_subarray(decoded_array, 30, 8)),
            Byte_From_Array(reverse_subarray(decoded_array, 46, 8)),
            Byte_From_Array(reverse_subarray(decoded_array, 68, 8)),
            Byte_From_Array(reverse_subarray(decoded_array, 97, 8)),
            Byte_From_Array(reverse_subarray(decoded_array, 106, 8)),
        ))