import os
import sys
import json
from agents.llm_client import call_llm

def log_debug(msg):
    print(f"[DEBUG] [IngestResources] {msg}", file=sys.stderr)

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    # Text-based files
    if ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
            
    # Try using MarkItDown if installed
    try:
        from markitdown import MarkItDown
        log_debug(f"Attempting to extract text from {os.path.basename(file_path)} using MarkItDown...")
        md = MarkItDown()
        result = md.convert(file_path)
        return result.text_content
    except ImportError:
        log_debug("MarkItDown python library not installed. Falling back to simple checks.")
        
    # Python fallback for PDF if markitdown isn't available
    if ext == ".pdf":
        try:
            import pypdf
            log_debug("Using pypdf fallback...")
            reader = pypdf.PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except ImportError:
            log_debug("pypdf not installed. Cannot parse PDF without markitdown or pypdf.")
            
    log_debug(f"Unsupported file type or parser missing for {file_path}")
    return ""

def classify_and_extract_rubrics(text):
    prompt = f"""
You are an Academic Coordinator at WELL Labs.
Analyze the following text extracted from an induction training resource:

--- START OF TEXT ---
{text[:6000]}
--- END OF TEXT ---

Task:
1. Classify this resource into one of the 6 IRC induction modules (1 to 6).
   - Module 1: Scientific Method / Introduction
   - Module 2: Literature Review / Research Framing
   - Module 3: Research Design & Question Formulation
   - Module 4: Methodologies & Hydrology
   - Module 5: Data Collection
   - Module 6: Data Analysis & Presentation
2. Extract the core scientific concepts, terms, and specific grading rubrics or requirements for student reflections.

Output the result strictly as a valid JSON object matching this schema:
{{
  "module_number": 1, // Integer from 1 to 6
  "module_name": "Module Title",
  "core_concepts": ["concept A", "concept B"],
  "grading_rubrics": ["rubric 1", "rubric 2"]
}}
"""
    log_debug("Calling LLM client to classify and extract rubrics...")
    response_str = call_llm(prompt, json_mode=True)
    return json.loads(response_str)

def main():
    if len(sys.argv) < 2:
        log_debug("ERROR: Missing target resources directory.")
        sys.exit(1)
        
    resources_dir = sys.argv[1]
    if not os.path.exists(resources_dir):
        log_debug(f"ERROR: Resources directory '{resources_dir}' does not exist.")
        sys.exit(1)
        
    log_debug(f"Scanning resources directory: {resources_dir}")
    
    # Target rubrics cache
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "resources")
    os.makedirs(output_dir, exist_ok=True)
    rubrics_file = os.path.join(output_dir, "session_rubrics.json")
    
    # Load existing rubrics if present
    rubrics_data = {}
    if os.path.exists(rubrics_file):
        try:
            with open(rubrics_file, "r", encoding="utf-8") as f:
                rubrics_data = json.load(f)
        except Exception:
            pass
            
    files_processed = 0
    for root, _, files in os.walk(resources_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Skip temp or metadata files
            if file.startswith("~$") or file.startswith("."):
                continue
                
            text = extract_text_from_file(file_path)
            if not text.strip():
                continue
                
            try:
                result = classify_and_extract_rubrics(text)
                mod_num = str(result.get("module_number"))
                if mod_num and mod_num in ["1", "2", "3", "4", "5", "6"]:
                    rubrics_data[mod_num] = {
                        "module_name": result.get("module_name"),
                        "core_concepts": result.get("core_concepts", []),
                        "grading_rubrics": result.get("grading_rubrics", [])
                    }
                    log_debug(f"Successfully processed and mapped {file} to Module {mod_num}")
                    files_processed += 1
            except Exception as e:
                log_debug(f"Error processing {file}: {e}")
                
    # Save the updated rubrics cache
    with open(rubrics_file, "w", encoding="utf-8") as f:
        json.dump(rubrics_data, f, indent=2)
        
    log_debug(f"Ingestion complete. Processed {files_processed} files. Rubrics saved in {rubrics_file}")
    print(json.dumps({"status": "success", "processed_files_count": files_processed}))

if __name__ == "__main__":
    main()
