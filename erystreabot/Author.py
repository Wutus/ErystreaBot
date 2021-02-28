from typing import *
from abc import abstractmethod
import discord

class Author(Protocol):
    @property
    @abstractmethod
    def id(self) -> int:
        raise NotImplementedError()