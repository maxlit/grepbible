from pathlib import Path
import os, re
import requests
from zipfile import ZipFile
from pathlib import Path
from urllib.parse import urljoin
import importlib.resources as pkg_resources
from . import static  # Relative import of the static package

DOWNLOAD_ENDPOINT = "https://powerdb.s3.us-west-2.amazonaws.com/download_endpoint/"
LOCAL_BIBLE_DIR = Path.home() / 'grepbible_data'

BOOK_ABBREVIATIONS = {
    'Gen': 'Genesis',
    'Ex': 'Exodus',
    'Lev': 'Leviticus',
    'Num': 'Numbers',
    'Deut': 'Deuteronomy',
    'Josh': 'Joshua',
    'Judg': 'Judges',
    'Ruth': 'Ruth',
    '1Sam': '1 Samuel',
    '2Sam': '2 Samuel',
    '1Kgs': '1 Kings',
    '2Kgs': '2 Kings',
    '1Chr': '1 Chronicles',
    '2Chr': '2 Chronicles',
    'Ezra': 'Ezra',
    'Neh': 'Nehemiah',
    'Est': 'Esther',
    'Job': 'Job',
    'Ps': 'Psalms',
    'Prov': 'Proverbs',
    'Eccles': 'Ecclesiastes',
    'Song': 'Song of Solomon',
    'Isa': 'Isaiah',
    'Jer': 'Jeremiah',
    'Lam': 'Lamentations',
    'Ezek': 'Ezekiel',
    'Dan': 'Daniel',
    'Hos': 'Hosea',
    'Joel': 'Joel',
    'Amos': 'Amos',
    'Obad': 'Obadiah',
    'Jonah': 'Jonah',
    'Mic': 'Micah',
    'Nah': 'Nahum',
    'Hab': 'Habakkuk',
    'Zeph': 'Zephaniah',
    'Hag': 'Haggai',
    'Zech': 'Zechariah',
    'Mal': 'Malachi',
    'Matt': 'Matthew',
    'Mark': 'Mark',
    'Luke': 'Luke',
    'John': 'John',
    'Acts': 'Acts',
    'Rom': 'Romans',
    '1Cor': '1 Corinthians',
    '2Cor': '2 Corinthians',
    'Gal': 'Galatians',
    'Eph': 'Ephesians',
    'Phil': 'Philippians',
    'Col': 'Colossians',
    '1Thess': '1 Thessalonians',
    '2Thess': '2 Thessalonians',
    '1Tim': '1 Timothy',
    '2Tim': '2 Timothy',
    'Titus': 'Titus',
    'Philem': 'Philemon',
    'Heb': 'Hebrews',
    'James': 'James',
    '1Pet': '1 Peter',
    '2Pet': '2 Peter',
    '1John': '1 John',
    '2John': '2 John',
    '3John': '3 John',
    'Jude': 'Jude',
    'Rev': 'Revelation',
}

def ensure_data_dir_exists():
    try:
        LOCAL_BIBLE_DIR.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Permission denied: Unable to create directory at {LOCAL_BIBLE_DIR}. Please check your permissions.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while creating the directory at {LOCAL_BIBLE_DIR}: {e}")
        exit(1)

def ensure_bible_version_exists(version):
    ensure_data_dir_exists()
    bible_version_path = LOCAL_BIBLE_DIR / version
    if not bible_version_path.exists():
        print(f"Downloading {version}...")
        download_and_extract_bible(version)
    else:
        pass
        #print(f"{version} already exists locally.")
    
def list_bibles():
    with pkg_resources.path(static, 'acronyms.txt') as acronym_path, \
         pkg_resources.path(static, 'full_names.txt') as full_name_path:
        
        # Read acronyms and full names into lists
        with open(acronym_path, 'r') as af:
            acronyms = af.read().splitlines()
        with open(full_name_path, 'r') as fnf:
            full_names = fnf.read().splitlines()
    
    # Create a mapping of acronyms to full names
    bible_versions = dict(zip(acronyms, full_names))
    
    # Check which Bibles are available locally
    local_bibles = [b.name for b in LOCAL_BIBLE_DIR.iterdir() if b.is_dir()]
    
    for acronym, full_name in bible_versions.items():
        local_indicator = "[local]" if acronym in local_bibles else ""
        print(f"{acronym} - {full_name} {local_indicator}")

def download_and_extract_bible(version):
    os.makedirs(LOCAL_BIBLE_DIR, exist_ok=True)
    zip_url = urljoin(DOWNLOAD_ENDPOINT, f"{version}.zip")
    zip_path = LOCAL_BIBLE_DIR / f"{version}.zip"
    
    # Download zip file
    response = requests.get(zip_url)
    with open(zip_path, 'wb') as zip_file:
        zip_file.write(response.content)
    
    # Extract zip file
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(LOCAL_BIBLE_DIR)
    os.remove(zip_path)  # Clean up zip file

def parse_citation(citation):
    # This is a simplified pattern and might need adjustments
    pattern = r'(\d?\s?[a-zA-Z]+\.?)\s+(\d+)(?:[:–](\d+))?[:](\d+)(?:–(\d+))?(?:,(\d+))?'
    match = re.match(pattern, citation.replace(" ", ""))
    if not match:
        print(f"Could not parse the citation: {citation}")
        return None
    
    book, start_chapter, end_chapter, start_verse, end_verse, extra_verse = match.groups()
    # Normalize book name
    book = book.replace('.', '')  # Remove period from abbreviations if present
    book = BOOK_ABBREVIATIONS.get(book, book)  # Translate abbreviation to full name if possible
    return book, start_chapter, end_chapter, start_verse, end_verse, extra_verse

def get_verse(version, citation):
    ensure_bible_version_exists(version)
    parsed = parse_citation(citation)
    if not parsed:
        return
    
    book, start_chapter, end_chapter, start_verse, end_verse, extra_verse = parsed
    chapters = range(int(start_chapter), int(end_chapter) + 1) if end_chapter else [int(start_chapter)]
    verses_to_fetch = [int(start_verse)]
    if end_verse:
        verses_to_fetch.extend(range(int(start_verse) + 1, int(end_verse) + 1))
    if extra_verse:
        verses_to_fetch.append(int(extra_verse))
    
    for chapter in chapters:
        chapter_file = LOCAL_BIBLE_DIR / version / f"{book}_{chapter}.txt"
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                chapter_verses = f.readlines()
                for verse_num in verses_to_fetch:
                    # Adjust for zero-based indexing
                    print(chapter_verses[verse_num - 1].strip())
        except FileNotFoundError:
            print(f"File not found: {chapter_file}")
        except IndexError:
            print(f"Verse number out of range in {book} chapter {chapter}")
