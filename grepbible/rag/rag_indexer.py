from pathlib import Path
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
import faiss
import numpy as np
import pickle
import argparse

def load_line_chunks(folder_path, lang_tag):
    docs = []
    for file_path in Path(folder_path).rglob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    docs.append(Document(
                        page_content=line,
                        metadata={
                            "source": str(file_path),
                            "lang": lang_tag
                        }
                    ))
    return docs

def build_index(docs, lang_tag, model_name="paraphrase-multilingual-MiniLM-L12-v2", index_folder="rag_index", batch_size=1000):
    model = SentenceTransformer(model_name)
    out_dir = Path(index_folder) / lang_tag / model_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Initialize the index first
    sample_embedding = model.encode(["sample text"])[0]
    dim = len(sample_embedding)
    index = faiss.IndexFlatIP(dim)

    # Process in batches
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i:i + batch_size]
        texts = [doc.page_content for doc in batch_docs]
        print(f"Processing batch {i//batch_size + 1}/{(len(docs)-1)//batch_size + 1}")
        
        embeddings = model.encode(texts, show_progress_bar=True)
        faiss.normalize_L2(embeddings)
        index.add(np.array(embeddings))

    faiss.write_index(index, str(out_dir / "faiss.index"))
    with open(out_dir / "metadata.pkl", "wb") as f:
        pickle.dump(docs, f)

def index_all_languages(base_folder, model_name="paraphrase-multilingual-MiniLM-L12-v2", index_folder="rag_index"):
    base_path = Path(base_folder)
    if base_path.is_dir():
        folder_tag = base_path.name  # Use the folder name as the tag
        print(f"Indexing {folder_tag} with model {model_name}...")
        docs = load_line_chunks(base_path, folder_tag)
        build_index(docs, folder_tag, model_name, index_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Index text files for RAG retrieval')
    parser.add_argument('--input-folder', required=True, help='Input folder containing text files')
    parser.add_argument('--index-folder', required=True, help='Output folder for the RAG index')
    parser.add_argument('--model', default="paraphrase-multilingual-MiniLM-L12-v2",
                       help='Name of the sentence transformer model to use')
    
    args = parser.parse_args()
    index_all_languages(args.input_folder, args.model, args.index_folder)
