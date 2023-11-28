from pyzora.secret import *


class MemorySecret(BaseSecret):
    """A memory secret to transfer between two NPCS in Holodrum and Labrynna."""

    __args = ("game_id", "game_region", "target_game", "memory", "is_return_secret")

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
    def load(cls, secret: bytearray | bytes, region: GameRegion):
        if len(secret) != 5:
            raise SecretError("secret must contain exactly 5 bytes")
        decoded_bytes = cls.decode_bytes(secret, region)
        decoded_secret = byte_array_to_string(decoded_bytes)
