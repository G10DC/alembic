import json
import re
from pathlib import Path

def extract_terms_from_text(text, section_idx):
    # Regex to find **term** followed by definition on the same line
    # Match: * **term**: definition OR - **term** is definition
    # We will search each line
    terms = {}
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        # Find all occurrences of **term**
        matches = list(re.finditer(r"\*\*([^*]+)\*\*", line))
        if matches:
            for idx, match in enumerate(matches):
                term = match.group(1).strip()
                # Find definition: text after this term on the line
                start_def = match.end()
                # If there is another term after this on the same line, stop definition there
                end_def = matches[idx+1].start() if idx+1 < len(matches) else len(line)
                definition = line[start_def:end_def].strip()
                # Clean up definition
                definition = re.sub(r"^[:\-–\s\=]+", "", definition).strip()
                # Remove common Italian verbs like "è", "significa", "si definisce come" from starting the definition
                definition = re.compile(r"^(si\s+definisce\s+come|significa|è|significano|sono|si\s+intende\s+per|si\s+riferisce\s+a)\s+", re.IGNORECASE).sub("", definition)
                definition = definition.strip()
                if definition and len(definition) > 3:
                    if term not in terms:
                        terms[term] = []
                    terms[term].append(definition)
    return terms

def main():
    condensed_dir = Path("/Users/gdc410/Desktop/TDC/work/condensed")
    output_file = Path("/Users/gdc410/Desktop/TDC/work/output_merged.md")
    
    chunk_files = sorted(list(condensed_dir.glob("chunk_*.md")), key=lambda p: int(p.stem.split("_")[1]))
    
    sections_text = []
    toc = ["# Table of Contents\n"]
    glossary_data = {}
    
    for idx, path in enumerate(chunk_files, start=1):
        content = path.read_text(encoding="utf-8")
        sections_text.append(content)
        
        # Build TOC entry: search for heading in file
        heading = f"Capitolo/Sezione {idx}"
        for line in content.splitlines():
            if line.startswith("## "):
                heading = line.replace("## ", "").strip()
                break
        
        anchor = heading.lower().replace(" ", "-").replace("/", "").replace("(", "").replace(")", "").replace(".", "")
        toc.append(f"- [{heading}](#{anchor})")
        
        # Extract terms
        chunk_terms = extract_terms_from_text(content, idx)
        for term, defs in chunk_terms.items():
            lower_term = term.lower()
            if lower_term not in glossary_data:
                glossary_data[lower_term] = {"original_case": term, "definitions": []}
            for d in defs:
                glossary_data[lower_term]["definitions"].append((idx, d))
                
    # Build final markdown
    full_markdown = []
    full_markdown.append("# Modelli di Amministrazioni Pubbliche — Studio Guidato")
    full_markdown.append("> Condensato da Alembic con preservazione integrale dei concetti.\n")
    
    full_markdown.append("\n".join(toc))
    full_markdown.append("\n---\n")
    
    # Add body sections
    full_markdown.append("\n\n---\n\n".join(sections_text))
    full_markdown.append("\n\n---\n\n")
    
    # Add Glossary
    full_markdown.append("# Glossario dei Termini Chiave")
    
    sorted_terms = sorted(glossary_data.keys())
    for t_lower in sorted_terms:
        term_info = glossary_data[t_lower]
        term_name = term_info["original_case"]
        definitions = term_info["definitions"]
        
        # Deduplicate identical definitions
        seen_defs = set()
        unique_defs = []
        for sec, d in definitions:
            clean_d = d.lower().strip()
            if clean_d not in seen_defs:
                seen_defs.add(clean_d)
                unique_defs.append((sec, d))
                
        full_markdown.append(f"### {term_name}")
        for sec, d in unique_defs:
            full_markdown.append(f"- **(Sezione {sec})**: {d}")
            
    output_file.write_text("\n\n".join(full_markdown), encoding="utf-8")
    print(f"Merged output saved to {output_file}")

if __name__ == "__main__":
    main()
