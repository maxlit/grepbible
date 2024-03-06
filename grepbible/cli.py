import argparse
from grepbible.bible_manager import get_verse, list_bibles

def main():
    parser = argparse.ArgumentParser(description="CLI tool to look up Bible verses.")
    parser.add_argument('-c', '--citation', help="Verse citation (e.g., 'Gen 1:1').", required=False)
    parser.add_argument('-v', '--version', help="Bible version.", required=False)
    parser.add_argument('-l', '--list', action='store_true', help="List all available Bibles.")

    args = parser.parse_args()

    if args.list:
        list_bibles()
    elif args.citation and args.version:
        get_verse(args.version, args.citation)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()