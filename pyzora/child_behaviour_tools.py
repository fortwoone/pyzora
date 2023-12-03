"""pyzora - Python library to help parsing secrets from Zelda OoS/OoA

Child behaviour helpers.

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
from pyzora.enums import *
from typing import Literal
from itertools import starmap


_NORM_METHODS = (str.upper, lambda x: x)


def _normalise_name(region: GameRegion, name: str) -> str:
    """Return a normalised version of the child's name.
    If the region is not JP, then this returns the unchanged string.

    :param region: The region to use for this operation.
    :type region: GameRegion
    :param name: The child's name.
    :type name: str
    :return: The normalised name.
    :rtype: str
    :meta private:"""
    return _NORM_METHODS[region](name)


def _get_value_for_child_name(region: GameRegion, name: str):
    if len(name) > 5:
        raise ValueError(f"invalid child name : must be at most 5 characters long (got a {len(name)}-character string instead)")
    b_name = bytes(_normalise_name(region, name), "utf-8")
    value = sum(map((0xF).__and__, b_name)) - 3
    while value > 255:
        value -= 3
    return value + 4


_ChildBehaviourArgs = tuple[RupeesGiven, SleepMethod, ChildQuestion, ChildKind] | tuple[RupeesGiven, SleepMethod]
_CHILDBEVHAVIOURTYPES=(RupeesGiven, SleepMethod, ChildQuestion, ChildKind)


def get_child_behaviour_value(
        region: GameRegion,
        name: str,
        *args: _ChildBehaviourArgs
) -> int:
    """Get the raw integer value for the child's behaviour based on the answer to the questions.

    :param region: The region to use for this (puts the name to uppercase if the region is Japan).
    :type region: GameRegion
    :param name: The child's name.
    :type name: str
    :param args: Contains in this order, how many rupees you gave to Blossom, the sleep method you suggested her to use, the answer you gave to the kid's question and what kind of child you were.
    :type args: RupeesGiven, SleepMethod, ChildQuestion, ChildKind
    :return: The raw behaviour value (does not go above 255).
    :rtype: int"""
    if not len(args):
        return _get_value_for_child_name(region, name)
    if len(args) not in {2, 4}:
        raise TypeError(f"unexpected arguments (starting at the {('third', 'fifth')[len(args) > 4]} value) : {args}")
    if not all(starmap(isinstance, zip(args, _CHILDBEVHAVIOURTYPES))):
        raise TypeError(f"wrong argument order or unexpected arguments : {tuple(map(lambda obj: type(obj).__qualname__, args))}")
    return _get_value_for_child_name(region, name) + sum(args)


_Byte = Literal[*range(256)]  # writing all values from 0 to 256 would be slow and ugly


def get_behaviour(value: _Byte) -> ChildBehaviour:
    if value == 0:
        return ChildBehaviour.NONE
    if value < 6:
        return ChildBehaviour.CURIOUS
    if value < 11:
        return ChildBehaviour.SHY
    return ChildBehaviour.BOUNCY
