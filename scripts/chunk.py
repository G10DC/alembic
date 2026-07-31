import json
from pathlib import Path

def word_count(text):
    return len(text.split())

def main():
    root = Path("/Users/gdc410/Desktop/TDC/work/extracted")
    src_file = Path("/Users/gdc410/Desktop/TDC/work/extracted/sections/001_parte-di-chi-sta-dentro-e-di-chi-sta-fuori-l-autor.txt")
    
    text = src_file.read_text(encoding="utf-8")
    paragraphs = text.split("\n\n")
    
    chunks = []
    current_chunk = []
    current_words = 0
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        p_words = word_count(p)
        if current_words + p_words > 4000 and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_words = p_words
        else:
            current_chunk.append(p)
            current_words += p_words
            
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    sec_dir = root / "sections"
    
    # Remove the original huge file to keep it clean
    src_file.unlink()
    
    manifest = []
    for i, chunk_text in enumerate(chunks, start=1):
        fname = f"{i:03d}_chunk_{i:02d}.txt"
        path = sec_dir / fname
        path.write_text(chunk_text, encoding="utf-8")
        
        # Take the first line or first few words as a preview title
        lines = chunk_text.splitlines()
        first_line = lines[0].strip() if lines else f"Chunk {i}"
        title = first_line[:50] if len(first_line) > 50 else first_line
        if not title:
            title = f"Chunk {i}"
            
        manifest.append({
            "index": i,
            "title": f"Capitolo/Sezione {i} - {title}",
            "path": str(path),
            "word_count": word_count(chunk_text),
            "detection_method": "paragraph_window"
        })
        
    (root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Split single section into {len(manifest)} chunks.")

if __name__ == "__main__":
    main()
