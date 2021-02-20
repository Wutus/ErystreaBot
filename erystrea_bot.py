import discord
import re
import json
from StringReplacer import StringReplacer

client = discord.Client()

configuration_path = "configure.json"
patterns_path = "patterns.json"

with open(configuration_path, 'r', encoding="utf-8") as f:
    config = json.load(f)

def prepare_pattern_dict(str_dict):
    return {
        re.compile(k, re.IGNORECASE):v for k,v in str_dict.items()
    }

with open(patterns_path, 'r', encoding="utf-8") as f:
    pattern_dict = prepare_pattern_dict(json.load(f))

def constant_replace(s, d):
    replacer = StringReplacer(d, ignore_case=True)
    replaced = replacer.process(s)
    return replaced

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot:
        return
    meta_dict = {
        "user": f"<@{message.author.id}>"
    }
    print(f"MESSAGE:\n{message.content}")
    for pattern, response in pattern_dict.items():
        if m := pattern.match(message.content):
            meta_dict["0"] = m.group()
            for i, g in enumerate(m.groups()):
                meta_dict[f"{i+1}"] = g 
            print(f"Matched to pattern {pattern}")
            replace_dict = {f"[{k}]":v for k,v in meta_dict.items()}
            replaced_response = constant_replace(response, replace_dict)
            reply_status = await message.reply(replaced_response)
            break

client.run(config["TOKEN"])