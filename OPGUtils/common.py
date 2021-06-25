# This file defines type and exceptions.
from enum import auto, Enum


class Priority(Enum):
    equal = auto()
    less = auto()
    more = auto()

    undefined = auto()


class NonOPGError(Exception):
    def __init__(self, message):
        super().__init__(message)


class OPGAmbiguousError(Exception):
    def __init__(self, message):
        super().__init__(message)
