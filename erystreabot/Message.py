from typing import *
from abc import abstractmethod
import discord
from Author import Author
class Message(Protocol):
    @property
    @abstractmethod
    def author(self) -> Author:
        raise NotImplementedError()

    @property
    @abstractmethod
    def content(self) -> str:
        raise NotImplementedError()