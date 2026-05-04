import zipfile
import json
import os
from xml.etree import ElementTree as ET
from langchain_core.tools import tool


def _extract_docx(path: str) -> str:
    with zipfile.ZipFile(path, "r") as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    lines = []
    for para in tree.getroot().iter(f"{ns}p"):
        texts = [t.text for t in para.iter(f"{ns}t") if t.text]
        if texts:
            lines.append("".join(texts))
    return "\n".join(lines)


def _extract_pdf(path: str) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text(layout=True) or "" for p in pdf.pages)
    except ImportError:
        raise RuntimeError("pdfplumber not installed. Run: pip install pdfplumber")


@tool
def read_paper(file_path: str) -> str:
    """Read a paper file (.pdf, .txt, .docx) and return its text content."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return _extract_pdf(file_path)
    elif ext == ".docx":
        return _extract_docx(file_path)
    elif ext == ".txt":
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")


@tool
def save_coding_result(paper_title: str, result_json: str) -> str:
    """Save the coding result JSON to the result directory. paper_title is used as filename."""
    out_dir = os.path.join(os.path.dirname(__file__), "result")
    os.makedirs(out_dir, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in " -_" else "_" for c in paper_title)[:80]
    out_path = os.path.join(out_dir, f"{safe_name}.json")
    data = json.loads(result_json)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return f"Saved to {out_path}"
