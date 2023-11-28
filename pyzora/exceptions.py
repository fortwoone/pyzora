class SecretError(Exception):
    """Something is wrong with the secret."""
    pass


class ChecksumError(Exception):
    """Wrong secret checksum."""
    pass


class NotAGameCodeError(SecretError):
    """The given secret is not a game code."""


class NotARingCodeError(SecretError):
    """The given secret is not a ring password."""

class NotAMemoryCodeError(SecretError):
    """The given secret is not a memory password."""
