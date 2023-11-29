from pyzora.secret import *
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
        "region",
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

    def __set_hero_quest(self, value: bool):
        self.__is_hero_quest = value

    is_hero_quest = property(lambda self: self.__is_hero_quest, __set_hero_quest,
                             doc="""A Hero's Secret allows the player to start
                             the game anew and get a special ring.""")

    def __set_linked_game(self, value: bool):
        self.__is_linked_game = value

    is_linked_game = property(lambda self: self.__is_linked_game, __set_linked_game,
                              doc="""If a game is linked, some additional events will happen in the 
                              target game.""")

    def __set_link_name(self, value: str):
        if len(value.strip()) > 5:
            raise ValueError(f"incorrect name for Link : {value}")
        self.__link_name = value.strip().ljust(5, "\0")

    link_name = property(lambda self: self.__link_name.replace("\0", " "), __set_link_name,
                         doc="""Link's name. Takes at most 5 characters to fit in the secret.""")

    def __set_child_name(self, value: str):
        self.__child_name = value.strip().ljust(5, "\0")

    child_name = property(lambda self: self.__child_name.replace("\0", " "), __set_child_name,
                          doc="""Game secrets also store Bipin and Blossom's child's
                          name.""")

    def __set_animal(self, value: ObtainedCompanion | int):
        self.__animal = ObtainedCompanion(value)

    animal = property(lambda self: self.__animal, __set_animal,
                      doc="""The companion Link has obtained.
                      During linked games, this should be set.
                      In linked games, the companion stored in the secret will
                      recognise Link and give him his flute again.""")

    def __get_behaviour(self):
        return ChildBehaviour(self.__behaviour[0])

    def __set_behaviour(self, value):
        self.__behaviour = bytearray((int(value),))

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
    def load(cls, secret: bytes | bytearray | str, region: GameRegion) -> "GameSecret":
        """Load a game secret from bytes or a string."""
        if isinstance(secret, str):
            # Secret string. Parse it before doing anything else.
            # Allows the user to give the region only once
            return cls.load(parse_secret(secret, region), region)
        if len(secret) != 20:
            raise SecretError("secret must contain exactly 20 bytes")
        decoded_bytes = cls.decode_bytes(secret, region)
        decoded_secret = byte_array_to_string(decoded_bytes)
        cloned_bytes = decoded_bytes.copy()
        cloned_bytes[19] = 0
        checksum = calculate_checksum(cloned_bytes)
        if decoded_bytes[19] & 0xF != checksum & 0xF:
            raise ChecksumError(
                f"checksum ({checksum}) does not match expected value({decoded_bytes[19]})"
            )
        del cloned_bytes
        game_id = int("".join(reversed(decoded_secret[5:20])), 2)
        if decoded_secret[3:5] != "00":
            raise NotAGameCodeError("given secret is not a game code")
        is_hero_quest, target_game = (func(itm) for func, itm in zip(("1".__eq__, int), decoded_secret[20:22]))
        is_linked_game = bool(int(decoded_secret[105]))
        link_name_array = bytearray((
            Byte(reverse_substring(decoded_secret, 22, 8)),
            Byte(reverse_substring(decoded_secret, 38, 8)),
            Byte(reverse_substring(decoded_secret, 60, 8)),
            Byte(reverse_substring(decoded_secret, 77, 8)),
            Byte(reverse_substring(decoded_secret, 89, 8))
        ))
        link_name = link_name_array.decode("utf-8")
        child_name_array = bytearray((
            Byte(reverse_substring(decoded_secret, 30, 8)),
            Byte(reverse_substring(decoded_secret, 46, 8)),
            Byte(reverse_substring(decoded_secret, 68, 8)),
            Byte(reverse_substring(decoded_secret, 97, 8)),
            Byte(reverse_substring(decoded_secret, 106, 8)),
        ))
        child_name = child_name_array.decode("utf-8")
        animal = ObtainedCompanion(Byte(reverse_substring(decoded_secret, 85, 4)))
        behaviour = Byte(reverse_substring(decoded_secret, 54, 6))
        was_given_free_ring = bool(int(decoded_secret[76]))
        return GameSecret(game_id=game_id, region=region,
                          link_name=link_name, target_game=target_game,
                          child_name=child_name, animal=animal,
                          was_given_free_ring=was_given_free_ring,
                          is_linked_game=is_linked_game,
                          is_hero_quest=is_hero_quest,
                          behaviour=behaviour)

    def __bytes__(self):
        link_byte_array = bytearray(self.link_name, "utf-8")
        child_byte_array = bytearray(self.child_name, "utf-8")
        cipher_key = (((self.game_id >> 8) + (self.game_id & 255)) & 7) * 2
        unencoded_secret = "".join(
            (
                reverse_string(integer_string(cipher_key).rjust(3, "0")),
                "00",  # This is to tell the game that we're writing a linking secret.
                reverse_string(integer_string(self.game_id).rjust(15, "0")),
                str(int(self.is_hero_quest)), str(int(self.target_game)),
                reverse_string(integer_string(link_byte_array[0]).rjust(8, "0")),
                reverse_string(integer_string(child_byte_array[0]).rjust(8, "0")),
                reverse_string(integer_string(link_byte_array[1]).rjust(8, "0")),
                reverse_string(integer_string(child_byte_array[1]).rjust(8, "0")),
                reverse_string(integer_string(self.behaviour).rjust(6, "0")),
                reverse_string(integer_string(link_byte_array[2]).rjust(8, "0")),
                reverse_string(integer_string(child_byte_array[2]).rjust(8, "0")),
                str(int(self.was_given_free_ring)),
                reverse_string(integer_string(link_byte_array[3]).rjust(8, "0")),
                reverse_string(integer_string(self.animal).rjust(4, "0")),
                reverse_string(integer_string(link_byte_array[4]).rjust(8, "0")),
                reverse_string(integer_string(child_byte_array[3]).rjust(8, "0")),
                str(int(self.is_linked_game)),
                reverse_string(integer_string(child_byte_array[4]).rjust(8, "0"))
            )
        )
        unencoded_bytes = string_to_byte_array(unencoded_secret)
        unencoded_bytes[19] = calculate_checksum(unencoded_bytes)
        secret = self._encode_bytes(unencoded_bytes, self.region)
        return bytes(secret)

    def __hash__(self):
        return hash(
            (
                self.game_id,
                self.__region,
                self.animal,
                self.behaviour,
                self.child_name,
                self.link_name,
                self.is_hero_quest,
                self.is_linked_game,
                self.target_game,
            )
        )
