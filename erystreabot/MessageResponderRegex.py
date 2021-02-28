from StringReplacer import StringReplacer
import re
import discord
import logging
from Message import Message
from MessageResponder import MessageResponder

class MessageResponderRegex(MessageResponder):

    def __init__(self, patterns_str: Dict[str, str]):
        self.patterns_str = patterns_str
        self.patterns = self._prepare_pattern_dict(patterns_str)

    def _prepare_pattern_dict(self, str_dict: Dict[str, str]):
        return {
            re.compile(k, re.IGNORECASE): v for k, v in str_dict.items()
        }

    def _constant_replace(self, s: str, d: Dict[str, str]):
        replacer = StringReplacer(d, ignore_case=True)
        replaced = replacer.process(s)
        return replaced
    
    def _get_basic_meta_dict(self, message: discord.Message) -> Dict[re.Pattern[str], str]:
        return {
            "user": f"<@{message.author.id}>"
        }

    def _get_replace_dict(self, meta_dict: Dict[str, str], match_dict: Dict[str, str]) -> Dict[str, str]:
        merged_dict = {**meta_dict, **match_dict}
        return {f"[{k}]": v for k, v in merged_dict.items()}

    def _process_match(self, meta_dict: Dict[str, str], m: re.Match[str], content: str) -> str:
        match_dict = {
            "0": m.group()
        }
        for i, g in enumerate(m.groups()):
            match_dict[f"{i+1}"] = g
        replace_dict = self._get_replace_dict(meta_dict, match_dict)
        replaced_response = self._constant_replace(content, replace_dict)
        return replaced_response

    def prepare_response(self, message: Message) -> Optional[str]:
        meta_dict = self.get_basic_meta_dict(message)
        for pattern, response in self.pattern_dict.items():
            if m := pattern.match(message.content):
                logging.info(f"Matched message: {message.content}\n  from {message.author}\n to pattern {pattern}")
                response = self._process_match(meta_dict, m, message.content)
                return response
        logging.info(f"No match for message {message.content} from {message.author}")
        return None