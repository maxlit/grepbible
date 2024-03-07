import argparse
from grepbible.bible_manager import *

def main():
    parser = argparse.ArgumentParser(description="CLI tool to look up Bible verses.")
    parser.add_argument('-c', '--citation', help="Verse citation (e.g., 'Gen 1:1').", required=False)
    parser.add_argument('-v', '--version', help="Bible version(s), separated by commas.", required=False, default="kj")
    parser.add_argument('-d', '--download', help="Download Bible version(s), separated by commas.", required=False)
    parser.add_argument('-l', '--list', action='store_true', help="List all available Bibles.")
    parser.add_argument('-b', '--books', action='store_true', help="List all available books (KJV names used).")
    parser.add_argument('-i', '--interleave', action='store_true', help="Interleave verses for multiple versions.")

    args = parser.parse_args()

    if args.list:
        list_bibles()
    elif args.citation:
        # Pass the interleave flag to the get_verse function
        get_verse(args.version, args.citation, args.interleave)
    elif args.download:
        for version in args.download.split(','):
            download_and_extract_bible(version)
    elif args.books:
        list_books()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()