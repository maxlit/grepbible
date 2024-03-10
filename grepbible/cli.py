import argparse
import json
from grepbible.bible_manager import *

def main():
    parser = argparse.ArgumentParser(description="CLI tool to look up Bible verses.")
    parser.add_argument('-c', '--citation', help="Verse citation (e.g., 'Gen 1:1').", required=False)
    parser.add_argument('-v', '--version', help="Bible version(s), separated by commas.", required=False, default="kj")
    parser.add_argument('-d', '--download', help="Download Bible version(s), separated by commas.", required=False)
    parser.add_argument('-l', '--list', action='store_true', help="List all available Bibles.")
    parser.add_argument('-b', '--books', action='store_true', help="List all available books (KJV names used).")
    parser.add_argument('-i', '--interleave', action='store_true', help="Interleave verses for multiple versions.")
    parser.add_argument('-r', '--random', help='Return a random quote.', action='store_true')
    parser.add_argument('--parse', action='store_true', help='(technical) Parse the citation and return JSON output')


    args = parser.parse_args()

    if args.list:
        list_bibles()
    elif args.citation and args.parse:
        parsed_details = parse_citation(args.citation)
        if parsed_details:
            print(json.dumps(parsed_details))  # Output parsed details as JSON
        else:
            print(json.dumps({"error": "Could not parse the citation"}))
    elif args.citation:
        # Pass the interleave flag to the get_verse function
        get_verse(args.version, args.citation, args.interleave)
    elif args.download:
        for version in args.download.split(','):
            download_and_extract_bible(version)
    elif args.books:
        list_books()
    elif args.random:
        get_random_quote(args.version, args.interleave)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()