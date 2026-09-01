from pathlib import Path
from docx import Document
from ingestion.parsers.base import BaseParser, ParsedDocument


class DOCXParser(BaseParser):
    supported_extensions = [".docx", ".doc"]

    def parse(self, path: Path) -> ParsedDocument:
        doc = Document(str(path))
        sections = []
        current_section = {"title": "Introduction", "text": ""}
        full_parts = []

        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue

            if para.style.name.startswith("Heading"):
                if current_section["text"].strip():
                    sections.append(current_section)
                current_section = {"title": text, "text": ""}
            else:
                current_section["text"] += text + "\n"
                full_parts.append(text)

        if current_section["text"].strip():
            sections.append(current_section)

        return ParsedDocument(
            file_name=path.name,
            file_type="docx",
            title=path.stem.replace("_", " ").replace("-", " "),
            content="\n".join(full_parts),
            sections=sections,
            metadata={"total_sections": len(sections), "source_path": str(path)},
        )
