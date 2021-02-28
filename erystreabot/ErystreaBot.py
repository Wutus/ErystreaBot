import discord
import json
import logging
from typing import *
from MessageResponder import MessageResponder

class ErystreaBot(discord.Client):

    def __init__(self, configuration_path: str, responder: MessageResponder, patterns_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configuration_path = configuration_path
        self.patterns_path = patterns_path
        with open(self.configuration_path, 'r', encoding="utf-8") as f:
            self.config = json.load(f)
        with open(self.patterns_path, 'r', encoding="utf-8") as f:
            self.pattern_dict = self.prepare_pattern_dict(json.load(f))
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
