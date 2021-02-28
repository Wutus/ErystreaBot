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

        response = self.responder.prepare_response(message)
        if response is not None:
            await message.reply(response)

    def launch_bot(self):
        self.run(self.config["token"])
