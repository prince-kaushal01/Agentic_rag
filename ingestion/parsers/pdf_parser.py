from pathlib import Path
import fitz  # PyMuPDF
from ingestion.parsers.base import BaseParser, ParsedDocument


class PDFParser(BaseParser):
    supported_extensions = [".pdf"]

    def parse(self, path: Path) -> ParsedDocument:
        doc = fitz.open(str(path))
        pages = []
        full_text_parts = []

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if text:
                pages.append({"page": page_num, "text": text})
                full_text_parts.append(text)

        doc.close()
        full_text = "\n\n".join(full_text_parts)

        return ParsedDocument(
            file_name=path.name,
            file_type="pdf",
            title=path.stem.replace("_", " ").replace("-", " "),
            content=full_text,
            pages=pages,
            metadata={"total_pages": len(pages), "source_path": str(path)},
        )
