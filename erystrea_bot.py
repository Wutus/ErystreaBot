import discord
import re
import json
from StringReplacer import StringReplacer


class ErystreaBot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configuration_path = "configure.json"
        self.patterns_path = "patterns.json"
        with open(self.configuration_path, 'r', encoding="utf-8") as f:
            self.config = json.load(f)
        with open(self.patterns_path, 'r', encoding="utf-8") as f:
            self.pattern_dict = self.prepare_pattern_dict(json.load(f))

    def prepare_pattern_dict(self, str_dict):
        return {
            re.compile(k, re.IGNORECASE): v for k, v in str_dict.items()
        }

    def constant_replace(self, s, d):
        replacer = StringReplacer(d, ignore_case=True)
        replaced = replacer.process(s)
        return replaced

    def match_pattern(self, message):
        meta_dict = {
            "user": f"<@{message.author.id}>"
        }
        for pattern, response in self.pattern_dict.items():
            if m := pattern.match(message.content):
                meta_dict["0"] = m.group()
                for i, g in enumerate(m.groups()):
                    meta_dict[f"{i+1}"] = g
                print(f"Matched to pattern {pattern}")
                replace_dict = {f"[{k}]": v for k, v in meta_dict.items()}
                replaced_response = self.constant_replace(
                    response, replace_dict)
                return replaced_response
        return None

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        print(f"MESSAGE:\n{message.content}")

        match_response = self.match_pattern(message)
        if match_response != None:
            await message.reply(match_response)

    def launch_bot(self):
        self.run(self.config["TOKEN"])
