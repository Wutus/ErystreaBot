import discord
import json
import logging
from typing import *
from MessageResponder import MessageResponder

class ErystreaBot(discord.Client):

    def __init__(self, config: Dict[str, str], responder: MessageResponder, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = config
        self.responder = responder

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        match_response = self.responder.prepare_response(message)
        if match_response is not None:
            await message.reply(match_response)

    def launch_bot(self):
        self.run(self.config["token"])
