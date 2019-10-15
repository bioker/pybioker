from unittest import TestCase

from bioker.util.string import StringsMatchBuilder


class TestStringsMatchBuilder(TestCase):

    def test_include(self):
        strings = ['abc', 'def']
        smb = StringsMatchBuilder(strings)
        matched_strings = smb.include('a').get_strings()
        self.assertEqual(1, len(matched_strings))
        self.assertIn('abc', matched_strings)

    def test_exclude(self):
        strings = ['abc', 'def']
        smb = StringsMatchBuilder(strings)
        matched_strings = smb.exclude('a').get_strings()
        self.assertEqual(1, len(matched_strings))
        self.assertIn('def', matched_strings)
