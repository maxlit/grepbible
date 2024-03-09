import unittest
import sys
from pathlib import Path

# Add the root directory to PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))
#import grepbible as gb
from grepbible.bible_manager import *

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

def main():
    unittest.main()

if __name__=='__main__':
    main()
