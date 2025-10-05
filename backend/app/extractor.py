import re
from typing import List, Dict, Any
import fitz  


def snippet_around(text: str, start: int, end: int, radius: int = 60) -> str:
    s = max(0, start - radius)
    e = min(len(text), end + radius)
    return text[s:e].strip().replace('\n', ' ')

class PDFExtractor:
    def __init__(self):
        self.date_regex = re.compile(
            r"\b(?:\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\d{4}[\-]\d{1,2}[\-]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?,?\s+\d{1,2},?\s+\d{2,4})\b",
            re.I,
        )
        self.amount_regex = re.compile(r"\b(?:Rs\.?|INR|USD|\$|EUR|€)\s?[\d,]+(?:\.\d+)?\b", re.I)
        self.signature_keywords = ["signed", "signature", "for and on behalf", "authorised signatory", "signatory"]

    def extract_pages(self, pdf_path: str) -> List[str]:
        """Return list of page texts (0-indexed pages)."""
        doc = fitz.open(pdf_path)
        pages = []
        for p in range(len(doc)):
            page = doc.load_page(p)
            text = page.get_text("text")
            pages.append(text)
        return pages

    def find_all_regex(self, regex: re.Pattern, pages: List[str]) -> List[Dict[str, Any]]:
        matches = []
        for i, page_text in enumerate(pages):
            for m in regex.finditer(page_text):
                start, end = m.span()
                matches.append(
                    {
                        "snippet": snippet_around(page_text, start, end),
                        "page": i + 1,
                        "start_char": start,
                        "end_char": end,
                        "rationale": f"Matched regex: {regex.pattern}" ,
                    }
                )
        return matches

    def find_keyword_context(self, keyword: str, pages: List[str]) -> List[Dict[str, Any]]:
        matches = []
        pattern = re.compile(re.escape(keyword), re.I)
        for i, page_text in enumerate(pages):
            for m in pattern.finditer(page_text):
                start, end = m.span()
                matches.append(
                    {
                        "snippet": snippet_around(page_text, start, end),
                        "page": i + 1,
                        "start_char": start,
                        "end_char": end,
                        "rationale": f"Keyword match: '{keyword}'",
                    }
                )
        return matches

    def generic_search(self, query: str, pages: List[str]) -> List[Dict[str, Any]]:
        terms = [t for t in re.split(r"\W+", query) if len(t) > 2]
        results = []
        seen = set()
        for term in terms:
            term_matches = self.find_keyword_context(term, pages)
            for m in term_matches:
                key = (m['page'], m['start_char'], m['end_char'])
                if key not in seen:
                    seen.add(key)
                    results.append(m)
        return results

    def handle_pointer(self, pointer: str, pages: List[str]) -> List[Dict[str, Any]]:
        p = pointer.lower()
        if any(k in p for k in ["date", "dates"]):
            matches = self.find_all_regex(self.date_regex, pages)
            return matches if matches else [{"snippet": "", "page": None, "start_char": None, "end_char": None, "rationale": "No date-like pattern found; try a different pointer or supply examples."}]

        if any(k in p for k in ["amount", "total", "value", "price", "contract value", "contract amount"]):
            matches = self.find_all_regex(self.amount_regex, pages)
            return matches if matches else [{"snippet": "", "page": None, "start_char": None, "end_char": None, "rationale": "No currency/amount pattern found."}]

        if any(k in p for k in ["who signed", "signed", "signature", "signatory"]):
            results = []
            for kw in self.signature_keywords:
                results += self.find_keyword_context(kw, pages)
            title_re = re.compile(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+){0,2})\s*,?\s*(Director|Manager|CEO|CFO|Partner|Proprietor)", re.I)
            
            for i, page_text in enumerate(pages):
                for m in title_re.finditer(page_text):
                    start, end = m.span()
                    results.append({
                        "snippet": snippet_around(page_text, start, end),
                        "page": i + 1,
                        "start_char": start,
                        "end_char": end,
                        "rationale": "Possible signatory line (name + title)",
                    })
            if results:
                
                seen = set()
                out = []
                for r in results:
                    key = (r['page'], r['start_char'], r['end_char'])
                    if key in seen: continue
                    seen.add(key)
                    out.append(r)
                return out
            return [{"snippet": "", "page": None, "start_char": None, "end_char": None, "rationale": "No likely signature lines found."}]

        
        generic = self.generic_search(pointer, pages)
        if generic:
            return generic
        return [{"snippet": "", "page": None, "start_char": None, "end_char": None, "rationale": "No matches found for the pointer."}]