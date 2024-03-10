from pathlib import Path
import os
# Creating a table of the books of the Bible in the KJV version along with their verse counts.
# The table will include all books from both the Old and New Testaments.
LOCAL_BIBLE_DIR = Path.home() / 'grepbible_data/kj' 

_books_and_verse_counts = [
    ("Genesis", 1533),
    ("Exodus", 1213),
    ("Leviticus", 859),
    ("Numbers", 1288),
    ("Deuteronomy", 959),
    ("Joshua", 658),
    ("Judges", 618),
    ("Ruth", 85),
    ("1 Samuel", 810),
    ("2 Samuel", 695),
    ("1 Kings", 816),
    ("2 Kings", 719),
    ("1 Chronicles", 942),
    ("2 Chronicles", 822),
    ("Ezra", 280),
    ("Nehemiah", 406),
    ("Esther", 167),
    ("Job", 1070),
    ("Psalms", 2461),
    ("Proverbs", 915),
    ("Ecclesiastes", 222),
    ("Song of Solomon", 117),
    ("Isaiah", 1292),
    ("Jeremiah", 1364),
    ("Lamentations", 154),
    ("Ezekiel", 1273),
    ("Daniel", 357),
    ("Hosea", 197),
    ("Joel", 73),
    ("Amos", 146),
    ("Obadiah", 21),
    ("Jonah", 48),
    ("Micah", 105),
    ("Nahum", 47),
    ("Habakkuk", 56),
    ("Zephaniah", 53),
    ("Haggai", 38),
    ("Zechariah", 211),
    ("Malachi", 55),
    ("Matthew", 1071),
    ("Mark", 678),
    ("Luke", 1151),
    ("John", 879),
    ("Acts", 1007),
    ("Romans", 433),
    ("1 Corinthians", 437),
    ("2 Corinthians", 257),
    ("Galatians", 149),
    ("Ephesians", 155),
    ("Philippians", 104),
    ("Colossians", 95),
    ("1 Thessalonians", 89),
    ("2 Thessalonians", 47),
    ("1 Timothy", 113),
    ("2 Timothy", 83),
    ("Titus", 46),
    ("Philemon", 25),
    ("Hebrews", 303),
    ("James", 108),
    ("1 Peter", 105),
    ("2 Peter", 61),
    ("1 John", 105),
    ("2 John", 13),
    ("3 John", 14),
    ("Jude", 25),
    ("Revelation", 404)
]


# books_and_verse_counts as dictionary
books_and_verse_counts = dict(_books_and_verse_counts)

lines_per_book = {}

for book in os.listdir(LOCAL_BIBLE_DIR):
    book_path = os.path.join(LOCAL_BIBLE_DIR, book)
    if not os.path.isdir(book_path):
        continue
    
    lines_count = 0
    for chapter_file in os.listdir(book_path):
        chapter_path = os.path.join(book_path, chapter_file)
        if os.path.isfile(chapter_path):
            with open(chapter_path, 'r') as file:
                lines_count += len(file.readlines())
    
    lines_per_book[book] = lines_count

discrepancies = {}

for book, target_count in books_and_verse_counts.items():
    real_count = lines_per_book.get(book, 0)  # Default to 0 if book not found in real counts
    if real_count != target_count:
        discrepancies[book] = {"observed": real_count, "expected": target_count}

if len(discrepancies) == 0:
    print("All books have the expected verse counts.")
else:
    for key in discrepancies:
        print(key + ": ", discrepancies[key])
