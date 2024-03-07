from pathlib import Path
import os, re
import requests
from zipfile import ZipFile, BadZipFile
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
        download_and_extract_bible(version)
    else:
        pass
        #print(f"{version} already exists locally.")

def get_available_versions():
    # Use the 'files' function to get a path-like object for 'acronyms.txt'
    resource_path = pkg_resources.files('grepbible.static').joinpath('acronyms.txt')
    with resource_path.open('r') as af:
        acronyms = af.read().splitlines()
    return acronyms

def is_valid_version(supplied_version):
    available_versions = get_available_versions()
    return supplied_version in available_versions


def list_bibles():
    ensure_data_dir_exists()
    # Adjust to use 'files()' for accessing resource files
    acronyms_path = pkg_resources.files('grepbible.static').joinpath('acronyms.txt')
    full_names_path = pkg_resources.files('grepbible.static').joinpath('full_names.txt')
    
    # Read acronyms and full names into lists
    with acronyms_path.open('r') as af:
        acronyms = af.read().splitlines()
    with full_names_path.open('r') as fnf:
        full_names = fnf.read().splitlines()
    
    # Create a mapping of acronyms to full names
    bible_versions = dict(zip(acronyms, full_names))
    
    # Check which Bibles are available locally
    local_bibles = [b.name for b in LOCAL_BIBLE_DIR.iterdir() if b.is_dir()]
    
    for acronym, full_name in bible_versions.items():
        local_indicator = "[local]" if acronym in local_bibles else ""
        print(f"{acronym} - {full_name} {local_indicator}")


def download_and_extract_bible(version):
    if not is_valid_version(version):
        print(f"Invalid version: {version}")
        print("Use the -l flag to list available versions.")
        return
    zip_url = urljoin(DOWNLOAD_ENDPOINT, f"{version}.zip")
    print(f"Downloading {version} from {zip_url}...")
    zip_path = LOCAL_BIBLE_DIR / f"{version}.zip"
    
    # Download zip file
    try:
        response = requests.get(zip_url, stream=True)
        if response.status_code == 200:
            with open(zip_path, 'wb') as zip_file:
                for chunk in response.iter_content(chunk_size=8192): 
                    zip_file.write(chunk)
            # Extract zip file
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(LOCAL_BIBLE_DIR)
            os.remove(zip_path)  # Clean up zip file
        else:
            print(f"Error downloading file: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except BadZipFile as e:
        print(f"Zip file error: {e}")
        os.remove(zip_path)  # Attempt to clean up corrupt zip file

def parse_citation(citation):
    # Pattern to match "BookName Chapter:Verse", "BookName Chapter:Verse-Verse", and "BookName Chapter:Verse,Verse"
    # Accepts a colon as the separator between the chapter and verses, and commas for multiple verses
    pattern = r'([1-3]?\s?[a-zA-Z]+\.?)\s+(\d+):\s*((?:\d+(?:-\d+)?\s*,?\s*)+)'
    match = re.match(pattern, citation)
    if not match:
        print(f"Could not parse the citation: {citation}")
        return None

    book_abbr, chapter, verses = match.groups()
    
    # Normalize the book abbreviation by removing any trailing dot and mapping to full name
    book_abbr_normalized = book_abbr.rstrip('.')
    book = BOOK_ABBREVIATIONS.get(book_abbr_normalized, book_abbr_normalized)
    
    # Split the verses part into individual verses or verse ranges
    verse_parts = [v.strip() for v in verses.split(',') if v]

    return book, chapter, verse_parts

def get_verse(version, citation):
    ensure_bible_version_exists(version)
    parsed = parse_citation(citation)
    if not parsed:
        return
    
    book, chapter, verse_parts = parsed  # Adjusted to match new parse_citation output
    
    for part in verse_parts:
        if '-' in part:  # If the part is a verse range
            start_verse, end_verse = map(int, part.split('-'))
            verses_to_fetch = range(start_verse, end_verse + 1)
        else:  # If the part is an individual verse
            verses_to_fetch = [int(part)]
        
        chapter_file = LOCAL_BIBLE_DIR / version / f"{book}_{chapter}.txt"
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                chapter_verses = f.readlines()
                for verse_num in verses_to_fetch:
                    print(chapter_verses[verse_num - 1].strip())  # Adjusted for zero-based indexing
        except FileNotFoundError:
            print(f"File not found: {chapter_file}")
        except IndexError:
            print(f"Verse number out of range in {book} chapter {chapter}, verse {verse_num}")
