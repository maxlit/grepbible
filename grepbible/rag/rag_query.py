import faiss
import pickle
from sentence_transformers import SentenceTransformer
from langdetect import detect
import numpy as np
from pathlib import Path
import argparse

def load_model(model_name):
    return SentenceTransformer(model_name)

def detect_language(text):
    from langdetect import detect
    return detect(text)

def query_rag(query, index_root="~/data/bible/rag_index", lang=None, 
              model_name="all-MiniLM-L6-v2", top_k=5, threshold=None):
    if not lang:
        lang = detect_language(query) 
        print(f"Detected language: {lang}")
    
    model = load_model(model_name)
    
    index_root = Path(index_root).expanduser()
    index_path = index_root / lang / model_name / "faiss.index"
    meta_path = index_root / lang / model_name / "metadata.pkl"

    if not index_path.exists() or not meta_path.exists():
        print(f"No index for language '{lang}' with model '{model_name}' in {index_root}")
        return []

    query_vector = model.encode([query])[0]
    # Normalize the query vector
    query_vector = query_vector / np.linalg.norm(query_vector)
    
    index = faiss.read_index(str(index_path))
    
    D, I = index.search(query_vector.reshape(1, -1), top_k)
    
    with open(meta_path, "rb") as f:
        docs = pickle.load(f)
    
    results = []
    for score, idx in zip(D[0], I[0]):
        if threshold is not None and score < threshold:
            continue
            
        # Get the source file and content
        source_file = docs[idx].metadata["source"]
        content = docs[idx].page_content
        
        # Find the line number by reading the file
        with open(source_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip() == content:
                    results.append({
                        "text": content,
                        "source": source_file,
                        "line": line_num,
                        "score": float(score)
                    })
                    break

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Query the RAG index')
    parser.add_argument('--index-folder', default="~/data/bible/rag_index", 
                       help='Folder containing the RAG index')
    parser.add_argument('--query', help='Query to search for. If not provided, enters interactive mode')
    parser.add_argument('--lang', help='Language/version tag (e.g., kj for King James). If not provided, will try to auto-detect')
    parser.add_argument('--model', default="all-MiniLM-L6-v2",
                       help='Name of the sentence transformer model to use')
    parser.add_argument('--top-k', type=int, default=5, help='Number of results to return')
    parser.add_argument('--threshold', type=float, help='cosine similarity threshold')
    parser.add_argument('--show-scores', action='store_true', help='Show L2 distance scores in output')
    
    args = parser.parse_args()
    
    if args.query:
        results = query_rag(args.query, index_root=args.index_folder, lang=args.lang, 
                          model_name=args.model, top_k=args.top_k, threshold=args.threshold)
        for i, res in enumerate(results, 1):
            score_text = f" — Score: {res['score']:.3f}" if args.show_scores else ""
            print(f"\nResult {i}{score_text} — Source: {res['source']} (Line {res['line']})\n{res['text']}")
    else:
        while True:
            q = input("\n🔍 Enter your query (or 'q' to quit): ")
            if q.strip().lower() == 'q':
                break
            results = query_rag(q, index_root=args.index_folder, lang=args.lang,
                              model_name=args.model, top_k=args.top_k, threshold=args.threshold)
            for i, res in enumerate(results, 1):
                score_text = f" — Score: {res['score']:.3f}" if args.show_scores else ""
                print(f"\nResult {i}{score_text} — Source: {res['source']} (Line {res['line']})\n{res['text']}")
