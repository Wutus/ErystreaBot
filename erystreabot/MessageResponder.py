from typing import *
from abc import abstractmethod
import discord
from Message import Message

class MessageResponder(Protocol):
    @abstractmethod
    def prepare_response(self, message: Message) -> str:
        raise NotImplementedError()