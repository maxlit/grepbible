import argparse
import json
from pathlib import Path
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
    parser.add_argument('-s', help='Search in Bible text', metavar='QUERY')
    parser.add_argument('--parse', action='store_true', help='(technical) Parse the citation and return JSON output')

    # Add search-related arguments
    search_group = parser.add_argument_group('search options')
    search_group.add_argument('--search', help='Search text in Bible verses')
    search_group.add_argument('--rag', action='store_true', help='Use RAG (semantic) search instead of fuzzy matching')
    search_group.add_argument('--top-k', type=int, default=5, help='Number of results to return')
    search_group.add_argument('--threshold', type=float, help='Minimum similarity threshold')
    search_group.add_argument('--show-scores', action='store_true', help='Show similarity scores in output')
    search_group.add_argument('--model', default="paraphrase-multilingual-MiniLM-L12-v2",
                            help='Model name for RAG search (only with --rag)')
    search_group.add_argument('--scorer', choices=['partial', 'ratio', 'token_sort', 'token_set',
                            'partial_token_sort', 'partial_token_set'], 
                            default='partial', help='Fuzzy matching strategy (without --rag)')

    args = parser.parse_args()

    if args.list:
        list_bibles()
    elif args.citation and args.parse:
        parsed_details = parse_citation(args.citation)
        if parsed_details:
            print(json.dumps(parsed_details))
        else:
            print(json.dumps({"error": "Could not parse the citation"}))
    elif args.s:  # New search handling
        if args.rag:
            from grepbible.rag.rag_query import query_rag
            results = query_rag(args.s, lang=args.version)
            for res in results:
                print(f"{res['source']}:{res['text']}")
        else:
            from grepbible.fuzz.fuzz_search import fuzzy_grep
            bible_folder = Path.home() / "grepbible_data" / args.version
            results = fuzzy_grep(bible_folder, args.s, threshold=70)
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