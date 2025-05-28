from pathlib import Path
from rapidfuzz import fuzz
import argparse

def fuzzy_grep(folder, query, threshold=75, scorer=fuzz.partial_ratio):
    folder = Path(folder)
    matches = []
    for file_path in folder.rglob("*.txt"):
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                score = scorer(query, line)
                if score >= threshold:
                    matches.append((file_path, lineno, score, line))
    matches.sort(reverse=True, key=lambda x: x[2])  # sort by score descending
    return matches

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Folder to search")
    parser.add_argument("query", help="Query string")
    parser.add_argument("--threshold", type=int, default=75, help="Minimum fuzzy match score (0–100)")
    parser.add_argument("--scorer", choices=["partial", "ratio", "token_sort"], default="partial", help="Fuzzy matching strategy")
    parser.add_argument("--show-scores", action="store_true", help="Show match scores in output")
    args = parser.parse_args()

    scorer_map = {
    "ratio": fuzz.ratio,
    "partial": fuzz.partial_ratio,
    "token_sort": fuzz.token_sort_ratio,
    "token_set": fuzz.token_set_ratio,
    "partial_token_sort": fuzz.partial_token_sort_ratio,
    "partial_token_set": fuzz.partial_token_set_ratio,
}


    scorer = scorer_map[args.scorer]
    results = fuzzy_grep(args.folder, args.query, args.threshold, scorer)

    for file, lineno, score, line in results:
        if args.show_scores:
            print(f"{file}:{lineno} [{score:.1f}%] {line}")
        else:
            print(f"{file}:{lineno} {line}")
