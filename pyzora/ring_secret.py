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

    def __set_rings(self, value:int):
        if value > int(AllRings):
            raise ValueError("cannot set a value higher than AllRings")
        if value < 0:
            raise ValueError("value must be an unsigned integer")
        # Converting the parameter into an integer in case we've been given a RingType instance
        self.__rings = int(value)

    rings = property(lambda self: self.__rings, __set_rings,
                     doc="""Get the rings stored in the secret as an integer.""")

    @property
    def ring_count(self):
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


