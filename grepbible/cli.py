import argparse
import json
from pathlib import Path
from grepbible.bible_manager import *

DEFAULT_RAG_THRESHOLD = 0.3 # depends strongly on the model used (and language in case of multilingual models), and the query
DEFAULT_FUZZ_THRESHOLD = 0.85

def main():
    parser = argparse.ArgumentParser(description="CLI tool to look up Bible verses.")
    parser.add_argument('-c', '--citation', help="Verse citation (e.g., 'Gen 1:1').", required=False)
    parser.add_argument('-v', '--version', help="Bible version(s), separated by commas.", required=False, default="kj")
    parser.add_argument('-d', '--download', help="Download Bible version(s), separated by commas.", required=False)
    parser.add_argument('-l', '--list', action='store_true', help="List all available Bibles.")
    parser.add_argument('-b', '--books', action='store_true', help="List all available books (KJV names used).")
    parser.add_argument('-i', '--interleave', action='store_true', help="Interleave verses for multiple versions.")
    parser.add_argument('-r', '--random', help='Return a random quote.', action='store_true')
    parser.add_argument('-s', help='Search in Bible text', metavar='QUERY')
    parser.add_argument('--rag', action='store_true', help='Use semantic search instead of fuzzy matching (requires ML dependencies)')
    parser.add_argument('--threshold', type=float, help=f'Useful only for search. Minimum similarity threshold between 0 and 1 (default: {DEFAULT_RAG_THRESHOLD} for RAG, {DEFAULT_FUZZ_THRESHOLD} for fuzzy)')
    parser.add_argument('--parse', action='store_true', help='(technical) Parse the citation and return JSON output')

    args = parser.parse_args()

    if args.list:
        list_bibles()
    elif args.citation and args.parse:
        parsed_details = parse_citation(args.citation)
        if parsed_details:
            print(json.dumps(parsed_details))
        else:
            print(json.dumps({"error": "Could not parse the citation"}))
    elif args.s:  # Search handling
        if args.rag:
            from grepbible.rag.rag_query import query_rag
            threshold = args.threshold if args.threshold is not None else DEFAULT_RAG_THRESHOLD
            results = query_rag(args.s, lang=args.version, threshold=threshold)
            for res in results:
                print(f"{res['source']}:{res['line']}:{res['text']}")
        else:
            from grepbible.fuzz.fuzz_search import fuzzy_grep
            bible_folder = Path.home() / "grepbible_data" / args.version
            threshold = args.threshold if args.threshold is not None else DEFAULT_FUZZ_THRESHOLD
            results = fuzzy_grep(bible_folder, args.s, threshold=threshold)
            for file, lineno, score, line in results:
                print(f"{file}:{lineno}:{line}")
    elif args.citation:
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