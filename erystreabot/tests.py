import unittest
from typing import *
from StringReplacer import StringReplacer
from parameterized import parameterized

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

if __name__ == '__main__':
    unittest.main()
