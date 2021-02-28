#Downloaded from https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
import re
from typing import *

def identity(s):
    return s

def lowercase(s):
    return s.lower()

class StringReplacer(object):

    def process(self, string: str):
        """
        Process the given string by replacing values as configured
        :param str string: string to perform replacements on
        :rtype: str
        """
        replacements = self.replacements
        if(len(replacements) == 0):
            #Nothing to replace - return original
            return string
        normalize = self.normalize
        # For each match, look up the new string in the replacements via the normalized old string
        return self.pattern.sub(lambda match: replacements[normalize(match.group(0))], string)

    def __init__(self, replacements: Dict[str, str], ignore_case: bool=False):
        """
        Given a replacement map, instantiate a StringReplacer.
        :param dict replacements: replacement dictionary {value to find: value to replace}
        :param bool ignore_case: whether the match should be case insensitive
        :rtype: None
        """
        self.normalize = self._configure_normalize(ignore_case)
        self.replacements = self._configure_replacements(replacements, self.normalize)
        self.pattern = self._configure_pattern(self.replacements, ignore_case)

    def _configure_normalize(self, ignore_case: bool):
        # If case insensitive, we need to normalize the old string so that later a replacement
        # can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
        # "HEY", "hEy", etc.
        return lowercase if ignore_case else identity

    def _configure_replacements(self, replacements: Dict[str, str], normalize: Callable[[str], str]):
        return {normalize(key): value for key, value in replacements.items()}

    def _configure_pattern(self, replacements: Dict[str, str], ignore_case: bool):
        # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
        # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
        # 'hey ABC' and not 'hey ABc'
        sorted_replacement_keys = sorted(replacements, key=len, reverse=True)
        escaped_replacement_keys = [re.escape(key) for key in sorted_replacement_keys]

        re_mode = re.IGNORECASE if ignore_case else 0

        # Create a big OR regex that matches any of the substrings to replace
        return re.compile('|'.join(escaped_replacement_keys), re_mode)