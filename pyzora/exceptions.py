"""pyzora - Python library to help parsing secrets from Zelda OoS/OoA

Exceptions raised by library functions.

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


class SecretError(Exception):
    """Something is wrong with the secret."""


class ChecksumError(SecretError):
    """Wrong secret checksum."""


class NotAGameCodeError(SecretError):
    """The given secret is not a game code."""


class NotARingCodeError(SecretError):
    """The given secret is not a ring password."""


class NotAMemoryCodeError(SecretError):
    """The given secret is not a memory password."""
