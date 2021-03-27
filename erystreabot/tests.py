import unittest
from typing import *
from parameterized import parameterized

from Author import Author
from Message import Message

from StringReplacer import StringReplacer
from MessageResponderRegex import MessageResponderRegex

import database.MockDbContext as mc 


class MockAuthor(Author):
    def __init__(self, id):
        self._id = id
    
    @property
    def id(self):
        return self._id
class MockMessage(Message):
    def __init__(self, content, author_id):
        self._content = content
        self._author = MockAuthor(author_id)

    @property
    def content(self):
        return self._content
    
    @property
    def author(self):
        return self._author

class StringReplacerTest(unittest.TestCase):
    @parameterized.expand([
        ["empty_dict_case_sensitive_1", {}, "abc def", False, "abc def"],
        ["empty_dict_case_sensitive_2", {}, "Lorem ipsum\n\n", False, "Lorem ipsum\n\n"],
        ["empty_dict_case_sensitive_3", {}, "Nothing Personal", False, "Nothing Personal"],
        ["empty_dict_case_insensitive_1", {}, "abc def", True, "abc def"],
        ["empty_dict_case_insensitive_2", {}, "Lorem ipsum\n\n", True, "Lorem ipsum\n\n"],
        ["empty_dict_case_insensitive_3", {}, "Nothing Personal", True, "Nothing Personal"],
        ["one_expression_dict_case_sensitive_same_case_1", {"abc": "def"}, "abc def", False, "def def"],
        ["one_expression_dict_case_sensitive_same_case_2", {"abc": "def"}, "Lorem ipsum\n\n", False, "Lorem ipsum\n\n"],
        ["one_expression_dict_case_sensitive_same_case_3", {"abc": "def"}, "Nothing Personal", False, "Nothing Personal"],
        ["one_expression_dict_case_insensitive_same_case_1", {"abc": "def"}, "abc def", True, "def def"],
        ["one_expression_dict_case_insensitive_same_case_2", {"abc": "def"}, "Lorem ipsum\n\n", True, "Lorem ipsum\n\n"],
        ["one_expression_dict_case_insensitive_same_case_3", {"abc": "def"}, "Nothing Personal", True, "Nothing Personal"],
        ["one_expression_dict_case_sensitive_different_case_1", {"AbC": "def"}, "abc def", False, "abc def"],
        ["one_expression_dict_case_sensitive_different_case_2", {"AbC": "def"}, "Lorem ipsum\n\n", False, "Lorem ipsum\n\n"],
        ["one_expression_dict_case_sensitive_different_case_3", {"AbC": "def"}, "Nothing Personal", False, "Nothing Personal"],
        ["one_expression_dict_case_insensitive_different_case_1", {"AbC": "def"}, "abc def", True, "def def"],
        ["one_expression_dict_case_insensitive_different_case_2", {"AbC": "def"}, "Lorem ipsum\n\n", True, "Lorem ipsum\n\n"],
        ["one_expression_dict_case_insensitive_different_case_3", {"AbC": "def"}, "Nothing PersonaBcl", True, "Nothing Persondefl"],
        ["two_expression_dict_case_sensitive_different_case_1", {"abc": "def", "ghi": "klm"}, "abcghi", False, "defklm"],
        ["two_expression_dict_case_sensitive_different_case_2", {"abc": "def", "ghi": "klm"}, "abcgHi", False, "defgHi"],
        ["two_expression_dict_case_insensitive_different_case_1", {"abc": "def", "ghi": "klm"}, "abcghi", True, "defklm"],
        ["two_expression_dict_case_insensitive_different_case_2", {"abc": "def", "ghi": "klm"}, "abcgHi", True, "defklm"]
    ])
    def test_is_replaced_text_correct(self, method_name: str, consts: Dict[str, str], string: str, ignore_case: bool, replaced: str):
        replacer = StringReplacer(consts, ignore_case)
        replaced_result = replacer.process(string)
        self.assertEqual(replaced_result, replaced)

class MessageResponderRegexTest(unittest.TestCase):
    def setUp(self):
        patterns_dict = {
            type('',(object,),{key: ".*\\bab\\b.*", response: "[user] wrote ab"})(),
            type('',(object,),{key: ".*\\bcD\\b.*", response: "[user] wrote cd"})(),
            type('',(object,),{key: ".*\\b(\d+)\\b.*", response: "[user] wrote [1]"})()
        }
        mockContext = mc.MockDbContext(patterns_dict)
        self.responder = MessageResponderRegex(mockContext)
        super().setUp()

    @parameterized.expand([
        ["nothing_to_change_1", "dcba dcba", 123, None],
        ["nothing_to_change_2", "Lorem ipsum", 456, None],
        ["first_pattern_match_1", "b ab a", 123, "<@123> wrote ab"],
        ["first_pattern_match_2", "B aB a", 456, "<@456> wrote ab"],
        ["second_pattern_match_1", "CD and CI", 123, "<@123> wrote cd"],
        ["second_pattern_match_2", "ci and cd", 456, "<@456> wrote cd"],
        ["both_pattern_match_1", "ab and cd", 123, "<@123> wrote ab"],
        ["both_pattern_match_2", "AB and CD", 456, "<@456> wrote ab"],
        ["group_pattern_match_1", "nm 789 mn", 123, "<@123> wrote 789"],
        ["group_pattern_match_2", "mn 987 mn", 456, "<@456> wrote 987"],
    ])
    def test_is_response_correct(self, method_name, message_content, author_id, expected_response):
        message = MockMessage(message_content, author_id)
        reponse = self.responder.prepare_response(message)
        self.assertEqual(reponse, expected_response)

if __name__ == '__main__':
    unittest.main()
