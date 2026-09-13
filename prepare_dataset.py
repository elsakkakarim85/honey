import os
import json
import PyPDF2

RAW_DIR = "raw_beekeeping_books"
OUTPUT_FILE = "ApisLM_Local_AI/beekeeping_dataset.jsonl"

def extract_text_from_pdfs(directory):
    print(f"Scanning '{directory}' for real PDF books...")
    corpus = ""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created '{directory}'. Waiting for user to drop PDF files.")
        return corpus

    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("No PDFs found yet. Drop real books into the folder.")
        return corpus
        
    for filename in pdf_files:
        filepath = os.path.join(directory, filename)
        print(f"Parsing {filename}...")
        try:
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        corpus += text + "\n"
        except Exception as e:
            print(f"Error parsing {filename}: {e}")
            
    return corpus

def chunk_into_jsonl(text, chunk_size=1000):
    if not text:
        return
        
    print(f"Chunking corpus and generating Instruction/Response dataset...")
    # Very basic chunking logic for demo purposes
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for chunk in chunks:
            # Formatting as required by Unsloth/QLoRA Instruction dataset
            entry = {
                "text": f"### Instruction:\nAnalyze the following apiculture context.\n\n### Input:\n{chunk[:50]}...\n\n### Response:\n{chunk}"
            }
            out.write(json.dumps(entry) + "\n")
            
    print(f"Dataset successfully compiled into {OUTPUT_FILE}! Ready for QLoRA Fine-tuning.")

if __name__ == "__main__":
    corpus_text = extract_text_from_pdfs(RAW_DIR)
    chunk_into_jsonl(corpus_text)
