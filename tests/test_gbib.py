import unittest
import sys
from pathlib import Path
import os

# Add the root directory to PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))
#import grepbible as gb
from grepbible.bible_manager import *
from grepbible.utils import grep_to_citation

# Add this at the top level
def skip_in_ci():
    """Skip test if running in CI environment"""
    return unittest.skipIf(
        os.getenv('CI') == 'true',
        'Test skipped in CI environment'
    )

class TestGB(unittest.TestCase):
    def test_parse_citation(self):
        quotes = ['Genesis 1:1', 'Gen 1:1', 'Gen. 1:1']
        for quote in quotes:
            book, chapter, verse_parts = parse_citation(quote)
            self.assertEqual(book, 'Genesis')
            self.assertEqual(chapter, '1')
            self.assertEqual(verse_parts[0], '1')

    def test_parse_citation_range(self):  
        book, chapter, verse_parts = parse_citation("Genesis 1:1-10")
        self.assertEqual(book, 'Genesis')
        self.assertEqual(chapter, '1')
        self.assertEqual(verse_parts[0], '1-10')

    def test_parse_citation_disjoint(self):  
        book, chapter, verse_parts = parse_citation("Genesis 1:1,10")
        self.assertEqual(book, 'Genesis')
        self.assertEqual(chapter, '1')
        self.assertEqual(verse_parts[1], '10')

    def test_parse_chapter(self):
        book, chapter, verse_parts = parse_citation("Psalms 23")
        self.assertEqual(book, 'Psalms')
        self.assertEqual(chapter, '23')
        self.assertEqual(verse_parts, None)

    def test_get_available_versions(self):
        accros = get_available_versions()
        self.assertTrue('kj' in accros)
        self.assertFalse('xyz' in accros)

    def test_is_valid_version(self):
        self.assertTrue(is_valid_version('bg'))
        self.assertFalse(is_valid_version('xyz'))

    def test_random_quote(self):
        quote = get_random_quote('kj')
        self.assertTrue(True) # the check is that it runs through, the quote itself goes to stdout

    def test_grep_to_citation(self):
        grep_line = "~/grepbible_data/kj/Daniel/10.txt:3:I ate no pleasant bread, neither came flesh nor wine in my mouth, neither did I anoint myself at all, till three whole weeks were fulfilled."
        expected = "(Daniel 10:3) I ate no pleasant bread, neither came flesh nor wine in my mouth, neither did I anoint myself at all, till three whole weeks were fulfilled."
        self.assertEqual(grep_to_citation(grep_line), expected)
        
        # Test with different path formats
        grep_line2 = "data/bible/Genesis/1.txt:1:In the beginning"
        expected2 = "(Genesis 1:1) In the beginning"
        self.assertEqual(grep_to_citation(grep_line2), expected2)

        # Test with different path formats
        grep_line3 = "~/grepbible_data/kj/kj/Amos/6.txt:12:Shall horses run upon the rock? will one plow there with oxen? for ye have turned judgment into gall, and the fruit of righteousness into hemlock:"
        expected3 = "(Amos 6:12) Shall horses run upon the rock? will one plow there with oxen? for ye have turned judgment into gall, and the fruit of righteousness into hemlock:"
        self.assertEqual(grep_to_citation(grep_line3), expected3)
        
        # Test error handling
        with self.assertRaises(ValueError):
            grep_to_citation("invalid:format")

def main():
    unittest.main()

if __name__=='__main__':
    main()
