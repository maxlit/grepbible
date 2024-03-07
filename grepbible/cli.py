import argparse
from grepbible.bible_manager import get_verse, list_bibles

def main():
    parser = argparse.ArgumentParser(description="CLI tool to look up Bible verses.")
    parser.add_argument('-c', '--citation', help="Verse citation (e.g., 'Gen 1:1').", required=False)
    parser.add_argument('-v', '--version', help="Bible version(s), separated by commas.", required=False, default="kj")
    parser.add_argument('-l', '--list', action='store_true', help="List all available Bibles.")
    parser.add_argument('-i', '--interleave', action='store_true', help="Interleave verses for multiple versions.")

    args = parser.parse_args()

    if args.list:
        list_bibles()
    elif args.citation:
        # Pass the interleave flag to the get_verse function
        get_verse(args.version, args.citation, args.interleave)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()